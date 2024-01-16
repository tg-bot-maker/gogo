from aiogram import types
from configs import config

from models.adapters.user_adapter import UserAdapter


async def start_command_sent(message: types.Message, user_manager_id: int):
    """ Уведомление админам о новом пользователе в боте"""
    for admin_id in config.admins:
        user_adapter = UserAdapter()
        admin_user_object = await user_adapter.get_user(admin_id)
        if admin_user_object:
            if admin_user_object.user_notifications_status:
                text = "<b>Уведомление 🔔</b>\n" \
                       f"В боте новый пользователь:\n\n" \
                       f"<i>Имя</i>  -  <b>{message.from_user.first_name}</b> "
                if message.from_user.last_name:
                    text += f"<b>{message.from_user.last_name}</b>"
                if message.from_user.username:
                    text += f"\n<i>Username</i>  -  <b>@{message.from_user.username}</b>"

                # Назначение менеджера если его нет
                if user_manager_id != 0:
                    user_manager = await user_adapter.get_user(user_manager_id)
                    text += f"\n<i>Менеджер</i>  -  <b>@{user_manager.user_name}</b>"
                    await message.bot.send_message(chat_id=admin_id, text=text)
                else:
                    text += f"\n\n<b>Менеджера нет!</b>"
                    keyboard = types.InlineKeyboardMarkup()\
                        .add(types.InlineKeyboardButton(text="Назначить менеджера", callback_data=f"assign_manager_btn#{message.from_user.id}")) \
                        .add(types.InlineKeyboardButton(text="Позже", callback_data="assign_manager_later_btn"))
                    await message.bot.send_message(chat_id=admin_id, text=text, reply_markup=keyboard)




