import random

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from models.adapters.base_adapter import BaseAdapter
from models.adapters.partners_adapter import PartnersAdapter




async def control_client_btn(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    client_id = data.get("user_id")
    partners_adapter = PartnersAdapter()
    keyboard = await partners_adapter.control_client_btn(client_id)
    await call.message.edit_text(text=partners_adapter._msg, reply_markup=keyboard)


async def move_client_to_buy_estate_btn(call: types.CallbackQuery, state: FSMContext):
    client_id = call.data.split("#")[-1]
    partners_adapter = PartnersAdapter()
    keyboard = await partners_adapter.move_client_to_buy_estate_btn(client_id)
    await call.message.edit_text(text=partners_adapter._msg, reply_markup=keyboard)


async def move_client_to_sell_estate_btn(call: types.CallbackQuery, state: FSMContext):
    client_id = call.data.split("#")[-1]
    partners_adapter = PartnersAdapter()
    keyboard = await partners_adapter.move_client_to_sell_estate_btn(client_id)
    await call.message.edit_text(text=partners_adapter._msg, reply_markup=keyboard)


async def send_decision_to_client_btn(call: types.CallbackQuery, state: FSMContext):
    client_id = call.data.split("#")[-1]
    partners_adapter = PartnersAdapter()
    keyboard = await partners_adapter.send_decision_to_client_btn(client_id)
    await call.message.edit_text(text=partners_adapter._msg, reply_markup=keyboard)


async def send_mortgage_result(call: types.CallbackQuery, state: FSMContext):
    client_id = call.data.split("#")[-1]
    result = call.data.split("#")[1]
    partners_adapter = PartnersAdapter()
    keyboard = await partners_adapter.send_mortgage_result(bool(result), int(client_id))
    await call.message.edit_text(text=partners_adapter._msg, reply_markup=keyboard)



async def restart_client_btn(call: types.CallbackQuery, state: FSMContext):
    base_adapter = BaseAdapter()
    keyboard = await base_adapter.back_kb()
    user_id = call.data.split("#")[-1]
    partners_adapter = PartnersAdapter()
    await partners_adapter.restart_partner_for_testing(user_id)
    await call.message.edit_text(text="Сброс клиента успешно произведен!", reply_markup=keyboard)



def register_control_client_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        control_client_btn,
        lambda callback_query: callback_query.data == 'control_client_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        move_client_to_buy_estate_btn,
        lambda callback_query: callback_query.data.split("#")[0] == 'move_client_to_buy_estate_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        move_client_to_sell_estate_btn,
        lambda callback_query: callback_query.data.split("#")[0] == 'move_client_to_sell_estate_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        send_mortgage_result,
        lambda callback_query: callback_query.data.split("#")[0] == 'send_mortgage_result',
        state='*'
    )
    dp.register_callback_query_handler(
        restart_client_btn,
        lambda callback_query: callback_query.data.split("#")[0] == 'restart_client_btn',
        state='*'
    )