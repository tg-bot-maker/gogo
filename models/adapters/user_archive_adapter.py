import datetime

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Optional
from database.db import session_factory
from models.controls.user_archive_controls import UserArchiveControl




class UserArchiveAdapter:
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


    #buttons
    async def archive_btn(self):
        self._msg = '<b>Вы находитесь в архиве 🗄</b>\n\n' \
                    'В архив попадают клиенты, которым были успешно оказаны услуги' \
                    ' или клиенты, которые обратились, но до оказания услуги не дошли.'
        keyboard = InlineKeyboardMarkup().add(
             InlineKeyboardButton('Список клиентов 📋', callback_data='archive_clients_btn')) \
            .add(InlineKeyboardButton('Внести клиента ➕', callback_data='add_client_to_archive_btn')) \
            .add(InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_admin_menu_btn'))
        return keyboard



    async def view_detail_archive_user(self, client_archive):
        emoji_dict = {True:" ✅", False: "🚫"}
        service_dict = {True: "Услуга оказана", False: "Услуга не оказана"}
        if not client_archive.last_check_date:
            last_check_date = "Не проверялся"
        else:
            last_check_date = client_archive.last_check_date
        self._msg = f'ФИО: {client_archive.user_fio}\n' \
                    f'Номер: {client_archive.user_number}\n' \
                    f'Дата последней проверки: {last_check_date}\n' \
                    f'Статус: {service_dict[client_archive.user_status]}\n' \
                    f'Добавлен вручную: {emoji_dict[client_archive.user_added_manually]}\n\n' \
                    f'Пометка: {client_archive.mark_from_partner}'
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_archive_btn'))
        return keyboard


    async def back_to_archive_kb(self):
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_archive_btn'))
        return keyboard


    async def add_to_archive_btn(self):
        self._msg = '<b>Для добавления клиента в архив вам необходимо записать ФИО и номер ' \
                    'телефона клиента. Так же при необходимости вы можете оставить пометку о клиенте.</b>\n\n' \
                    'Введите ФИО клиента:'
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_archive_btn'))
        return keyboard


    async def add_to_archive_get_fio(self):
        self._msg = 'Введите номер телефона клиента:'
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_archive_btn'))
        return keyboard

    async def add_to_archive_get_number(self):
        self._msg = 'Введите короткую пометку о клиенте:'
        keyboard = InlineKeyboardMarkup().add(
                InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_archive_btn'))
        return keyboard


    async def add_to_archive_get_mark(self):
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton('Добавить в архив ✅', callback_data='add_to_archive_final')) \
            .add(InlineKeyboardButton('Отменить 🚫', callback_data='back_to_archive_btn'))
        return keyboard




    async def add_user_to_archive(self, user_id, user_fio, user_number,
                                  user_added_manually, user_status, mark_from_partner):
        with session_factory() as session:
            user_archive_control = UserArchiveControl(session)
            await user_archive_control.add(user_id, user_fio, user_number,
                                           user_added_manually, user_status, mark_from_partner)
            session.commit()


    async def get_user_archive(self, user_id):
        with session_factory() as session:
            user_archive_control = UserArchiveControl(session)
            user_archive = await user_archive_control.get(user_id)
            session.commit()
        return user_archive


    async def update_last_check(self, user_id, mark):
        with session_factory() as session:
            user_archive_control = UserArchiveControl(session)
            user_archive = await user_archive_control.get(user_id)
            user_archive.last_check_date = datetime.datetime.now()
            if mark != "":
                user_archive.mark_from_partner += f"\n\n{mark}"
            session.commit()


    async def get_users_in_archive_as_buttons(self):
        with session_factory() as session:
            user_archive_control = UserArchiveControl(session)
            users = await user_archive_control.get_all()
            session.commit()
        buttons: dict = {}
        for user in users:
            buttons[f"user_number#{user.user_id}"] = user.user_fio

        return buttons