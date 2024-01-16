from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Optional
from models.controls.user_controls import UserControl
from models.controls.payments_control import PaymentsControl
from models.controls.contract_controls import ContractControl
from database.db import session_factory
from datetime import datetime



class AdminPanelAdapter:
    def __init__(self, user_id: Optional[int] = None):
        self._user_id = user_id
        self._inline_keyboard = InlineKeyboardMarkup()
        self._msg = ''

    async def approve_top_up_kb(self):
        top_up_approved_btn = InlineKeyboardButton('✅️   Пополнить    ', callback_data='top_up_approved_btn')
        cancel_top_up_btn = InlineKeyboardButton('❌️   Отменить    ', callback_data='cancel_top_up_btn')
        return InlineKeyboardMarkup().add(top_up_approved_btn, cancel_top_up_btn)

    async def payments_btn(self):
        self._msg = "Выберите дествие:"
        create_invoice_btn = InlineKeyboardButton('Выставить счет', callback_data='create_invoice_btn')
        check_payments_btn = InlineKeyboardButton('Проверка платежей', callback_data='check_payments_btn')
        payments_statistics_btn = InlineKeyboardButton('Статистика по счетам', callback_data='payments_statistics_btn')
        back_btn = InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_partner_menu_btn')
        self._inline_keyboard = InlineKeyboardMarkup().add(create_invoice_btn).add(check_payments_btn).add(payments_statistics_btn).add(back_btn)

    async def contract_creation_final(self):
        send_to_client_btn = InlineKeyboardButton('Отправить клиенту', callback_data='send_to_client_btn')
        back_btn = InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_btn')
        self._inline_keyboard = InlineKeyboardMarkup().add(send_to_client_btn).add(back_btn)
        return self._inline_keyboard

    async def check_payments_detail_kb(self, client_id):
        approve_payment_from_client_btn = InlineKeyboardButton('Подтвердить оплату ✅️', callback_data=f'approve_payment_from_client_btn#{client_id}')
        back_btn = InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_btn')
        self._inline_keyboard = InlineKeyboardMarkup().add(approve_payment_from_client_btn).add(back_btn)
        return self._inline_keyboard

    async def partners_panel_for_admin_btn(self):
        self._msg = "<b>Выберите действие:</b>"
        partner_list_for_admin_btn = InlineKeyboardButton('Список партнеров 📄', callback_data='partner_list_for_admin_btn')
        users_without_partner_list_btn = InlineKeyboardButton('Клиенты без партнера 🙋', callback_data='users_without_partner_list_btn')
        create_partner_btn = InlineKeyboardButton('Сделать партнером ➕', callback_data='create_partner_btn')
        change_partner_btn = InlineKeyboardButton('Переназначить партнера 🔁', callback_data='change_partner_btn')
        back_btn = InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_admin_menu_btn')
        self._inline_keyboard = InlineKeyboardMarkup().add(partner_list_for_admin_btn).add(users_without_partner_list_btn).add(create_partner_btn).add(change_partner_btn).add(back_btn)
        return self._inline_keyboard




    async def get_contract_waiting_users_as_buttons(self):
        with session_factory() as session:
            user_control = UserControl(session)
            contract_waiting_clients = await user_control.get_contract_waiting_users()
            session.commit()
        buttons: dict = {}
        for client in contract_waiting_clients:
            if client.user_fio != "Аноним":
                name = client.user_fio
            else:
                name = f"TG: {client.user_name}"
            buttons[f"user_number#{client.user_id}"] = name

        return buttons


    async def get_contract_waiting_users_for_partner_as_buttons(self, partner_id):
        with session_factory() as session:
            user_control = UserControl(session)
            contract_waiting_clients = await user_control.get_contract_waiting_users_for_partner(partner_id)
            session.commit()
        buttons: dict = {}
        for client in contract_waiting_clients:
            if client.user_fio != "Аноним":
                name = client.user_fio
            else:
                name = f"TG: {client.user_name}"
            buttons[f"user_number#{client.user_id}"] = name

        return buttons


    async def get_client_fio_by_id(self, client_id):
        with session_factory() as session:
            user_control = UserControl(session)
            client_fio = await user_control.get_client_fio_by_id(client_id)
            session.commit()

        return client_fio


    async def create_payment(self, client_id, payment_link, payment_amount):
        with session_factory() as session:
            payments_control = PaymentsControl(session)
            await payments_control.add(client_id, payment_link, payment_amount)
            session.commit()

        return True



    async def get_user_payment(self, client_id):
        with session_factory() as session:
            payments_control = PaymentsControl(session)
            client_payment = await payments_control.get(client_id)
            session.commit()
        return client_payment



    async def get_users_without_partner_as_buttons(self):
        with session_factory() as session:
            user_control = UserControl(session)
            users_without_partner = await user_control.get_users_without_partner()
            session.commit()
        buttons: dict = {}
        for user in users_without_partner:
            if user.user_fio != "Аноним":
                name = user.user_fio
            else:
                name = f"TG: {user.user_name}"
            buttons[f"user_number#{user.user_id}"] = name

        return buttons




    async def get_user_payment_link(self, client_id):
        client_payment = await self.get_user_payment(client_id)

        if client_payment:
            text = f"<b>Cумма к оплате:</b>\n{client_payment.payment_amount} рублей.\n\n" \
                   f"<b>Ссылка для оплаты:</b>\n{client_payment.payment_link}"
            payment_done_btn = InlineKeyboardButton(' Платеж совершен ✅️ ', callback_data='payment_done_btn')
            back_btn = InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_btn')
            keyboard = InlineKeyboardMarkup().add(payment_done_btn, back_btn)

        else:
            text = "<b>Менеджер готовит ссылку для оплаты. Как только она будет готова вы получите уведомление.</b>"
            back_btn = InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_btn')
            keyboard = InlineKeyboardMarkup().add(back_btn)
        return text, keyboard


    async def get_user_contract_if_ready(self, client_id):
        user_contract = await self.get_user_contract(client_id)

        if user_contract:
            text = f"1#<b>Договор сформирован и отправлен вам в сообщении ниже ⬇️</b>\n\n"\
                    "Если вы согласны с условиями договора и хотите продолжить работу, нажмите кнопку для согласия с условиями."


            contract_aprovement_btn = InlineKeyboardButton('Согласен(-а) ✅', callback_data='contract_approved_btn#delete_msg')
            back_btn = InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_btn')
            keyboard = InlineKeyboardMarkup().add(contract_aprovement_btn, back_btn)

        else:
            text = "0#<b>Менеджер уже готовит для вас договор, ожидайте, пожалуйста. Вы получите уведомление как только он будет готов.</b>"
            back_btn = InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_btn')
            keyboard = InlineKeyboardMarkup().add(back_btn)
        return text, keyboard


    async def write_payment_done_datetime(self, client_id):
        with session_factory() as session:
            payments_control = PaymentsControl(session)
            client_payment = await payments_control.get(client_id)
            client_payment.payment_date = datetime.now()
            session.commit()
        return True


    async def approve_payment_from_client_btn(self, client_id):
        with session_factory() as session:
            payments_control = PaymentsControl(session)
            client_payment = await payments_control.get(client_id)
            client_payment.payment_status = True
            session.commit()
        return True



    async def get_user_contract(self, client_id):
        with session_factory() as session:
            contract_control = ContractControl(session)
            client_contract = await contract_control.get(client_id)
            session.commit()
        return client_contract



    async def create_contract(self, client_id, contract_path):
        with session_factory() as session:
            contract_control = ContractControl(session)
            await contract_control.add(client_id, contract_path)
            session.commit()
        return True


    async def make_contract_approved(self, client_id):
        with session_factory() as session:
            contract_control = ContractControl(session)
            contract = await contract_control.get(client_id)
            contract.contract_status = True
            session.commit()
        return True


    async def bank_contacts_btn(self):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Назад", callback_data="back_to_partner_menu_btn"))

        self._msg = "<b>Сбербанк:</b>\n" \
               "Герман Греф - 89009900990\n\n" \
               "<b>Тинькофф</b>:\n" \
               "Олег Тиньков - 89009900990\n\n"
        return keyboard