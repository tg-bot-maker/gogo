from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from handlers.states import SG
from models.adapters.partners_adapter import PartnersAdapter
from models.adapters.user_adapter import UserAdapter
from models.adapters.base_adapter import BaseAdapter
from models.adapters.admin_panel_adapter import AdminPanelAdapter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pagination.MagicPaginator import ButtonPagination
from aiogram.utils import exceptions

from handlers.admin_handlers.analytics_handlers.analytics_handlers import view_detail_user
from APscheduler.notifications.partner_notifications import notify_partner_assigned


async def partners_panel_for_admin_btn(call: types.CallbackQuery):
    admin_adapter = AdminPanelAdapter()
    keyboard = await admin_adapter.partners_panel_for_admin_btn()
    await call.message.edit_text(text=admin_adapter._msg, reply_markup=keyboard)


async def partner_list_for_admin_btn(call: types.CallbackQuery, state: FSMContext):
    partners_adapter = PartnersAdapter()
    keyboard_data = await partners_adapter.get_partners_list_as_buttons()
    keyboard_data = dict(reversed(keyboard_data.items()))
    await state.update_data(call=call)
    custom_keyboard = [InlineKeyboardButton(text='◀︎', callback_data='back_to_admin_menu_btn')]
    paginator = ButtonPagination(button_data=keyboard_data, amount_elements=5)
    await state.update_data(paginator=paginator)
    try:
        keyboard = paginator.pagination(custom_keyboard=custom_keyboard)
        await call.message.edit_text(text="<b>Партнеры:</b>", reply_markup=keyboard)
        await SG.partners_list_pagination.set()
    except KeyError:
        await call.message.edit_text(text="<b>Партнеров нет!</b>", reply_markup=InlineKeyboardMarkup().add(custom_keyboard[0]))


async def view_detail_partner(call: types.CallbackQuery, state: FSMContext):
    partner_id = int(call.data.split("#")[-1])
    partners_adapter = PartnersAdapter()
    keyboard = await partners_adapter.view_detail_partner(partner_id)
    await call.message.edit_text(text=partners_adapter._msg, reply_markup=keyboard)





async def create_partner_btn(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(call=call)
    await call.message.edit_text(text="<b>Введите ID пользователя:</b>")
    await SG.create_partner_final.set()

async def create_partner_final(message: types.Message, state: FSMContext):
    user_id = int(message.text)
    await message.delete()
    user_adapter = UserAdapter()
    partners_adapter = PartnersAdapter()
    user_name = await user_adapter.get_user_name(user_id)
    await partners_adapter.make_partner(user_id)
    data = await state.get_data()
    call = data.get("call")
    await notify_partner_assigned(message, user_id)
    await call.message.edit_text(text=f"Пользователь @{user_name} был назначен партнером!")




async def change_partner_btn(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(call=call)
    await call.message.edit_text(text="<b>Введите ID пользователя, для которого вы хотите изменить партнера:</b>")
    await SG.change_partner_choose_partner.set()

async def change_partner_choose_partner(message: types.Message, state: FSMContext):
    await state.update_data(user_id=int(message.text))
    await message.delete()
    data = await state.get_data()
    call = data.get("call")
    partners_adapter = PartnersAdapter()
    keyboard_data = await partners_adapter.get_partners_list_as_buttons()
    custom_keyboard = [InlineKeyboardButton(text='Убрать партнера 🚫', callback_data='item#partner_number#0000000000'), InlineKeyboardButton(text='◀︎', callback_data='back_to_admin_menu_btn')]
    paginator = ButtonPagination(button_data=keyboard_data, amount_elements=5)
    await state.update_data(paginator=paginator)
    try:
        keyboard = paginator.pagination(custom_keyboard=custom_keyboard)
        await call.message.edit_text(text="<b>Партнеры:</b>", reply_markup=keyboard)
        await SG.change_partner_choose_partner.set()
    except KeyError:
        await call.message.edit_text(text="<b>Партнеров нет!</b>", reply_markup=InlineKeyboardMarkup().add(custom_keyboard[0]))


async def change_partner_final(call: types.CallbackQuery, state: FSMContext):
    partner_id = int(call.data.split("#")[-1])
    data = await state.get_data()
    call = data.get("call")
    user_id = data.get("user_id")
    partners_adapter = PartnersAdapter()
    base_adapter = BaseAdapter()
    await partners_adapter.change_partner(user_id, partner_id)
    keyboard = await base_adapter.back_to_admin_kb()
    await call.message.edit_text(text="Партнер пользователя успешно изменен!", reply_markup=keyboard)




async def bank_contacts_btn(call: types.CallbackQuery):
    admin_adapter = AdminPanelAdapter()
    keyboard = await admin_adapter.bank_contacts_btn()
    await call.message.edit_text(text=admin_adapter._msg, reply_markup=keyboard)



async def users_without_partner_list_btn(call: types.CallbackQuery, state: FSMContext):
    admin_panel_adapter = AdminPanelAdapter()
    keyboard_data = await admin_panel_adapter.get_users_without_partner_as_buttons()
    keyboard_data = dict(reversed(keyboard_data.items()))
    await state.update_data(call=call)
    custom_keyboard = [InlineKeyboardButton(text='◀︎', callback_data='back_to_admin_menu_btn')]
    paginator = ButtonPagination(button_data=keyboard_data, amount_elements=6)
    await state.update_data(paginator=paginator)
    try:
        keyboard = paginator.pagination(custom_keyboard=custom_keyboard)
        await call.message.edit_text(text="<b>Клиенты без партнера:</b>", reply_markup=keyboard)
        await SG.users_without_partner.set()
    except KeyError:
        keyboard = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(text='◀️   Назад    ', callback_data='back_to_admin_menu_btn'))
        await call.message.edit_text(text="<b>Клиентов нет!</b>", reply_markup=keyboard)







# pagination handlers
async def partners_list_pagination(call: types.CallbackQuery, state: FSMContext):
    paginator = (await state.get_data()).get('paginator')
    keyboard = paginator.page_switch(call.data.split('#')[1])
    try:
        await call.message.edit_text(text="<b>Партнеры:</b>",
                                       reply_markup=keyboard)
        await state.update_data(paginator=paginator)
    except exceptions.MessageNotModified:
        await call.answer(text='Партнеров больше нет!', show_alert=True)



async def users_without_partner_pagination(call: types.CallbackQuery, state: FSMContext):
    paginator = (await state.get_data()).get('paginator')
    keyboard = paginator.page_switch(call.data.split('#')[1])
    try:
        await call.message.edit_text(text="<b>Клиенты без партнера:</b>",
                                       reply_markup=keyboard)
        await state.update_data(paginator=paginator)
    except exceptions.MessageNotModified:
        await call.answer(text='Клиентов больше нет!', show_alert=True)




def register_partners_panel_for_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(
        create_partner_final,
        state=SG.create_partner_final
    )
    dp.register_message_handler(
        change_partner_choose_partner,
        state=SG.change_partner_choose_partner
    )
    dp.register_callback_query_handler(
        partners_list_pagination,
        lambda callback_query: callback_query.data.split("#")[0] == 'amg',
        state=SG.partners_list_pagination
    )
    dp.register_callback_query_handler(
        view_detail_partner,
        lambda callback_query: callback_query.data.split("#")[1] == "partner_number",
        state=SG.partners_list_pagination,
    )
    dp.register_callback_query_handler(
        users_without_partner_pagination,
        lambda callback_query: callback_query.data.split("#")[0] == 'amg',
        state=SG.users_without_partner
    )
    dp.register_callback_query_handler(
        view_detail_user,
        lambda callback_query: callback_query.data.split("#")[1] == "user_number",
        state=SG.users_without_partner,
    )
    dp.register_callback_query_handler(
        partners_list_pagination,
        lambda callback_query: callback_query.data.split("#")[0] == 'amg',
        state=SG.change_partner_choose_partner
    )
    dp.register_callback_query_handler(
        change_partner_final,
        lambda callback_query: callback_query.data.split("#")[1] == "partner_number",
        state=SG.change_partner_choose_partner,
    )
    dp.register_callback_query_handler(
        partners_panel_for_admin_btn,
        lambda callback_query: callback_query.data == 'partners_panel_for_admin_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        create_partner_btn,
        lambda callback_query: callback_query.data == 'create_partner_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        view_detail_partner,
        lambda callback_query: callback_query.data == 'view_detail_partner',
        state='*'
    )
    dp.register_callback_query_handler(
        partner_list_for_admin_btn,
        lambda callback_query: callback_query.data == 'partner_list_for_admin_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        change_partner_btn,
        lambda callback_query: callback_query.data == 'change_partner_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        bank_contacts_btn,
        lambda callback_query: callback_query.data == 'bank_contacts_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        users_without_partner_list_btn,
        lambda callback_query: callback_query.data == 'users_without_partner_list_btn',
        state='*'
    )