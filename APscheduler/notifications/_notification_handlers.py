from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils import exceptions
from models.adapters.partners_adapter import PartnersAdapter
from aiogram.types import InlineKeyboardButton
from pagination.MagicPaginator import ButtonPagination
from handlers.states import SG

import asyncio





async def assign_manager_btn(call: types.CallbackQuery, state: FSMContext):
    partner_adapter = PartnersAdapter()
    keyboard_data = await partner_adapter.get_partners_list_as_buttons()
    keyboard_data = dict(reversed(keyboard_data.items()))
    custom_keyboard = [InlineKeyboardButton(text='Назначить позже', callback_data='go_back_btn')]
    paginator = ButtonPagination(button_data=keyboard_data, amount_elements=6)
    await state.update_data(paginator=paginator)
    await state.update_data(client_id=call.data.split("#")[1])
    try:
        keyboard = paginator.pagination(custom_keyboard=custom_keyboard)
        await call.message.edit_text(text="<b>Выберите партнера:</b>", reply_markup=keyboard)
        await SG.partners_pagination.set()
    except KeyError:
        keyboard = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(text='◀️   В меню    ', callback_data='go_back_btn'))
        await call.message.edit_text(text="<b>Партнеров пока нет!</b>", reply_markup=keyboard)


async def assign_manager_final(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    client_id = data.get("client_id")
    partner_id = int(call.data.split("#")[-1])
    partner_adapter = PartnersAdapter()
    await partner_adapter.change_partner(client_id, partner_id)

    keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text='◀️   В меню    ', callback_data='go_back_btn'))
    await call.message.edit_text(text="Менеджер назначен!", reply_markup=keyboard)



async def assign_manager_later_btn(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Хорошо 😉")
    await asyncio.sleep(1)
    await call.message.delete()
    await state.finish()









#pagination_handler
async def partners_pagination(call: types.CallbackQuery, state: FSMContext):
    paginator = (await state.get_data()).get('paginator')
    keyboard = paginator.page_switch(call.data.split('#')[1])
    try:
        await call.message.edit_text(text="<b>Выберите партнера:</b>",
                                       reply_markup=keyboard)
        await state.update_data(paginator=paginator)
    except exceptions.MessageNotModified:
        await call.answer(text='Больше нет партнеров!', show_alert=True)



def register_notifications_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        assign_manager_btn,
        lambda callback_query: callback_query.data.split("#")[0] == 'assign_manager_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        assign_manager_later_btn,
        lambda callback_query: callback_query.data == 'assign_manager_later_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        partners_pagination,
        lambda callback_query: callback_query.data.split("#")[0] == 'amg',
        state=SG.partners_pagination
    )
    dp.register_callback_query_handler(
        assign_manager_final,
        lambda callback_query: callback_query.data.split("#")[1] == "partner_number",
        state=SG.partners_pagination,
    )