from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Optional





class MeetingsAdapter:
    def __init__(self, user_id: Optional[int] = None):
        self._user_id = user_id
        self._inline_keyboard = InlineKeyboardMarkup()
        self._msg = ''

    @property
    def inline_keyboard(self) -> InlineKeyboardMarkup:
        return self._inline_keyboard

    @property
    def message_text(self) -> str:
        return self._msg


    async def meetings_btn(self):
        self._msg = '<b>Выберите функцию:</b>'
        self._inline_keyboard = InlineKeyboardMarkup()\
            .add(InlineKeyboardButton(text="Календарь встреч  🗓", url="https://calendar.google.com/")) \
            .add(InlineKeyboardButton(text="Шаблоны сообщений  📎", callback_data="meetings_message_templates_btn")) \
            .add(InlineKeyboardButton(text="◀️   Назад    ", callback_data="back_to_partner_menu_btn"))
        return self._inline_keyboard


    async def meetings_message_templates_btn(self):
        self._msg = '<b>Выберите шаблон сообщения:</b>'
        self._inline_keyboard = InlineKeyboardMarkup()\
            .add(InlineKeyboardButton(text="📍 Напоминание о встрече", callback_data="meeting_reminder_template_btn")) \
            .add(InlineKeyboardButton(text="📍 Список документов", callback_data="meeting_dox_list_template_btn")) \
            .add(InlineKeyboardButton(text="◀️   Назад    ", callback_data="meetings_btn"))
        return self._inline_keyboard

"""
    async def update_client_step_help_notification_job_id(self, user_id, job_id):
        with session_factory() as session:
            user_control = UserControl(session)
            user = await user_control.get(user_id)
            user.client_step_help_notification_job_id = job_id
            session.commit()

        return True"""