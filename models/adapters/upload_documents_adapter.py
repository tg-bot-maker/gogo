from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Optional
from database.db import session_factory
from models.adapters.admin_panel_adapter import AdminPanelAdapter
from models.adapters.user_adapter import UserAdapter
from models.controls.form_control import UserFormControl
from models.controls.user_controls import UserControl
from models.controls.user_documents_control import UserDocumentsControl



class UploadDocumentsAdapter:
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


    async def get_drive_link(self, user_id):
        with session_factory() as session:
            user_documents_control = UserDocumentsControl(session)
            user_documents = await user_documents_control.get(user_id)
            session.commit()
        return user_documents.user_documents_drive_folder_link


    async def write_drive_link_to_db(self, user_id, drive_link):
        with session_factory() as session:
            user_documents_control = UserDocumentsControl(session)
            user_documents = await user_documents_control.get(user_id)
            user_documents.user_documents_drive_folder_link = drive_link
            session.commit()

    async def upload_documents_btn(self, user_id):
        upload_documents_adapter = UploadDocumentsAdapter()
        was_uploaded = await upload_documents_adapter.was_uploaded(user_id)
        with session_factory() as session:
            form_control = UserFormControl(session)
            user_form = await form_control.get(user_id)
            user_citizenship = user_form.citizenship
            session.commit()

        self._msg = "<b>📄    Загрузите cледующие документы:</b>"
        if was_uploaded is False and user_citizenship == "ru":
            keyboard = InlineKeyboardMarkup().add(
                InlineKeyboardButton('Паспорт', callback_data='upload_documents_passport_btn')) \
                .add(InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_btn'))
        elif was_uploaded is not False and user_citizenship == "ru":
            keyboard = InlineKeyboardMarkup().add(
                InlineKeyboardButton('СНИЛС', callback_data='upload_documents_snils_btn')) \
                .add(InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_btn'))
        else:
            keyboard = InlineKeyboardMarkup().add(
                InlineKeyboardButton('Паспорт', callback_data='upload_documents_passport_btn')) \
                .add(InlineKeyboardButton('СНИЛС', callback_data='upload_documents_snils_btn')) \
                .add(InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_btn'))
        """
        else:
            keyboard = InlineKeyboardMarkup().add(
                InlineKeyboardButton('Паспорт вашей страны', callback_data='upload_documents_passport_btn')) \
                .add(InlineKeyboardButton('СНИЛС', callback_data='upload_documents_snils_btn')) \
                .add(InlineKeyboardButton('Нотариальный перевод', callback_data='in_dev')) \
                .add(InlineKeyboardButton('Копия трудовой', callback_data='in_dev')) \
                .add(InlineKeyboardButton('Справка о доходе', callback_data='in_dev')) \
                .add(InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_btn'))
"""
        return keyboard


    async def upload_documents_passport_btn(self, page_number):
        self._msg = "<b>📄    Вам нужно загрузить фото 2-3 и 4-5 страниц паспорта.</b>\n\n" \
                    "<i> Для сброса и отмены действия вы можете отправить команду /start </i>\n\n" \
                    f"<b>Отправьте, пожалуйста, фото {page_number} страниц паспорта:</b>"

        return self._msg


    async def upload_passport(self, user_documents_user_id, user_documents_passport23,
                              user_documents_passport45):
        with session_factory() as session:
            user_documents_control = UserDocumentsControl(session)
            user_documents = await user_documents_control.get(user_documents_user_id)
            user_documents.user_documents_passport23 = user_documents_passport23
            user_documents.user_documents_passport45 = user_documents_passport45

            if await self.snils_was_uploaded(user_documents_user_id):
                user_control = UserControl(session)
                await user_control.update_stage(user_documents_user_id, "prepare_contract")
            session.commit()
        return True


    async def was_uploaded(self, user_documents_user_id):
        with session_factory() as session:
            user_documents_control = UserDocumentsControl(session)
            user_documents = await user_documents_control.get(user_documents_user_id)
            session.commit()

        if user_documents.user_documents_passport45:
            return "Паспорт был загружен!", InlineKeyboardMarkup().add(
                InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_upload_documents_btn'))
        else:
            return False


    async def snils_was_uploaded(self, user_documents_user_id):
        with session_factory() as session:
            user_documents_control = UserDocumentsControl(session)
            user_documents = await user_documents_control.get(user_documents_user_id)
            session.commit()

        if user_documents.user_documents_snils:
            return "<b>СНИЛС был загружен!\n\nТеперь вы можете перейти к следующему этапу 👇</b>", InlineKeyboardMarkup().add(
                InlineKeyboardButton('   Перейти    ', callback_data='go_back_btn'))
        else:
            return False


    async def upload_snils_btn(self):
        self._msg = "<b>Паспорт был успешно загружен.\n\n📄    Загрузите фото СНИЛС:</b>"
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_upload_documents_btn'))
        return self._msg, keyboard


    async def upload_snils(self, user_documents_user_id, user_documents_snils,  call, scheduler):
        with session_factory() as session:
            user_documents_control = UserDocumentsControl(session)
            user_documents = await user_documents_control.get(user_documents_user_id)
            user_documents.user_documents_snils = user_documents_snils

            if await self.was_uploaded(user_documents_user_id):
                user_id = user_documents_user_id
                user_control = UserControl(session)
                admin_panel_adapter = AdminPanelAdapter()
                user_adapter = UserAdapter()
                if await admin_panel_adapter.get_user_contract(user_id):
                    await user_adapter.update_user_stage(user_id, "contract_ready", call, scheduler)
                else:
                    await user_adapter.update_user_stage(user_id, "prepare_contract", call, scheduler)
                #await user_control.update_stage(user_documents_user_id, "pick_product")

            session.commit()
        return True


