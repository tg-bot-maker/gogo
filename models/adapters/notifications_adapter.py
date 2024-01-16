from aiogram.types import InlineKeyboardMarkup
from typing import Optional
from database.db import session_factory
from models.controls.user_controls import UserControl





class NotificationsAdapter:
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

    async def update_client_step_help_notification_job_id(self, user_id, job_id):
        with session_factory() as session:
            user_control = UserControl(session)
            user = await user_control.get(user_id)
            user.client_step_help_notification_job_id = job_id
            session.commit()

        return True


    async def update_client_step_help_notification_status(self, user_id, status):
        with session_factory() as session:
            user_control = UserControl(session)
            user = await user_control.get(user_id)
            user.client_step_help_notification_status = status
            session.commit()

        return True


    async def check_notifications_status(self, user_id):
        with session_factory() as session:
            user_control = UserControl(session)
            user = await user_control.get(user_id)
            if user:
                if user.user_notifications_status:
                    return True
                else:
                    return False
            else:
                raise Exception("User to notify not found")
