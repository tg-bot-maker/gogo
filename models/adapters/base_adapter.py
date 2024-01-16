from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types
from typing import Optional
from database.db import session_factory
from models.controls.user_controls import UserControl
from models.controls.history_control import CreditHistoryControl
from models.controls.user_documents_control import UserDocumentsControl
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from configs import config

from APscheduler.notifications.admin_notifications import start_command_sent



class BaseAdapter:
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


    async def start(self,
                    user_id: int,
                    user_name: str = None,
                    start_mode: bool = True,
                    user_manager_id: int = 0,
                    scheduler: AsyncIOScheduler = None,
                    message: types.Message = None
                    ) -> InlineKeyboardMarkup:

        """Start bot"""
        if start_mode:
             with session_factory() as session:
                user_control = UserControl(session)
                user = await user_control.get(user_id)
                if not user:
                    history_control = CreditHistoryControl(session)
                    upload_documents_control = UserDocumentsControl(session)
                    await upload_documents_control.add(user_id)
                    await user_control.add(user_id, user_name, user_manager_id)
                    session.commit()
                    with session_factory() as session:
                        await history_control.add(user_id)
                        session.commit()
                    scheduler.add_job(start_command_sent, trigger="date", run_date=datetime.now()+timedelta(seconds=5), kwargs={"message": message, "user_manager_id": user_manager_id})
                    user_control = UserControl(session)
                    user = await user_control.get(user_id)
                else:
                    pass

        else:
            with session_factory() as session:
                user_control = UserControl(session)
                user = await user_control.get(user_id)





        if user.user_stage == 'form':
            stage_text_to_add = f'Для начала, чтобы мы могли понять, сможем мы вас ' \
                                f'одобрить или нет, нам необходимо задать вам несколько вопросов. Отвечайте на них честно.\n\n' \
                                f'Когда будете готовы, нажмите на кнопку <b>заполнить анкету</b> и приступите к ответам на вопросы:'
            stage_highlight = "1⃣  <b>Заполнение анкеты</b> 👈\n" \
                              '2⃣  Загрузка документов\n' \
                              '3⃣  Подготовка договора\n' \
                              '4⃣  Кредитная история\n' \
                              '5⃣  Оплата\n' \
                              '6⃣  Одобрение ипотеки\n' \
                              '7⃣  Решение по ипотеке\n' \

            self._inline_keyboard.row(
                InlineKeyboardButton('Заполнить анкету', callback_data='form_question_0'),
                InlineKeyboardButton('Помощь', callback_data='help_btn')
            )
        elif user.user_stage == 'check_credit_history':
            stage_text_to_add = "Мы рады что вы выбрали наш сервис!\n\n" \
                                "После прохождения вами следующего этапа мы сможем с вероятностью 90% прогнозировать, одобрят вас или нет.\n" \
                                "Следующий этап - это проверка штрафов и долгов на ФССП и кредитной истории ОКБ и НБКИ."



            stage_highlight = "1⃣  Заполнение анкеты\n" \
                              '2⃣  Загрузка документов\n' \
                              '3⃣  Подготовка договора\n' \
                              '4⃣  <b>Кредитная история</b> 👈\n' \
                              '5⃣  Оплата\n' \
                              '6⃣  Одобрение ипотеки\n' \
                              '7⃣  Решение по ипотеке\n' \


            self._inline_keyboard.row(
                InlineKeyboardButton('Кредитная история', callback_data='check_credit_history_btn'),
                InlineKeyboardButton('Помощь', callback_data='help_btn')
            )
        elif user.user_stage == 'upload_docs':
            stage_text_to_add = "На данном этапе вам необходиимо загрузить фотографии или сканы ваших документов."
            stage_highlight = "1⃣  Заполнение анкеты\n" \
                              '2⃣  <b>Загрузка документов</b> 👈\n' \
                              '3⃣  Подготовка договора\n' \
                              '4⃣  Кредитная история\n' \
                              '5⃣  Оплата\n' \
                              '6⃣  Одобрение ипотеки\n' \
                              '7⃣  Решение по ипотеке\n' \


            self._inline_keyboard.row(
                InlineKeyboardButton('Загрузить документы', callback_data='upload_documents_btn'),
                InlineKeyboardButton('Помощь', callback_data='help_btn')
            )


        elif user.user_stage == 'pick_product':
            stage_text_to_add = f'Для начала вам необходимо выбрать ' \
                                f' продукт. Выберите нужный вариант по кнопке 👇'
            stage_highlight = "<b>Выбор продукта</b> 📍"

            self._inline_keyboard.row(
                        InlineKeyboardButton('Выбрать продукт', callback_data='pick_credit_product_btn'),
                        InlineKeyboardButton('Помощь', callback_data='help_btn')
                    )

        elif user.user_stage in ['contract_ready', 'prepare_contract']:
            stage_text_to_add = "<b>На данном этапе вам нужно ознакомиться с договором и принять его условия 📄</b>"
            stage_highlight = "1⃣  Заполнение анкеты\n" \
                              '2⃣  Загрузка документов\n' \
                              '3⃣  <b>Подготовка договора</b> 👈\n' \
                              '4⃣  Кредитная история\n' \
                              '5⃣  Оплата\n' \
                              '6⃣  Одобрение ипотеки\n' \
                              '7⃣  Решение по ипотеке\n' \

            self._inline_keyboard.add(
                        InlineKeyboardButton('Получить договор', callback_data='get_contract_btn'),
                        InlineKeyboardButton('Помощь', callback_data='help_btn')
                    )

        elif user.user_stage in ['payment', 'payment_ready']:
            stage_text_to_add = "<b>Вы приняли условия договора ✅\n\nДля продолжения работы вам необходимо оплатить наши услуги. Сделать это вы можете по кнопке ниже.</b>"
            stage_highlight = "1⃣  Заполнение анкеты\n" \
                              '2⃣  Загрузка документов\n' \
                              '3⃣  Подготовка договора\n' \
                              '4⃣  Кредитная история\n' \
                              '5⃣  <b>Оплата</b> 👈\n' \
                              '6⃣  Одобрение ипотеки\n' \
                              '7⃣  Решение по ипотеке\n' \


            self._inline_keyboard.add(
                InlineKeyboardButton('Оплатить', callback_data='pay_btn'),
                InlineKeyboardButton('Помощь', callback_data='help_btn')
            )
        elif user.user_stage == "payment_done":
            stage_text_to_add = "<b>Отлично!\nВаша оплата проверяется менеджером, после подтверждения оплаты вы получите уведомление.</b>"
            stage_highlight = "1⃣  Заполнение анкеты\n" \
                              '2⃣  Загрузка документов\n' \
                              '3⃣  Подготовка договора\n' \
                              '4⃣  Кредитная история\n' \
                              '5⃣  <b>Оплата</b> 👈\n' \
                              '6⃣  Одобрение ипотеки\n' \
                              '7⃣  Решение по ипотеке\n' \


            self._inline_keyboard.add(
                InlineKeyboardButton('Помощь', callback_data='help_btn')
            )
        elif user.user_stage == "payment_approved":
            stage_text_to_add = "<b>Вы успешно приняли условия договора и совершили оплату," \
                                " мы уже занимаемся одобрением вашей ипотеки ✔</b>"
            stage_highlight = "1⃣  Заполнение анкеты\n" \
                              '2⃣  Загрузка документов\n' \
                              '3⃣  Подготовка договора\n' \
                              '4⃣  Кредитная история\n' \
                              '5⃣  Оплата\n' \
                              '6⃣  <b>Одобрение ипотеки</b> 👈\n' \
                              '7⃣  Решение по ипотеке\n' \


            self._inline_keyboard.add(
                InlineKeyboardButton('Помощь', callback_data='help_btn')
            )
        elif user.user_stage == "mortgage_approving_result":
            if user.mortgage_result is True:
                stage_text_to_add = "<b>Ваша ипотека одобрена! 🎉</b>\n" \
                                    "<i>Для получения более подробной информации вы можете" \
                                    " обратиться к своему менеджеру или по кнопке <b>Помощь</b> ниже.</i>"
            elif user.mortgage_result is False:
                stage_text_to_add = "<b>Ваша ипотека не была одобрена.</b>\n" \
                                    "<i>Для получения более подробной информации вы можете" \
                                    " обратиться к своему менеджеру или по кнопке <b>Помощь</b> ниже.</i>"
            else:
                stage_text_to_add = "<b>Ваша ипотека находится на рассмотрении.</b>\n" \
                                    "<i>Для получения более подробной информации вы можете" \
                                    " обратиться к своему менеджеру или по кнопке <b>Помощь</b> ниже.</i>"
            stage_highlight = "1⃣  Заполнение анкеты\n" \
                              '2⃣  Загрузка документов\n' \
                              '3⃣  Подготовка договора\n' \
                              '4⃣  Кредитная история\n' \
                              '5⃣  Оплата\n' \
                              '6⃣  Одобрение ипотеки\n' \
                              '7⃣  <b>Решение по ипотеке</b> 👈\n' \


            self._inline_keyboard.row(
                InlineKeyboardButton('Подбор недвижимости 🏡', callback_data='buy_estate_selection'),
                InlineKeyboardButton('Помощь', callback_data='help_btn')
            )




        # ЭТАПЫ ПОКУПКИ НЕДВИЖИМОСТИ
        elif user.user_stage == "buy_estate_form":
            stage_text_to_add = "Для того чтобы мы могли подобрать для вас недвижимость, вам необходимо заполнить анкету 📝"
            stage_highlight = "1⃣  <b>Анкета</b> 👈\n" \
                              "2⃣  Загрузка документов\n" \
                              "3⃣  Подготовка договора\n" \
                              "4⃣  Оплата\n" \
                              "5⃣  Подбор объекта\n" \
                              "6⃣  Покупка\n" \

            self._inline_keyboard.add(
                InlineKeyboardButton('Заполнить анкету', callback_data='fill_the_buy_estate_form_btn'),
                InlineKeyboardButton('Помощь', callback_data='help_btn')
            )


        elif user.user_stage == "buy_estate_upload_docs":
            stage_text_to_add = "Для продолжения работы вам необходимо загрузить документы 📄"
            stage_highlight = "1⃣  Анкета\n" \
                              "2⃣  <b>Загрузка документов</b> 👈\n" \
                              "3⃣  Подготовка договора\n" \
                              "4⃣  Оплата\n" \
                              "5⃣  Подбор объекта\n" \
                              "6⃣  Покупка\n" \

            self._inline_keyboard.add(
                InlineKeyboardButton('Загрузить документы', callback_data='buy_estate_upload_docs_btn'),
                InlineKeyboardButton('Помощь', callback_data='help_btn')
            )


        elif user.user_stage == "buy_estate_contract":
            stage_text_to_add = "На данном этапе мы подготовим договор 📝"
            stage_highlight = "1⃣  Анкета\n" \
                              "2⃣  Загрузка документов\n" \
                              "3⃣  <b>Подготовка договора</b> 👈\n" \
                              "4⃣  Оплата\n" \
                              "5⃣  Подбор объекта\n" \
                              "6⃣  Покупка\n" \

            self._inline_keyboard.add(
                #InlineKeyboardButton('Загрузить документы', callback_data='buy_estate_upload_docs_btn'),
                InlineKeyboardButton('Помощь', callback_data='help_btn')
            )


        elif user.user_stage == "buy_estate_payment":
            stage_text_to_add = "На данном этапе вы можете оплатить услуги 📝"
            stage_highlight = "1⃣  Анкета\n" \
                              "2⃣  Загрузка документов\n" \
                              "3⃣  Подготовка договора\n" \
                              "4⃣  <b>Оплата 👈\n\n" \
                              "5⃣  Подбор объекта</b>" \
                              "6⃣  Покупка\n" \

            self._inline_keyboard.add(
                InlineKeyboardButton('Оплатить', callback_data='buy_estate_pay_btn'),
                InlineKeyboardButton('Помощь', callback_data='help_btn')
            )


        elif user.user_stage == "buy_estate_selection":
            stage_text_to_add = "На данном этапе мы поможем вам подобрать недвижимость по вашим критериям и преобрети ее по выгодной цене ✅"
            stage_highlight = "1⃣  Анкета\n" \
                              "2⃣  Загрузка документов\n" \
                              "3⃣  Подготовка договора\n" \
                              "4⃣  Оплата\n" \
                              "5⃣  <b>Подбор объекта</b> 👈\n" \
                              "6⃣  Покупка\n" \


            self._inline_keyboard.add(
                InlineKeyboardButton('Посмотреть объекты', callback_data='check_the_objects_btn'),
                InlineKeyboardButton('Помощь', callback_data='help_btn')
            )


        elif user.user_stage == "buy_estate_buying":
            stage_text_to_add = "На данном этапе мы поможем вам подобрать недвижимость по вашим критериям и преобрети ее по выгодной цене ✅"
            stage_highlight = "1⃣  Анкета\n" \
                              "2⃣  Загрузка документов\n" \
                              "3⃣  Подготовка договора\n" \
                              "4⃣  Оплата\n" \
                              "5⃣  Подбор объекта\n" \
                              "6⃣  <b>Покупка</b> 👈\n" \


            self._inline_keyboard.add(
                InlineKeyboardButton('Помощь', callback_data='help_btn')
            )





        # ЭТАПЫ ПРОДАЖИ НЕДВИЖИМОСТИ
        elif user.user_stage == "sell_estate_form":
            stage_text_to_add = "Для того чтобы мы могли помочь вам продать недвижимость, вам необходимо заполнить анкету 📝"
            stage_highlight = "1⃣  <b>Анкета</b> 👈\n" \
                              "2⃣  Загрузка документов\n" \
                              "3⃣  Подготовка договора\n" \
                              "4⃣  Оплата\n" \
                              "5⃣  Продажа\n" \

            self._inline_keyboard.add(
                InlineKeyboardButton('Заполнить анкету', callback_data='fill_the_sell_estate_form_btn'),
                InlineKeyboardButton('Помощь', callback_data='help_btn')
            )





        elif user.user_stage == "finish":
            stage_text_to_add = "<b>Спасибо за то что воспользовались нашим сервисом!/<b>"
            stage_highlight = ""


            self._inline_keyboard.add(
                InlineKeyboardButton('Оставить обратную связь', callback_data='leave_feedback_btn')) \
                .add(InlineKeyboardButton('Помощь', callback_data='help_btn'))

        else:
            stage_highlight = ""
            stage_text_to_add = ""







        if user_id in config.admins:
            self._msg = f'Здравствуйте, <b>администратор</b>!\n\n' \
                        f'На данный момент в находитесь на этапе:\n' \
                        f'{stage_highlight}\n\n' \
                        f'{stage_text_to_add}'
            self._inline_keyboard.add(InlineKeyboardButton('Администрирование', callback_data='admin_panel_btn'))
            self._inline_keyboard.add(InlineKeyboardButton('Кабинет партнера', callback_data='partner_menu_handler'))
            self._inline_keyboard.add(InlineKeyboardButton('Кабинет клиента', callback_data='personal_panel_btn'))

        elif user.is_partner:
            self._msg = f'Здравствуйте, <b>партнер</b>!\n\n' \
                        f'<i>Для тестирования системы у вас есть возможность самостоятельно пройти все этапы работы бота.\n' \
                        f'Ваши ответы и ваш аккаунт клиента будут закреплены за вашим партнерским аккаунтом.</i>\n\n' \
                        f'На данный момент в находитесь на этапе:\n' \
                        f'{stage_highlight}\n\n' \
                        f'{stage_text_to_add}'
            self._inline_keyboard.add(InlineKeyboardButton('Кабинет партнера', callback_data='partner_menu_handler'))
            self._inline_keyboard.add(InlineKeyboardButton('Кабинет клиента', callback_data='personal_panel_btn'))


        elif user.user_manager_id != 0000000000:
            with session_factory() as session:
                user_control = UserControl(session)
                user_partner = await user_control.get(user.user_manager_id)

                self._msg = f'Здравствуйте!\nВаш менеджер - @{user_partner.user_name}\n\n' \
                        f'На данный момент в находитесь на этапе:\n' \
                        f'{stage_highlight}\n\n' \
                        f'{stage_text_to_add}'
            self._inline_keyboard.add(InlineKeyboardButton('Мой кабинет', callback_data='personal_panel_btn'))


        else:
            self._msg = f'Здравствуйте!\n\n' \
                        f'На данный момент в находитесь на этапе:\n' \
                        f'{stage_highlight}\n\n' \
                        f'{stage_text_to_add}'
            self._inline_keyboard.add(InlineKeyboardButton('Мой кабинет', callback_data='personal_panel_btn'))


        if user.user_stage == 'greetings':
            self._msg = 'greetings'
            self._inline_keyboard = InlineKeyboardMarkup().row(InlineKeyboardButton('Регистрация', callback_data='registration_btn'))
            return self.inline_keyboard


        return self.inline_keyboard


    async def admin_menu_kb(self):
        keyboard = InlineKeyboardMarkup()
        webAppTest = types.WebAppInfo(url="https://max-test-domain.site/webapp_page?key=eANH55sHJy3pF2I")

        webapp_button = types.InlineKeyboardButton(text='Посмотреть таблицу 👀', web_app=webAppTest)
        keyboard.add(InlineKeyboardButton('Партнеры 📁', callback_data='partners_panel_for_admin_btn')) \
        .add(InlineKeyboardButton('Аналитика 🔎', callback_data='admin_analytics_btn')) \
        .add(InlineKeyboardButton('Архив 🗄', callback_data='archive_btn')) \
        .add(webapp_button) \
        .add(InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_btn'))
        #.add(InlineKeyboardButton('Посмотреть объекты 🗺', callback_data='check_the_objects_btn')) \

        return keyboard


    async def partner_menu_kb(self):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Партнерская программа 🤝', callback_data='referral_system_btn')) \
        .row(InlineKeyboardButton('Создать договор 📄', callback_data='generate_contract_btn'),
        InlineKeyboardButton('Счета на оплату 💰', callback_data='payments_btn')) \
        .add(InlineKeyboardButton('Встречи 🤝', callback_data='meetings_btn')) \
        .add(InlineKeyboardButton('Юридические услуги 🛠', callback_data='legal_services_btn')) \
        .add(InlineKeyboardButton('Финансы 🛠', callback_data='finances_btn')) \
        .add(InlineKeyboardButton('Ипотечный калькулятор 🧮', url="https://calcus.ru/kalkulyator-ipoteki")) \
        .add(InlineKeyboardButton('Страховка 🛡', callback_data='partner_menu_insurance_btn')) \
        .add(InlineKeyboardButton('Контакты банков 📞', callback_data='bank_contacts_btn')) \
        .add(InlineKeyboardButton('Условия банков 🏦', url="https://docs.google.com/spreadsheets/d/1ffcfjHBWhJdYMcgvPUVihtrcnXWfULHE12yMBZy24oQ/edit?usp=sharing")) \
        .add(InlineKeyboardButton('Уведомления 🔔', callback_data='notifications_btn')) \
        .add(InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_btn'))

        return keyboard


    async def analytics_kb(self, show_form_button: bool):
        keyboard = InlineKeyboardMarkup()
        user = await self.get_user(self._user_id)
        if user.user_manager_id == 0000000000 and user.is_partner is False:
            keyboard.add(InlineKeyboardButton('Назначить партнера', callback_data=f'assign_manager_btn#{user.user_id}'))
        keyboard.add(InlineKeyboardButton('Управление', callback_data='control_client_btn'))
        if show_form_button:
            keyboard.add(InlineKeyboardButton('Посмотреть анкету', callback_data='show_form'))
        return keyboard.add(InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_to_analytics_btn'))


    async def back_kb(self):
        return InlineKeyboardMarkup().add(InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_btn'))



    async def back_to_admin_kb(self):
        return InlineKeyboardMarkup().add(InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_admin_menu_btn'))


    async def get_users_as_buttons(self):
        with session_factory() as session:
            user_control = UserControl(session)
            users = await user_control.get_all()
            session.commit()
        buttons: dict = {}
        for user in users:
            if user.user_fio == "Аноним":
                name = f"TG: {user.user_name}"
            else:
                name = user.user_fio
            buttons[f"user_number#{user.user_id}"] = name

        return buttons



    async def get_users_for_invoice_as_buttons(self):
        with session_factory() as session:
            user_control = UserControl(session)
            users = await user_control.get_clients_without_invoice()
            session.commit()
        buttons: dict = {}
        for user in users:
            if user.user_fio != "Аноним":
                name = user.user_fio
            else:
                name = f"TG: {user.user_name}"
            buttons[f"user_number#{user.user_id}"] = name

        return buttons


    async def get_users_for_invoice_for_partner_as_buttons(self, partner_id):
        with session_factory() as session:
            user_control = UserControl(session)
            users = await user_control.get_clients_without_invoice_for_partner(partner_id)
            session.commit()
        buttons: dict = {}
        for user in users:
            if user.user_fio != "Аноним":
                name = user.user_fio
            else:
                name = f"TG: {user.user_name}"
            buttons[f"user_number#{user.user_id}"] = name

        return buttons


    async def get_user(self, user_id: int):
        with session_factory() as session:
            user_control = UserControl(session)
            user = await user_control.get(user_id)
            session.commit()
        return user







