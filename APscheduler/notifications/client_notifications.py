from configs.config import client_step_help_notification_delay
from aiogram import types
from datetime import datetime, timedelta

from models.adapters.notifications_adapter import NotificationsAdapter


check_notifications_status = NotificationsAdapter().check_notifications_status



async def notify_client(user_id, call, scheduler):
    """ Уведомление для клиента"""
    job = scheduler.add_job(client_step_help_notification, 'date', run_date=datetime.now() + timedelta(seconds=client_step_help_notification_delay),
                      args=[user_id, call])

    notifications_adapter = NotificationsAdapter()
    await notifications_adapter.update_client_step_help_notification_status(user_id=user_id, status=False)
    await notifications_adapter.update_client_step_help_notification_job_id(user_id=user_id, job_id=job.id)




async def client_step_help_notification(user_id, call):
    """ Уведомление для клиента с предложением помощи в переходе на следующий этап"""
    keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text="Нужна помощь 🙋‍♂", callback_data="help_btn")) \
        .add(types.InlineKeyboardButton(text="Продолжу позже 👌", callback_data="ill_go_on_later_btn"))

    await call.bot.send_message(chat_id=int(user_id), text="Если у вас возникли сложности"
                                " и не получается перейти к следующему этапу, нажмите на"
                                " кнопку <b>Нужна помощь 👇</b> \n\n<b>Мы обязательно вам поможем!</b>", reply_markup=keyboard)
    notifications_adapter = NotificationsAdapter()
    await notifications_adapter.update_client_step_help_notification_status(user_id=user_id, status=True)



async def notify_client_new_referral(message: types.Message, client_id):
    """ Уведомление для клиента о том что у него новый реферал"""
    text = "<b>Уведомление 🔔</b>\n" \
           f"Пользователь @{message.from_user.username} перешел по вашей реферальной ссылке!"
    if await check_notifications_status(client_id):
        await message.bot.send_message(chat_id=client_id, text=text)