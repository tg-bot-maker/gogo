import re

from aiogram import Dispatcher, types
from  aiogram.types.input_media import InputMediaPhoto
from aiogram.dispatcher import FSMContext

from handlers.states import SG
from models.adapters.base_adapter import BaseAdapter
from models.adapters.user_adapter import UserAdapter
from models.adapters.client_referral_system_adapter import ClientReferralSystemAdapter

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from configs import config

import asyncio

from APscheduler.notifications.partner_notifications import notify_partner_new_client
from APscheduler.notifications.client_notifications import notify_client_new_referral



async def greetings_btn(call: types.CallbackQuery, state: FSMContext, scheduler: AsyncIOScheduler):
    user_adapter = UserAdapter()
    await user_adapter.update_user_stage(user_id=call.from_user.id, user_stage="pick_product", call=call, scheduler=scheduler)
    await back_hendler_btn(call, state)


async def start_func(message: types.Message, state: FSMContext, scheduler: AsyncIOScheduler = None):
    await state.finish()
    try:
        manager_id = int(message.text.split(" ")[1])
        await notify_partner_new_client(message=message, partner_id=manager_id)
    except Exception as e:
        if type(e) == ValueError: #если не получается привести к int значит это клиентская партнерка
            manager_id = 0
            client_referral_id = int(message.text.split(" ")[1][:-3])
            client_referral_system_adapter = ClientReferralSystemAdapter()
            await client_referral_system_adapter.add_referral(client_user_id=message.from_user.id, client_referrer_id=client_referral_id)
            await notify_client_new_referral(message=message, client_id=client_referral_id)
        else:
            manager_id = 0
    base_adapter = BaseAdapter()
    keyboard = await base_adapter.start(
        user_id=message.from_user.id,
        user_name=message.from_user.username if message.from_user.username else "Пользователь",
        user_manager_id=manager_id,
        scheduler=scheduler,
        message=message
    )
    if base_adapter._msg == "greetings":
        text = """Добро пожаловать в <b>GoHome</b>.\n\n<b>GoHome</b> - это автоматизированый сервис по одобрению """ \
        """ипотеки, подбору недвижимости и юридическому сопровождению.\n\nНажмите кнопку что бы <b>начать</b> 👇"""

        with open("files/templates/house.jpg", "rb") as photo:
            await message.answer_photo(photo=photo, caption=text, reply_markup=keyboard)
    else:
        await message.answer(text=base_adapter._msg, reply_markup=keyboard)



async def back_hendler_btn(call: types.CallbackQuery, state: FSMContext, scheduler: AsyncIOScheduler = None):
    """ Кнопка выхода назад в главное меню"""
    await state.finish()
    base_adapter = BaseAdapter()
    keyboard = await base_adapter.start(user_id=call.from_user.id,
                                        user_name=call.message.from_user.username if call.message.from_user.username else "Anonymous",
                                        start_mode=False, scheduler=scheduler, message=call.message)
    if call.message.text:
        await call.message.edit_text(text=base_adapter.message_text, reply_markup=keyboard)
    else:
        try:
            await call.message.delete()
        except:
            pass
        await call.message.answer(text=base_adapter.message_text, reply_markup=keyboard)


async def help_handler(call: types.CallbackQuery, state: FSMContext):
    base_adapter = BaseAdapter()
    keyboard = await base_adapter.back_kb()
    await call.message.edit_text(text="При возникновении вопросов или сложностей в работе"
                                      " с ботом, напишите, пожалуйста: <b>@mr_b0ss7</b> \n\n"
                                      "Или позвоните по номеру: <code>+79660990054</code>", reply_markup=keyboard)


async def notifications_btn(call: types.CallbackQuery):
    user_adapter = UserAdapter()
    keyboard = await user_adapter.notifications_btn(call.from_user.id)
    await call.message.edit_text(text=user_adapter._msg, reply_markup=keyboard)


async def update_notifications_status(call: types.CallbackQuery):
    if call.data.split("#")[-1] == "True":
        new_status = True
    else:
        new_status = False
    user_adapter = UserAdapter()
    await user_adapter.update_notifications_status(call.from_user.id, new_status)
    await notifications_btn(call)


async def in_dev_alert(call: types.CallbackQuery, state: FSMContext):
    await call.answer(text="Эта функция в разработке 🛠", show_alert=True)



async def ill_go_on_later_btn(call: types.CallbackQuery):
    await call.message.edit_text("Хорошо 😉")
    await asyncio.sleep(1)
    await call.message.delete()


async def partner_menu_handler(call: types.CallbackQuery):
    base_adapter = BaseAdapter()
    keyboard = await base_adapter.partner_menu_kb()
    await call.message.edit_text(text="<b>Выберите действие:</b>", reply_markup=keyboard)

async def back_to_partner_menu_btn(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await partner_menu_handler(call)



async def admin_panel_btn(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    base_adapter = BaseAdapter()
    keyboard = await base_adapter.admin_menu_kb()
    await call.message.edit_text(text="<b>Выберите действие:</b>", reply_markup=keyboard)

async def back_to_admin_menu_btn(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    if call.from_user.id in config.admins:
        await admin_panel_btn(call, state)
    else:
        await partner_menu_handler(call)



#registration
async def registration_btn(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_caption("Введите ваш номер телефона:")
    await state.update_data(call=call)
    await SG.reg_final.set()


async def reg_final(message: types.Message, state: FSMContext, scheduler: AsyncIOScheduler):
    data = await state.get_data()
    call = data.get("call")
    number = message.text
    user_id = message.from_user.id
    await message.delete()
    if str(number).isnumeric():
        user_adapter = UserAdapter()
        await user_adapter.set_user_fio_and_number(user_id, number)
        await call.message.edit_caption("Вы успешно зарегистрированы! ✅")
        await asyncio.sleep(1)
        await state.finish()
        await greetings_btn(call, state, scheduler)
    else:
        await call.message.edit_caption("<i>Ваш номер может содержать только цифры!</i>\nВведите ваш номер:")
        await SG.reg_final.set()






#########################################
def register_base_handlers(dp: Dispatcher):
    dp.register_message_handler(
        reg_final,
        state=SG.reg_final
    )
    dp.register_message_handler(
        start_func,
        commands='start',
        state='*'
    )
    dp.register_callback_query_handler(
        back_hendler_btn,
        lambda callback_query: callback_query.data == 'go_back_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        back_to_partner_menu_btn,
        lambda callback_query: callback_query.data == 'back_to_partner_menu_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        partner_menu_handler,
        lambda callback_query: callback_query.data == 'partner_menu_handler',
        state='*'
    )
    dp.register_callback_query_handler(
        help_handler,
        lambda callback_query: callback_query.data == 'help_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        greetings_btn,
        lambda callback_query: callback_query.data == 'greetings_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        notifications_btn,
        lambda callback_query: callback_query.data == 'notifications_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        ill_go_on_later_btn,
        lambda callback_query: callback_query.data == 'ill_go_on_later_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        admin_panel_btn,
        lambda callback_query: callback_query.data == 'admin_panel_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        back_to_admin_menu_btn,
        lambda callback_query: callback_query.data == 'back_to_admin_menu_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        registration_btn,
        lambda callback_query: callback_query.data == 'registration_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        update_notifications_status,
        lambda callback_query: callback_query.data.split("#")[0] == 'update_notifications_status',
        state='*'
    )
    dp.register_callback_query_handler(
        in_dev_alert,
        lambda callback_query: callback_query.data in ['legal_services_btn', 'finances_btn'],
        state='*'
    )




