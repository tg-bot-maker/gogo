from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Optional
from database.db import session_factory
from models.controls.user_controls import UserControl
from models.controls.history_control import CreditHistoryControl
from models.controls.user_documents_control import UserDocumentsControl
from models.controls.form_control import UserFormControl
from models.controls.contract_controls import ContractControl
from models.controls.payments_control import PaymentsControl




class PartnersAdapter:
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




    async def analytics_for_partner_kb(self, form_status: bool, restart_func = False):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Управление', callback_data='control_client_btn'))
        if restart_func:
            keyboard.add(InlineKeyboardButton('Сбросить ♻️', callback_data='restart_partner_for_testing_btn'))
        if form_status:
            keyboard.add(InlineKeyboardButton('Посмотреть анкету', callback_data='show_form_for_partner'))
        return keyboard.add(InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_to_my_clients_btn'))


    async def control_client_btn(self, client_id: int):
        self._msg = "<b>Выберите действие:</b>"
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Перевести на покупку недвижимости', callback_data=f'move_client_to_buy_estate_btn#{client_id}'))
        keyboard.add(InlineKeyboardButton('Перевести на продажу недвижимости', callback_data=f'move_client_to_sell_estate_btn#{client_id}'))
        keyboard.add(InlineKeyboardButton('Сбросить клиента в начало ♻️', callback_data=f'restart_client_btn#{client_id}'))

        with session_factory() as session:
            user_control = UserControl(session)
            client = await user_control.get(client_id)
            if client.user_stage == "payment_approved":
                keyboard.add(InlineKeyboardButton('Отправить решение по ипотеке', callback_data=f'send_decision_to_client_btn#{client_id}'))
            session.commit()

        return keyboard.add(InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_to_my_clients_btn'))


    async def make_partner(self, user_id: int):
        with session_factory() as session:
            user_control = UserControl(session)
            user = await user_control.get(user_id)
            user.is_partner = True
            user.user_manager_id = user_id
            session.commit()
        return True


    async def view_detail_partner(self, partner_id):
        with session_factory() as session:
            user_control = UserControl(session)
            partner = await user_control.get(partner_id)
            session.commit()
        if partner.user_fio != "Аноним":
            name = partner.user_fio
        else:
            name = partner.user_name
        clients_amount = await self.get_partner_clients(partner_id)
        self._msg = f"<b>{name}</b>\n\n" \
                    f"Количество клиентов: <b>{len(clients_amount)}</b>"
        return InlineKeyboardMarkup().add(InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_admin_menu_btn'))



    async def get_partners_list_as_buttons(self):
        with session_factory() as session:
            user_control = UserControl(session)
            partners_list = await user_control.get_partners_list()
            session.commit()
        buttons: dict = {}
        for partner in partners_list:
            if partner.user_fio == "Аноним":
                name = f"TG: {partner.user_name}"
            else:
                name = partner.user_fio
            buttons[f"partner_number#{partner.user_id}"] = name

        return buttons


    async def get_partner_clietns_as_buttons(self, partner_id):
        with session_factory() as session:
            user_control = UserControl(session)
            partner_clients_list = await user_control.get_partner_clients(partner_id)
            session.commit()
        buttons: dict = {}
        for client in partner_clients_list:
            if client.user_fio == "Аноним":
                name = f"TG: {client.user_name}"
            else:
                name = client.user_fio
            buttons[f"partner_number#{client.user_id}"] = name

        return buttons



    async def get_partner_clients(self, partner_id):
        with session_factory() as session:
            user_control = UserControl(session)
            partner_clients = await user_control.get_partner_clients(partner_id)
            session.commit()
        return partner_clients


    async def change_partner(self, user_id, partner_id):
        with session_factory() as session:
            user_control = UserControl(session)
            user = await user_control.get(user_id)
            user.user_manager_id = partner_id
            session.commit()
        return True


    async def restart_partner_for_testing(self, user_id):
        with session_factory() as session:
            user_control = UserControl(session)
            user = await user_control.get(user_id)
            user.user_stage = "greetings"
            user.product_choice = None

            form_control = UserFormControl(session)
            form = await form_control.get(user_id)
            if form:
                session.delete(form)

            history_control = CreditHistoryControl(session)
            history = await history_control.get(user_id)
            history.credit_history_user_debts = None
            history.credit_history_user_bki = None
            history.credit_history_user_okb = None

            user_contract_control = ContractControl(session)
            contract = await user_contract_control.get(user_id)
            if contract:
                session.delete(contract)

            user_payments_control = PaymentsControl(session)
            user_payments = await user_payments_control.get(user_id)
            if user_payments:
                session.delete(user_payments)

            documents_control = UserDocumentsControl(session)
            documents = await documents_control.get(user_id)
            documents.user_documents_snils = None
            documents.user_documents_passport23 = None
            documents.user_documents_passport45 = None
            documents.user_documents_drive_folder_link = "Документы не загружены"

            session.commit()
        return True


    async def move_client_to_buy_estate_btn(self, client_id):

        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_to_my_clients_btn'))
        with session_factory() as session:
            user_control = UserControl(session)
            user = await user_control.get(client_id)
            if user.user_name:
                self._msg = f"<b>Клиент <i>@{user.user_name}</i> был переведен на этап покупки недвижимости!</b>"
            else:
                self._msg = f"<b>Клиент <i>{user.user_id}</i> был переведен на этап покупки недвижимости!</b>"
            user.user_stage = 'buy_estate_form'
            session.commit()
        return keyboard



    async def move_client_to_sell_estate_btn(self, client_id):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_to_my_clients_btn'))
        with session_factory() as session:
            user_control = UserControl(session)
            user = await user_control.get(client_id)
            if user.user_name:
                self._msg = f"<b>Клиент <i>@{user.user_name}</i> был переведен на этап продажи недвижимости!</b>"
            else:
                self._msg = f"<b>Клиент <i>{user.user_id}</i> был переведен на этап продажи недвижимости!</b>"
            user.user_stage = 'sell_estate_form'
            session.commit()
        return keyboard


    async def send_decision_to_client_btn(self, client_id):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Ипотека одобрена ✅ ', callback_data=f'send_mortgage_result#1#{client_id}'))
        keyboard.add(InlineKeyboardButton('Ипотека отклонена 🚫 ', callback_data=f'send_mortgage_result#0#{client_id}'))
        keyboard.add(InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_to_my_clients_btn'))
        return keyboard


    async def send_mortgage_result(self, result: bool, client_id: int):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_to_my_clients_btn'))
        with session_factory() as session:
            user_control = UserControl(session)
            user = await user_control.get(client_id)
            if user.user_name:
                self._msg = f"<b>Клиент <i>@{user.user_name}</i> получил решение от банка!</b>"
            else:
                self._msg = f"<b>Клиент <i>{user.user_id}</i> получил решение от банка!</b>"
            user.user_stage = 'mortgage_approving_result'
            user.mortgage_result = result
            session.commit()
        return keyboard