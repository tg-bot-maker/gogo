from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Optional
from database.db import session_factory
from models.controls.user_controls import UserControl


class PickProductAdapter:
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


    async def pick_credit_product(self):
        self._msg = "<b>🔎    Выберите кредитный продукт:</b>"
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton('Ипотека под ключ 🔑', callback_data='pick_product_choice#mortgage_btn')) \
            .add(InlineKeyboardButton('Покупка недвижимости', callback_data='pick_product_choice#buy_property_btn')) \
            .add(InlineKeyboardButton('Продажа недвижимости', callback_data='pick_product_choice#sell_property_btn')) \
            #.add(InlineKeyboardButton('Кредитная карта', callback_data='pick_product_choice#credit_card_btn')) \
            #.add(InlineKeyboardButton('Кредит под залог недвижимости', callback_data='pick_product_choice#real_estate_loan_btn')) \
            #.add(InlineKeyboardButton('Кредит на развитие бизнеса', callback_data='pick_product_choice#business_btn')) \
            #.add(InlineKeyboardButton('Автокредит', callback_data='pick_product_choice#car_loan_btn'))
        return keyboard


    async def pick_credit_product_choice(self, choice):
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton('Выбрать ✅', callback_data=f'pick_credit_product_choice#{choice}')) \
            .add(InlineKeyboardButton('◀️   Назад    ', callback_data='go_back_btn'))
        return keyboard


    async def pick_credit_product_finish(self, user_id, choice):
        with session_factory() as session:
            user_control = UserControl(session)
            user = await user_control.get(user_id)
            user.product_choice = choice
            session.commit()