from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from handlers.states import SG
from models.adapters.base_adapter import BaseAdapter
from models.adapters.partners_adapter import PartnersAdapter
from models.adapters.upload_documents_adapter import UploadDocumentsAdapter
from models.adapters.form_adapter import FormAdapter
from models.adapters.referral_system_adapter import ReferralSystemAdapter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pagination.MagicPaginator import ButtonPagination
from aiogram.utils import exceptions

from configs.config import stages



async def referral_system_btn(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await state.update_data(call=call)
    referral_system_adapter = ReferralSystemAdapter()
    keyboard = await referral_system_adapter.referral_system_kb(call)
    await call.message.edit_text(text="<b>Ваша партнерская ссылка для привлечения клиентов:\n"
                                      f"<code>https://t.me/{call.message.from_user.username}?start={call.from_user.id}</code></b>", reply_markup=keyboard)


async def back_to_referral_system_btn(call: types.CallbackQuery, state: FSMContext):
    await referral_system_btn(call, state)



async def ref_my_clients(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(call=call)
    partner_adapter = PartnersAdapter()
    keyboard_data = await partner_adapter.get_partner_clietns_as_buttons(call.from_user.id)
    custom_keyboard = [InlineKeyboardButton(text='◀︎', callback_data='back_to_partner_menu_btn')]
    paginator = ButtonPagination(button_data=keyboard_data, amount_elements=5)
    await state.update_data(paginator=paginator)
    try:
        keyboard = paginator.pagination(custom_keyboard=custom_keyboard)
        await call.message.edit_text(text="<b>Выберите клиента:</b>", reply_markup=keyboard)
        await SG.partner_clients_list_pagination.set()
    except KeyError:
        await call.message.edit_text(text="<b>Клиентов пока нет!</b>")




async def view_detail_user(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user_id = int(call.data.split("#")[2])
    await state.update_data(user_id=user_id)
    documents_adapter = UploadDocumentsAdapter()
    drive_link = await documents_adapter.get_drive_link(user_id)
    form_adapter = FormAdapter()
    base_adapter = BaseAdapter()
    partner_adapter = PartnersAdapter()
    form = await form_adapter.get_form(user_id)
    if form and user_id == call.from_user.id:
        user_fio = form.user_fio
        user_number = form.user_number
        keyboard = await partner_adapter.analytics_for_partner_kb(form_status=True, restart_func=True)
    elif not form and user_id == call.from_user.id:
        user_fio = "Анкета не заполнена"
        user_number = "Анкета не заполнена"
        keyboard = await partner_adapter.analytics_for_partner_kb(form_status=False, restart_func=True)
    elif form and user_id != call.from_user.id:
        user_fio = form.user_fio
        user_number = form.user_number
        keyboard = await partner_adapter.analytics_for_partner_kb(form_status=True, restart_func=False)
    else:
        user_fio = "Анкета не заполнена"
        user_number = "Анкета не заполнена"
        keyboard = await partner_adapter.analytics_for_partner_kb(form_status=False, restart_func=False)

    products = {"mortgage_btn": "Ипотека под ключ", "buy_property_btn": "Покупка недвижимости", "sell_property_btn": "Продажа недвижимости", "None": "Пока не выбран" }

    user = await base_adapter.get_user(user_id)
    text = "<b>Аналитика</b>  🔎\n\n"\
           f"<b>------------------------</b>\n" \
           f"<b>Username:</b> @{user.user_name}\n" \
           f"<b>Telegram ID:</b> <code>{str(user.user_id)}</code>\n" \
           f"<b>Дата регистрации:</b> {user.register_date}\n" \
           f"<b>Имя:</b> {user_fio}\n" \
           f"<b>Телефон:</b> {user_number}\n\n" \
           f"<b>📈 Этап:</b> {stages[user.user_stage]}\n" \
           f"<b>📍 Выбранный продукт:</b> {products[str(user.product_choice)]}\n" \
           f"<b>🔗 Ссылка на файлы:</b> {drive_link}\n"
    await call.message.edit_text(text=text, reply_markup=keyboard)


async def show_form_for_partner(call: types.CallbackQuery, state):
    await SG.partner_clients_list_pagination.set()
    accomodation_types = {"house": "Дом", "new_house": "Строительство дома", "flat": "Квартира", "new_flat": "Новостройка", "commercial": "Коммерческая", "apart": "Апартаменты"}
    symbols = {False: "❌", True: "✅"}
    data = await state.get_data()
    user_id = data.get("user_id")
    keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('◀️   Назад    ', callback_data=f'item#partner_number#{user_id}'))
    form_adapter = FormAdapter()
    form = await form_adapter.get_form(user_id)
    await call.message.edit_text(f"<b>ID Клиента:</b> {form.form_user_id}\n" 
                                 f"<b>Гражданство:</b> {form.citizenship}\n" 
                                 f"<b>Размер ипотеки:</b> {form.estimated_mortgage_amount}\n" 
                                 f"<b>Тип недвижимости:</b> {accomodation_types[form.accommodation_type]}\n" 
                                 f"<b>Размер первого взноса:</b> {form.down_payment_amount}\n"
                                 f"<b>Срок ипотеки:</b> {form.mortgage_term}\n"
                                 f"<b>Дети после 2018:</b> {symbols[form.children_after_2018]}\n"
                                 f"<b>Наличие кредитов:</b> {symbols[form.credits_in_the_past]}\n"
                                 f"<b>Официальная работа:</b> {symbols[form.official_job]}\n"
                                 f"<b>Судимости:</b> {symbols[form.convictions]}\n"
                                 f"<b>Банкротство:</b> {symbols[form.bankruptcy]}\n"
                                 f"<b>Просрочки по платежам:</b> {symbols[form.late_payments]}\n"
                                 f"<b>Брак:</b> {symbols[form.marriage]}\n"
                                 f"<b>Количество детей:</b> {form.children_amount}\n",
                                 reply_markup=keyboard)


async def restart_partner_for_testing_btn(call: types.CallbackQuery, state: FSMContext):
    base_adapter = BaseAdapter()
    keyboard = await base_adapter.back_kb()
    user_id = call.from_user.id
    partners_adapter = PartnersAdapter()
    await partners_adapter.restart_partner_for_testing(user_id)
    await call.message.edit_text(text="Сброс произведен!", reply_markup=keyboard)








#pagination_handler
async def partner_clients_pagination(call: types.CallbackQuery, state: FSMContext):
    paginator = (await state.get_data()).get('paginator')
    keyboard = paginator.page_switch(call.data.split('#')[1])
    try:
        await call.message.edit_text(text="<b>Выберите пользователя:</b>",
                                       reply_markup=keyboard)
        await state.update_data(paginator=paginator)
    except exceptions.MessageNotModified:
        await call.answer(text='Больше нет пользователей!', show_alert=True)



def register_referral_system_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        referral_system_btn,
        lambda callback_query: callback_query.data == 'referral_system_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        back_to_referral_system_btn,
        lambda callback_query: callback_query.data == 'back_to_referral_system_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        show_form_for_partner,
        lambda callback_query: callback_query.data == 'show_form_for_partner',
        state='*'
    )
    dp.register_callback_query_handler(
        restart_partner_for_testing_btn,
        lambda callback_query: callback_query.data == 'restart_partner_for_testing_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        ref_my_clients,
        lambda callback_query: callback_query.data in ['ref_my_clients', "go_back_to_my_clients_btn"],
        state='*'
    )
    dp.register_callback_query_handler(
        partner_clients_pagination,
        lambda callback_query: callback_query.data.split("#")[0] == 'amg',
        state=SG.partner_clients_list_pagination
    )
    dp.register_callback_query_handler(
        view_detail_user,
        lambda callback_query: callback_query.data.split("#")[1] == "partner_number",
        state=SG.partner_clients_list_pagination,
    )

