from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from models.adapters.form_adapter import FormAdapter
from handlers.states import SG
from handlers.base_handlers import back_hendler_btn
from models.adapters.user_adapter import UserAdapter
from models.adapters.base_adapter import BaseAdapter
from models.adapters.client_panel_adapter import ClientPanelAdapter
from handlers.client_handlers.form_handlers.fill_form_handlers import form_question_0

async def in_dev(call: types.CallbackQuery, state: FSMContext):
    await call.answer(text="Эта функция в разработке 🛠", show_alert=True)


async def not_yet(call: types.CallbackQuery, state: FSMContext):
    await call.answer(text="Вы пока не завершили процесс получения ипотеки!", show_alert=True)


async def personal_panel_btn(call: types.CallbackQuery):
    client_panel_adapter = ClientPanelAdapter()
    user_adapter = UserAdapter()
    client_obj = await user_adapter.get_user(call.from_user.id)
    keyboard = await client_panel_adapter.client_panel_btn(client_obj)
    await call.message.edit_text(text=client_panel_adapter._msg, reply_markup=keyboard)


async def my_form_btn(call: types.CallbackQuery):
    client_id = call.data.split("#")[-1]
    client_panel_adapter = ClientPanelAdapter()
    form_adapter = FormAdapter()
    form_obj = await form_adapter.get_form(client_id)
    if form_obj:
        keyboard = await client_panel_adapter.my_form_btn(form_obj)
        await call.message.edit_text(text=client_panel_adapter._msg, reply_markup=keyboard)
    else:
        await call.answer(text="Вы пока не заполнили анкету!", show_alert=True)


async def change_my_form_btn(call: types.CallbackQuery, state: FSMContext):
    await form_question_0(call, state, updating_form=True)




def register_client_panel_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        personal_panel_btn,
        lambda callback_query: callback_query.data in ["personal_panel_btn","back_to_client_panel_btn"],
        state='*'
    )
    dp.register_callback_query_handler(
        my_form_btn,
        lambda callback_query: callback_query.data.split("#")[0] == 'my_form_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        change_my_form_btn,
        lambda callback_query: callback_query.data.split("#")[0] == 'change_my_form_btn',
        state='*'
    )



    dp.register_callback_query_handler(
        not_yet,
        lambda callback_query: callback_query.data.split("#")[0] == 'my_mortgage_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        in_dev,
        lambda callback_query: callback_query.data.split("#")[0] == 'my_insurance_btn',
        state='*'
    )