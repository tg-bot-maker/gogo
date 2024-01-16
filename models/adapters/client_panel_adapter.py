from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Optional
from database.models import User
from database.models import UserForm

class ClientPanelAdapter:
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


    async def client_panel_btn(self, client_obj: User):
        if client_obj.user_fio != "Аноним":
            name = f"Ваше имя: <b>{client_obj.user_fio}</b>\n"
        else:
            name = ""

        self._msg = f"📍  <b>Добро пожаловать в ваш кабинет!</b>\n" \
                    f"👤  {name}" \
                    f"🆔  Ваш ID: <code>{client_obj.user_id}</code>\n\n" \
                    f"Здесь вы можете просмотреть и в случае необходимости изменить вашу <b>анкету</b>" \
                    f"или просмотреть информацию по вашей <b>ипотеке</b> и <b>страховке</b>.\n" \
                    f"Также вы можете поучаствовать в нашей <b>реферальной программе</b> и получить " \
                    f"<b>выплаты 20.000 рублей</b> за каждого друга, который по вашей рекомендации" \
                    f" получит ипотеку при помощи нашего сервиса!" \

        keyboard = InlineKeyboardMarkup()\
            .add(InlineKeyboardButton('Моя анкета 📝', callback_data=f'my_form_btn#{client_obj.user_id}')) \
            .add(InlineKeyboardButton('Моя ипотека 🏡', callback_data=f'my_mortgage_btn#{client_obj.user_id}')) \
            .add(InlineKeyboardButton('Моя страховка 🛡', callback_data=f'my_insurance_btn#{client_obj.user_id}')) \
            .add(InlineKeyboardButton('Реферальная программа 💰', callback_data=f'client_referral_system_btn#{client_obj.user_id}')) \
            .add(InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_btn'))

        return keyboard


    async def my_form_btn(self, form: UserForm):
        description = {"ru": "Российская Федерация", "different": "Другое"}
        accomodation_types = {"house": "Дом", "new_house": "Строительство дома", "flat": "Квартира",
                              "new_flat": "Новостройка", "commercial": "Коммерческая", "apart": "Апартаменты"}
        symbols = {False: "❌", True: "✅"}
        text = f"<b>ФИО:</b> {form.user_fio}\n" \
               f"<b>Гражданство:</b> {description[form.citizenship]}\n" \
               f"<b>Размер ипотеки:</b> {form.estimated_mortgage_amount}\n" \
               f"<b>Тип недвижимости:</b> {accomodation_types[form.accommodation_type]}\n" \
               f"<b>Размер первого взноса:</b> {form.down_payment_amount}\n" \
               f"<b>Срок ипотеки:</b> {form.mortgage_term}\n" \
               f"<b>Дети после 2018:</b> {symbols[form.children_after_2018]}\n" \
               f"<b>Наличие кредитов:</b> {symbols[form.credits_in_the_past]}\n" \
               f"<b>Официальная работа:</b> {symbols[form.official_job]}\n" \
               f"<b>Судимости:</b> {symbols[form.convictions]}\n" \
               f"<b>Банкротство:</b> {symbols[form.bankruptcy]}\n" \
               f"<b>Просрочки по платежам:</b> {symbols[form.late_payments]}\n" \
               f"<b>Брак:</b> {symbols[form.marriage]}\n" \
               f"<b>Количество детей:</b> {form.children_amount}\n"

        self._msg = "📝 Ваша анкета:\n\n" \
                    f"{text}" \


        keyboard = InlineKeyboardMarkup()\
            .add(InlineKeyboardButton('Изменить анкету (заполнить заново)', callback_data=f'change_my_form_btn#{form.form_user_id}')) \
            .add(InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_client_panel_btn'))

        return keyboard