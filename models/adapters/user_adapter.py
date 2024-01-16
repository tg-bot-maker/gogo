from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import Optional
from database.db import session_factory
from models.controls.user_controls import UserControl


from APscheduler.notifications.partner_notifications import notify_partner_client_new_step
from APscheduler.notifications.client_notifications import notify_client

class UserAdapter:
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


    async def notifications_btn(self, user_id):
        with session_factory() as session:
            user_control = UserControl(session)
            user = await user_control.get(user_id)
            session.commit()
        if user.user_notifications_status == True:
            self._msg = "<b>Уведомления включены  ✅</b>"
            keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('Отключить 🚫', callback_data='update_notifications_status#False'))
        else:
            self._msg = "<b>Уведомления отключены  🚫</b>"
            keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('Включить ✅', callback_data='update_notifications_status#True'))

        return keyboard.add(InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_partner_menu_btn'))



    async def set_user_fio_and_number(self, user_id, number):
        with session_factory() as session:
            user_control = UserControl(session)
            user = await user_control.get(user_id)
            user.user_number = number
            session.commit()
        return user


    async def get_user(self, user_id: int):
        with session_factory() as session:
            user_control = UserControl(session)
            user = await user_control.get(user_id)
            session.commit()
        return user


    async def update_notifications_status(self, user_id, new_status):
        with session_factory() as session:
            user_control = UserControl(session)
            user = await user_control.get(user_id)
            user.user_notifications_status = new_status
            session.commit()


    async def get_user_stage(self, user_id):
        with session_factory() as session:
            user_control = UserControl(session)
            user = await user_control.get(user_id)
            session.commit()
        return user.user_stage



    async def get_user_name(self, user_id):
        with session_factory() as session:
            user_control = UserControl(session)
            user = await user_control.get(user_id)
            session.commit()
        return user.user_name


    async def update_user_stage(self, user_id, user_stage, call, scheduler):
        user = await self.get_user(user_id)

        # Получаю job_id уведомления о переходе на новый этап
        job_id = user.client_step_help_notification_job_id
        # Если уведомление не было отправлено и job_id (задача) уже была создана, то удаляю задачу из scheduler
        if user.client_step_help_notification_status is False and job_id != 0:
            try:
                scheduler.remove_job(job_id)
            except Exception as e:
                pass
        # Ставлю новую задачу на отправку уведомления
        await notify_client(user_id, call, scheduler)

        with session_factory() as session:
            user_control = UserControl(session)
            user = await user_control.get(user_id)

            if user.user_manager_id != 0000000000:
                await notify_partner_client_new_step(user, user_stage, call)

            await user_control.update_stage(user_id, user_stage)
            session.commit()


    async def get_user_who_paid_as_buttons(self):
        with session_factory() as session:
            user_control = UserControl(session)
            users_who_paid = await user_control.get_users_who_paid()
            session.commit()
        buttons: dict = {}
        for client in users_who_paid:
            if client.user_fio != "Аноним":
                name = client.user_fio
            else:
                name = client.user_name
            buttons[f"user_number#{client.user_id}"] = name

        return buttons



    async def get_user_who_paid_for_partner_as_buttons(self, partner_id):
        with session_factory() as session:
            user_control = UserControl(session)
            users_who_paid = await user_control.get_users_who_paid_for_partner(partner_id)
            session.commit()
        buttons: dict = {}
        for client in users_who_paid:
            if client.user_fio != "Аноним":
                name = client.user_fio
            else:
                name = client.user_name
            buttons[f"user_number#{client.user_id}"] = name

        return buttons





