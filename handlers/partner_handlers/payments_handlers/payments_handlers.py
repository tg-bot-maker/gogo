from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from handlers.states import SG
from models.adapters.base_adapter import BaseAdapter
from models.adapters.admin_panel_adapter import AdminPanelAdapter
from models.adapters.user_adapter import UserAdapter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pagination.MagicPaginator import ButtonPagination
from aiogram.utils import exceptions
from apscheduler.schedulers.asyncio import AsyncIOScheduler



async def pay_btn(call: types.CallbackQuery, state: FSMContext):
    admin_panel_adapter = AdminPanelAdapter()
    text, keyboard = await admin_panel_adapter.get_user_payment_link(call.from_user.id)
    await call.message.edit_text(text=text, reply_markup=keyboard)


async def payment_done_btn(call: types.CallbackQuery, scheduler: AsyncIOScheduler):
    user_adapter = UserAdapter()
    admin_panel_adapter = AdminPanelAdapter()
    await admin_panel_adapter.write_payment_done_datetime(call.from_user.id)
    await user_adapter.update_user_stage(call.from_user.id, "payment_done", call, scheduler)
    base_adapter = BaseAdapter()
    keyboard = await base_adapter.start(call.from_user.id)
    await call.message.edit_text(text=base_adapter._msg, reply_markup=keyboard)









async def payments_btn(call: types.CallbackQuery, state: FSMContext):
    admin_panel_adapter = AdminPanelAdapter()
    await admin_panel_adapter.payments_btn()
    await call.message.edit_text(text=admin_panel_adapter._msg, reply_markup=admin_panel_adapter._inline_keyboard)


async def back_to_payments_btn(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await payments_btn(call, state)


async def payments_statistics_btn(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text='◀︎', callback_data='payments_btn'))
    await call.message.edit_text(text="Функция в разработке!", reply_markup=keyboard)


async def create_invoice_btn(call: types.CallbackQuery, state: FSMContext):
    base_adapter = BaseAdapter()
    user_adapter = UserAdapter()
    user = await user_adapter.get_user(call.from_user.id)
    #if user.is_partner:
    keyboard_data = await base_adapter.get_users_for_invoice_for_partner_as_buttons(call.from_user.id)
    #else:
        #keyboard_data = await base_adapter.get_users_for_invoice_as_buttons()
    custom_keyboard = [InlineKeyboardButton(text='◀︎', callback_data='payments_btn')]
    paginator = ButtonPagination(button_data=keyboard_data, amount_elements=5)
    await state.update_data(paginator=paginator)
    try:
        keyboard = paginator.pagination(custom_keyboard=custom_keyboard)
        await call.message.edit_text(text="<b>Выберите клиента:</b>", reply_markup=keyboard)
        await SG.user_list_pagination_payments.set()
    except KeyError:
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text='◀︎', callback_data='payments_btn'))
        await call.message.edit_text(text="<b>Клиентов для выставления счета нет!</b>", reply_markup=keyboard)


async def invoice_creation_1(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(client_id=call.data.split("#")[-1])
    await state.update_data(call=call)
    await call.message.edit_text(text="<b>Отправьте ссылку на оплату:</b>")
    await SG.invoice_creation.set()


async def invoice_creation_2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    call = data.get("call")
    await state.update_data(payment_link=message.text)
    await message.delete()
    await call.message.edit_text(text="<b>Введите сумму платежа:</b>")
    await SG.invoice_creation_final.set()

async def invoice_creation_final(message: types.Message, state: FSMContext, scheduler: AsyncIOScheduler):
    data = await state.get_data()
    call = data.get("call")
    payment_link = data.get("payment_link")
    client_id = data.get("client_id")
    payment_amount = message.text
    await message.delete()
    admin_panel_adapter = AdminPanelAdapter()

    user_adapter = UserAdapter()
    user_stage = await user_adapter.get_user_stage(client_id)

    #Если клиент на этапе ожидание ссылки для оплаты, то сазу отправляем ее
    if user_stage == "payment":
        kb = InlineKeyboardMarkup().add(InlineKeyboardButton('Оплатить', callback_data='pay_btn'))
        await user_adapter.update_user_stage(client_id, "payment_ready", call, scheduler)
        await call.message.bot.send_message(reply_markup=kb, chat_id=client_id, text="<b>Ссылка на оплату была добавлена менеджером.</b>")
    #Если клиент на более раннем этапе, то не отправляем ему ссылку

    base_adapter = BaseAdapter()
    keyboard = await base_adapter.back_kb()
    await admin_panel_adapter.create_payment(client_id, payment_link, payment_amount)
    await call.message.edit_text(text=f"<b>Ссылка успешно сохранена!</b>", reply_markup=keyboard)


async def check_payments_btn(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(call=call)
    user_adapter = UserAdapter()
    custom_keyboard = [InlineKeyboardButton(text='◀︎', callback_data='payments_btn')]
    keyboard_data = await user_adapter.get_user_who_paid_for_partner_as_buttons(call.from_user.id)
    paginator = ButtonPagination(button_data=keyboard_data, amount_elements=5)
    await state.update_data(paginator=paginator)
    try:
        keyboard = paginator.pagination(custom_keyboard=custom_keyboard)
        await call.message.edit_text(text="<b>Выберите клиента:</b>", reply_markup=keyboard)
        await SG.users_who_paid_pagination.set()
    except KeyError:
        await call.message.edit_text(text="<b>Клиентов, которые совершили оплату пока нет!</b>",
                                     reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('◀️   Назад    ', callback_data='payments_btn')))



async def check_payments_detail(call: types.CallbackQuery, state: FSMContext):
    client_id = call.data.split("#")[-1]
    admin_panel_adapter = AdminPanelAdapter()
    client_fio = await admin_panel_adapter.get_client_fio_by_id(client_id)
    client_payment = await admin_panel_adapter.get_user_payment(client_id)

    keyboard = await admin_panel_adapter.check_payments_detail_kb(client_id)
    await call.message.edit_text(text=f"<b>📍 Платеж от клиента:</b>\n{client_fio}\n\n"
                                      f"<b>🔗 Ссылка:</b>\n{client_payment.payment_link}\n\n"
                                      f"<b>📅 Дата платежа:</b> {client_payment.payment_date}\n"
                                      f"<b>💰 Сумма платежа:</b> {client_payment.payment_amount}", reply_markup=keyboard)



async def approve_payment_from_client_btn(call: types.CallbackQuery, state: FSMContext, scheduler: AsyncIOScheduler):
    client_id = call.data.split("#")[-1]
    admin_panel_adapter = AdminPanelAdapter()
    base_adapter = BaseAdapter()
    user_adapter = UserAdapter()
    await admin_panel_adapter.approve_payment_from_client_btn(client_id)
    await user_adapter.update_user_stage(client_id, "payment_approved", call, scheduler)
    keyboard = await base_adapter.back_kb()
    await call.message.edit_text(text="<b>Платеж успешно подтвержден!</b>", reply_markup=keyboard)





# pagination handlers
async def user_list_pagination_payments(call: types.CallbackQuery, state: FSMContext):
    paginator = (await state.get_data()).get('paginator')
    keyboard = paginator.page_switch(call.data.split('#')[1])
    try:
        await call.message.edit_text(text="<b>Выберите клиента:</b>",
                                       reply_markup=keyboard)
        await state.update_data(paginator=paginator)
    except exceptions.MessageNotModified:
        await call.answer(text='Больше нет клиентов!', show_alert=True)


async def users_who_paid_pagination(call: types.CallbackQuery, state: FSMContext):
    paginator = (await state.get_data()).get('paginator')
    keyboard = paginator.page_switch(call.data.split('#')[1])
    try:
        await call.message.edit_caption(caption="<b>Выберите клиента:</b>", reply_markup=keyboard)
        await state.update_data(paginator=paginator)
    except exceptions.MessageNotModified:
        await call.answer(text='Больше нет клиентов!', show_alert=True)



def register_payments_handlers(dp: Dispatcher):
    dp.register_message_handler(
        invoice_creation_2,
        state=SG.invoice_creation
    )
    dp.register_message_handler(
        invoice_creation_final,
        state=SG.invoice_creation_final
    )
    dp.register_callback_query_handler(
        payments_btn,
        lambda callback_query: callback_query.data == 'payments_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        payment_done_btn,
        lambda callback_query: callback_query.data == 'payment_done_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        create_invoice_btn,
        lambda callback_query: callback_query.data == 'create_invoice_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        payments_statistics_btn,
        lambda callback_query: callback_query.data == 'payments_statistics_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        check_payments_btn,
        lambda callback_query: callback_query.data == 'check_payments_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        pay_btn,
        lambda callback_query: callback_query.data == 'pay_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        user_list_pagination_payments,
        lambda callback_query: callback_query.data.split("#")[0] == 'amg',
        state=SG.user_list_pagination_payments
    )
    dp.register_callback_query_handler(
        invoice_creation_1,
        lambda callback_query: callback_query.data.split("#")[1] == "user_number",
        state=SG.user_list_pagination_payments,
    )
    dp.register_callback_query_handler(
        users_who_paid_pagination,
        lambda callback_query: callback_query.data.split("#")[0] == 'amg',
        state=SG.users_who_paid_pagination
    )
    dp.register_callback_query_handler(
        check_payments_detail,
        lambda callback_query: callback_query.data.split("#")[1] == "user_number",
        state=SG.users_who_paid_pagination,
    )
    dp.register_callback_query_handler(
        approve_payment_from_client_btn,
        lambda callback_query: callback_query.data.split("#")[0] == "approve_payment_from_client_btn",
        state="*",
    )