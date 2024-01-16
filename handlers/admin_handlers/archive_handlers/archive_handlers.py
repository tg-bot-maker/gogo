from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from handlers.states import SG
from models.adapters.base_adapter import BaseAdapter
from models.adapters.user_archive_adapter import UserArchiveAdapter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pagination.MagicPaginator import ButtonPagination
from aiogram.utils import exceptions


async def archive_btn(call: types.CallbackQuery, state: FSMContext):
    user_archive_adapter = UserArchiveAdapter()
    keyboard = await user_archive_adapter.archive_btn()
    await call.message.edit_text(text=user_archive_adapter._msg, reply_markup=keyboard)


async def back_to_archive_btn(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await archive_btn(call, state)


async def archive_clients_btn(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(call=call)
    user_archive_adapter = UserArchiveAdapter()
    keyboard_data = await user_archive_adapter.get_users_in_archive_as_buttons()
    custom_keyboard = [InlineKeyboardButton(text='◀︎', callback_data='back_to_archive_btn')]
    paginator = ButtonPagination(button_data=keyboard_data, amount_elements=5)
    await state.update_data(paginator=paginator)
    try:
        keyboard = paginator.pagination(custom_keyboard=custom_keyboard)
        await call.message.edit_text(text="<b>Клиенты в архиве:</b>", reply_markup=keyboard)
        await SG.archive_users_list_pagination.set()
    except KeyError:
        await call.message.edit_text(text="<b>Клиентов в архиве пока нет!</b>",
                                     reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='◀️   Назад    ', callback_data='back_to_archive_btn')))



async def view_detail_archive_user(call: types.CallbackQuery, state: FSMContext):
    client_id = call.data.split("#")[-1]
    user_archive_adapter = UserArchiveAdapter()
    client_archive = await user_archive_adapter.get_user_archive(client_id)
    keyboard = await user_archive_adapter.view_detail_archive_user(client_archive)
    await call.message.edit_text(text=user_archive_adapter._msg, reply_markup=keyboard)











# pagination handler
async def archive_users_list_pagination(call: types.CallbackQuery, state: FSMContext):
    paginator = (await state.get_data()).get('paginator')
    keyboard = paginator.page_switch(call.data.split('#')[1])
    try:
        await call.message.edit_text(text="<b>Клиенты в архиве:</b>",
                                       reply_markup=keyboard)
        await state.update_data(paginator=paginator)
    except exceptions.MessageNotModified:
        await call.answer(text='Клиентов больше нет!', show_alert=True)






def register_archive_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        archive_btn,
        lambda callback_query: callback_query.data == 'archive_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        archive_clients_btn,
        lambda callback_query: callback_query.data == 'archive_clients_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        back_to_archive_btn,
        lambda callback_query: callback_query.data == 'back_to_archive_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        archive_users_list_pagination,
        lambda callback_query: callback_query.data.split("#")[0] == 'amg',
        state=SG.archive_users_list_pagination
    )
    dp.register_callback_query_handler(
        view_detail_archive_user,
        lambda callback_query: callback_query.data.split("#")[1] == "user_number",
        state=SG.archive_users_list_pagination,
    )