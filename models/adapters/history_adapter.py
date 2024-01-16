from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Optional
from database.db import session_factory
from models.adapters.user_adapter import UserAdapter
from models.adapters.admin_panel_adapter import AdminPanelAdapter
from models.controls.history_control import CreditHistoryControl


class HistoryAdapter:
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


    async def check_credit_history_btn(self, user_id):
        with session_factory() as session:
            history_controller = CreditHistoryControl(session)
            history = await history_controller.get(user_id)
            session.commit()

        keyboard = InlineKeyboardMarkup()
        if history.credit_history_user_debts is None:
            self._msg = "<b>С помощью кредитной истории банки принимают решение по одобрению ипотеки. Поэтому для нас важно перед подачей все" \
                                " проверить. Так же, как и для вас важно проверить себя на штрафы и долги на ФССП. Потому что даже 2000 р. штрафа могут " \
                                "послужить для банка причиной для отказа.\n\nВам необходимо проверить ваши задолженности на ФССП.\nЗагружать результаты проверки не нужно. Достаточно подтвердить, что вы сделали проверку и не обнаружили долгов.</b>"
            keyboard.add(InlineKeyboardButton('Проверка задолженностей', callback_data='history_check_debts_btn')) \
             .add(InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_btn'))
        elif history.credit_history_user_okb is None and history.credit_history_user_debts is not None:
            self._msg = "<b>Вам необходимо загрузить файл с отчетом о кредитной истории из ОКБ.\n\nПосле загрузки файла вы автоматически перейдете к следующему этапу.</b>"
            keyboard.add(InlineKeyboardButton('Отчет ОКБ', callback_data='history_check_okb_btn')) \
                .add(InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_btn'))
        else:
            self._msg = "<b>Вам необходимо загрузить файл с отчетом о кредитной истории из БКИ.\n\nПосле загрузки файла вы автоматически перейдете к следующему этапу.</b>"
            keyboard.add(InlineKeyboardButton('Отчет БКИ', callback_data='history_check_bki_btn')) \
                .add(InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_btn'))


       # self._msg = "<b>Вам необходимо загрузить два файла с отчетами о кредитной истории.\n\nПосле загрузки файлов с отчетами вы автоматически перейдете к следующему этапу.\n\nПо кнопкам ниже вы можете найти подробные инструкции по проверке истории:</b>"
        return keyboard


    async def check_history_bki_btn(self):
        self._msg = "<b>Для того чтобы мы могли проверить вашу кредитную историю, вам необходимо загрузить файл с кредитной историей в формате PDF.</b>\n\n" \
                    "<b>Для этого вам нужно сделать следующее:</b>\n" \
                    "<b>1</b> - Перейти на сайт https://person.nbki.ru \n"  \
                    "<b>2</b> - Зарегистрироваться на сайте, указав email и создав пароль. \n" \
                    "<b>3</b> - Подтвердить email. \n" \
                    "<b>4</b> - Зайти в личный кабинет https://person.nbki.ru \n" \
                    "<b>5</b> - Указать все данные паспорта. \n" \
                    "<b>6</b> - Нажать <i>Авторизоваться через Госуслуги</i>, Вас перебросит на сайт Госуслуг, где вам необходимо ввести логин и пароль от Госуслуг. (Если у Вас нет Госуслуг, необходимо зарегистрироваться и подтвердить аккаунт в точках подтверждения аккаунтов). \n" \
                    "<b>7</b> - После авторизации зайти в <i>Мои заказы</i>. \n" \
                    "<b>8</b> - Выбрать <i>Заказать кредитный отчет</i>. \n" \
                    "<b>9</b> - После этого зайти корзину. \n" \
                    "<b>10</b> - Ваш отчет готов, нажмите <i>Скачать отчет</i>. " \

        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton('Загрузить отчет (PDF файл)', callback_data='upload_file_bki_btn'))\
            .add(InlineKeyboardButton('Посмотреть видео инструкцию', callback_data='history_view_video_instruction_bki_btn')) \
            .add(InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_check_credit_history_btn'))

        return keyboard



    async def history_view_video_instruction_bki_btn(self):
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_check_credit_history_bki_btn'))
        return keyboard


    async def check_history_okb_btn(self):
        self._msg = "<b>Вам необходимо проверить и загрузить кредитную истотрию с помощью подтверждения личности с сайта Гос. услуги. \n\n" \
                    "Для запроса необходимо зайти на сайт ОКБ по ссылке https://credistory.ru, выбрать вариант войти через Гос. услуги и следовать инструкциям.</b>"
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton('Загрузить отчет (PDF файл)', callback_data='upload_file_okb_btn')) \
            .add(InlineKeyboardButton('Посмотреть видео инструкцию', callback_data='history_view_video_instruction_okb_btn')) \
                .add(InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_check_credit_history_btn'))

        return keyboard

    async def history_view_video_instruction_okb_btn(self):
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton('◀️   Назад    ', callback_data='to_ltsc_btn'))
        return keyboard


    async def check_debts_btn(self):
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('Перейти к Госуслугам', url="https://www.gosuslugi.ru/")) \
                .add(InlineKeyboardButton('Проверка проведена, долгов нет', callback_data='check_done_no_debts_btn')) \
                .add(InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_check_credit_history_btn'))

        return keyboard


    async def check_done_no_debts_btn(self, user_id):
        with session_factory() as session:
            history_controller = CreditHistoryControl(session)
            history = await history_controller.get(user_id)
            history.credit_history_user_debts = True
            session.commit()

        self._msg = "<b>Отлично! Теперь вы можете перейти к следующему этапу 👇</b>"
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('    Перейти    ', callback_data='back_to_check_credit_history_btn'))
        return keyboard

    async def upload_file_okb_btn(self, user_id):
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_check_credit_history_btn'))
        self._msg = "<b>Отправьте файл с отчетом ОКБ</b>"

        with session_factory() as session:
            history_controller = CreditHistoryControl(session)
            history = await history_controller.get(user_id)
            session.commit()


        if history.credit_history_user_okb is None:
            self._msg = "<b>Отправьте файл с отчетом ОКБ</b>"
            take_file = True
        else:
            self._msg = "<b>Отчет ОКБ был успешно загружен!\nТеперь вы можете перейти к следующему этапу 👇</b>"
            keyboard = InlineKeyboardMarkup().add(
                InlineKeyboardButton('    Перейти    ', callback_data='back_to_check_credit_history_btn'))
            take_file = False

        return keyboard, take_file



    async def upload_file_bki_btn(self, user_id):
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_check_credit_history_bki_btn'))

        with session_factory() as session:
            history_controller = CreditHistoryControl(session)
            history = await history_controller.get(user_id)
            session.commit()

        if history.credit_history_user_bki is None:
            self._msg = "<b>Отправьте файл с отчетом БКИ</b>"
            take_file = True
        else:
            self._msg = "<b>Отчет БКИ был загружен!</b>"
            take_file = False

        return keyboard, take_file


    async def add_bki(self, credit_history_user_id, credit_history_user_bki, call, scheduler):
        with session_factory() as session:
            history_controller = CreditHistoryControl(session)
            history = await history_controller.get(credit_history_user_id)
            history.credit_history_user_bki = credit_history_user_bki

            if history.credit_history_user_okb is not None:
                user_adapter = UserAdapter()
                admin_panel_adapter = AdminPanelAdapter()
                if await admin_panel_adapter.get_user_payment(call.from_user.id):
                    await user_adapter.update_user_stage(call.from_user.id, "payment_ready", call, scheduler)
                else:
                    await user_adapter.update_user_stage(call.from_user.id, "payment", call, scheduler)
                new_stage = True
            else:
                new_stage = False
            session.commit()
            return new_stage

    async def add_okb(self, credit_history_user_id, credit_history_user_okb, call, scheduler):
        with session_factory() as session:
            history_controller = CreditHistoryControl(session)
            history = await history_controller.get(credit_history_user_id)
            history.credit_history_user_okb = credit_history_user_okb

            if history.credit_history_user_bki is not None:
                user_adapter = UserAdapter()
                admin_panel_adapter = AdminPanelAdapter()
                if await admin_panel_adapter.get_user_payment(call.from_user.id):
                    await user_adapter.update_user_stage(call.from_user.id, "payment_ready", call, scheduler)
                else:
                    await user_adapter.update_user_stage(call.from_user.id, "payment", call, scheduler)
                new_stage = True
            else:
                new_stage = False
            session.commit()
            return new_stage

