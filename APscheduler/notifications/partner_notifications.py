from aiogram import types
from configs.config import stages

from models.adapters.notifications_adapter import NotificationsAdapter

check_notifications_status = NotificationsAdapter().check_notifications_status


async def notify_partner_assigned(message: types.Message, partner_id):
    """ Уведомление для партнера о том что он назначен партнером"""
    text = "<b>Уведомление 🔔</b>\n" \
           f"Вы были назначены партнером! 🎉"
    if await check_notifications_status(partner_id):
        await message.bot.send_message(chat_id=partner_id, text=text)


async def notify_partner_new_client(message: types.Message, partner_id):
    """ Уведомление для партнера о том что у него новый клиент"""
    text = "<b>Уведомление 🔔</b>\n" \
           f"Пользователь @{message.from_user.username} перешел по вашей реферальной ссылке!"
    if await check_notifications_status(partner_id):
        await message.bot.send_message(chat_id=partner_id, text=text)



async def notify_partner_client_new_step(user, step, call):
    """ Уведомление для партнера о том что клиент перешел на новый этап"""
    text = "<b>Уведомление 🔔</b>\n" \
             f"Пользователь @{user.user_name} перешел на этап <b>{stages[step]}</b>!"
    if await check_notifications_status(user.user_manager_id):
        await call.bot.send_message(chat_id=user.user_manager_id, text=text)
