from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Optional
from aiogram.dispatcher import FSMContext
from database.db import session_factory
from models.controls.form_control import UserFormControl
from models.controls.user_controls import UserControl



class FormAdapter:
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


    async def get_fio_by_id(self, user_id):
        with session_factory() as session:
            form_control = UserFormControl(session)
            user_fio = await form_control.get(user_id)
            session.commit()
        return user_fio


    async def get_form(self, user_id):
        with session_factory() as session:
            form_control = UserFormControl(session)
            form = await form_control.get(user_id)
            session.commit()
        return form

    async def form_question_0(self):
        self._msg = "<i>После заполнения анкеты вы сможете проверить её," \
                    " и в случае, если в ней были допущены ошибки, заполнить заново.</i>\n\n" \
                    "<b>Введите ваши ФИО:</b>"
        return True

    async def form_question_0_1(self):
        self._msg = "<b>Введите актуальный номер телефона:</b>"
        return True


    async def form_question_1(self):
        self._msg = "<b>Ваше гражданство:</b>"
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton('Российская Федерация', callback_data='russian_citizenship_btn'))\
            .add(InlineKeyboardButton('Другое', callback_data='q1_different_btn'))

        return keyboard


    async def form_question_2(self):
        self._msg = "<b>Примерная сумма ипотеки</b>" \
                    " <i>(число в рублях)</i>:"
        return True


    async def form_question_3(self):
        self._msg = "<b>Какое жилье планируете приобретать?</b>"
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton('Дом', callback_data='accommodation_type_house_btn'),
            InlineKeyboardButton('Стройка дома', callback_data='accommodation_type_new_house_btn'))\
            .add(InlineKeyboardButton('Квартира', callback_data='accommodation_type_flat_btn'),
            InlineKeyboardButton('Новостройка', callback_data='accommodation_type_new_flat_btn')) \
            .add(InlineKeyboardButton('Апартаменты', callback_data='accommodation_type_apart_btn')) \
            .add(InlineKeyboardButton('Коммерческая недвижимость', callback_data='accommodation_type_commercial_btn'))
        return keyboard



    async def form_question_4(self):
        self._msg = "<b>Введите желаемый первый взнос по ипотеке</b>" \
                    " <i>(Число в рублях)</i>:"
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('Без первого взноса', callback_data='q4_no_down_payment'))
        return keyboard


    async def form_question_5(self):
        self._msg = "<b>Выберите желаемый срок ипотеки</b>:"
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton('10 лет', callback_data='form_question_5_btn#10'),
            InlineKeyboardButton('20 лет', callback_data='form_question_5_btn#20'),
            InlineKeyboardButton('30 лет', callback_data='form_question_5_btn#30'),
            InlineKeyboardButton('Другой', callback_data='form_question_5_btn#different'),
        )
        return keyboard

    async def form_question_5_1(self):
        self._msg = "<b>Введите желаемый срок ипотеки</b>" \
                    " <i>(число в годах)</i>:"
        return True

    async def form_question_6(self):
        self._msg = "<b>У вас есть дети, рождённые после 2018 года?</b>"
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton('Да', callback_data='yes_children_after_2018_btn'),
            InlineKeyboardButton('Нет', callback_data='no_children_after_2018_btn'),
        )
        return keyboard


    async def form_question_7(self):
        self._msg = "<b>Брали ли вы когда нибудь кредиты?</b>"
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton('Да', callback_data='yes_credits_in_the_past_btn'),
            InlineKeyboardButton('Нет', callback_data='no_credits_in_the_past_btn'),
        )
        return keyboard


    async def form_question_8(self):
        self._msg = "<b>Работаете ли вы официально?</b>"
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton('Да', callback_data='yes_official_job_btn'),
            InlineKeyboardButton('Нет', callback_data='no_official_job_btn'),
        )
        return keyboard


    async def form_question_9(self):
        self._msg = "<b>Были ли у вас судимости?</b>"
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton('Да', callback_data='yes_convictions_btn'),
            InlineKeyboardButton('Нет', callback_data='no_convictions_btn'),
        )
        return keyboard


    async def form_question_10(self):
        self._msg = "<b>Проводилась ли в отношении вас процедура банкротства?</b>"
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton('Да', callback_data='yes_bankruptcy_btn'),
            InlineKeyboardButton('Нет', callback_data='no_bankruptcy_btn'),
        )
        return keyboard


    async def form_question_11(self):
        self._msg = "<b>Допускали ли вы просрочки по кредитам?</b>"
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton('Да', callback_data='yes_late_payments_btn'),
            InlineKeyboardButton('Нет', callback_data='no_late_payments_btn'),
        )
        return keyboard


    async def form_question_12(self):
        self._msg = "<b>Состоите ли вы в браке?</b>"
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton('Да', callback_data='yes_marriage_btn'),
            InlineKeyboardButton('Нет', callback_data='no_marriage_btn'),
        )
        return keyboard


    async def form_question_13(self):
        self._msg = "<b>Есть ли у вас дети? Если да, то сколько?</b>" \
                    "\n<i>(введите количество или нажмите кнопку)</i>"
        no_children_btn = InlineKeyboardButton('Нет детей', callback_data='q13_no_children_btn')
        keyboard = InlineKeyboardMarkup().add(no_children_btn)
        return keyboard


    async def check_form(self, data):
        accomodation_types = {"house": "Дом", "new_house": "Строительство дома", "flat": "Квартира",
                              "new_flat": "Новостройка", "commercial": "Коммерческая", "apart": "Апартаменты"}
        symbols = {False: "❌", True: "✅"}
        citizenship = {"ru": "Российская Федерация", "different": "Другое"}


        self._msg = f"<b>Ваша анкета:</b> \n\n" \
                                 f"<b>ФИО:</b> {data.get('fio')}\n" \
                                 f"<b>Гражданство:</b> {citizenship[data.get('citizenship')]}\n" \
                                 f"<b>Размер ипотеки:</b> {data.get('estimated_mortgage_amount')}\n" \
                                 f"<b>Тип недвижимости:</b> {accomodation_types[data.get('accommodation_type')]}\n" \
                                 f"<b>Размер первого взноса:</b> {data.get('down_payment_amount')}\n" \
                                 f"<b>Срок ипотеки:</b> {data.get('mortgage_term')}\n" \
                                 f"<b>Дети после 2018:</b> {symbols[data.get('children_after_2018')]}\n" \
                                 f"<b>Наличие кредитов:</b> {symbols[data.get('credits_in_the_past')]}\n" \
                                 f"<b>Официальная работа:</b> {symbols[data.get('official_job')]}\n" \
                                 f"<b>Судимости:</b> {symbols[data.get('convictions')]}\n" \
                                 f"<b>Банкротство:</b> {symbols[data.get('bankruptcy')]}\n" \
                                 f"<b>Просрочки по платежам:</b> {symbols[data.get('late_payments')]}\n" \
                                 f"<b>Брак:</b> {symbols[data.get('marriage')]}\n" \
                                 f"<b>Количество детей:</b> {data.get('children_amount')}\n"

        approve_my_form_btn = InlineKeyboardButton('Сохранить ✅', callback_data='check_form_callback#approve_my_form_btn')
        disapprove_my_form_btn = InlineKeyboardButton('Отменить ❌', callback_data='check_form_callback#disapprove_my_form_btn')
        keyboard = InlineKeyboardMarkup().add(approve_my_form_btn).add(disapprove_my_form_btn)
        return keyboard


    async def form_final(self, state: FSMContext):
        with session_factory() as session:
            data = await state.get_data()
            form_control = UserFormControl(session)
            user_control = UserControl(session)
            user = await user_control.get(data.get("form_user_id"))
            user.user_fio = data.get("fio")
            await form_control.add(
            form_user_id = data.get("form_user_id"),
            user_fio = data.get("fio"),
            user_number = int(user.user_number),
            citizenship = data.get("citizenship"),
            estimated_mortgage_amount = data.get("estimated_mortgage_amount"),
            accommodation_type = data.get("accommodation_type"),
            down_payment_amount = data.get("down_payment_amount"),
            mortgage_term = data.get("mortgage_term"),
            children_after_2018 = data.get("children_after_2018"),
            credits_in_the_past = data.get("credits_in_the_past"),
            official_job = data.get("official_job"),
            convictions = data.get("convictions"),
            bankruptcy = data.get("bankruptcy"),
            late_payments = data.get("late_payments"),
            marriage = data.get("marriage"),
            children_amount = data.get("children_amount"),
            )
            session.commit()
            await state.finish()


    async def update_form(self, state):
        with session_factory() as session:
            data = await state.get_data()
            form_control = UserFormControl(session)
            user_control = UserControl(session)
            user_id = data.get("form_user_id")
            user = await user_control.get(user_id)
            user.user_fio = data.get("fio")
            form = await form_control.get(user_id)
            form.user_fio = data.get("fio")
            form.user_number = data.get("number")
            form.citizenship = data.get("citizenship")
            form.estimated_mortgage_amount = data.get("estimated_mortgage_amount")
            form.accommodation_type = data.get("accommodation_type")
            form.down_payment_amount = data.get("down_payment_amount")
            form.mortgage_term = data.get("mortgage_term")
            form.children_after_2018 = data.get("children_after_2018")
            form.credits_in_the_past = data.get("credits_in_the_past")
            form.official_job = data.get("official_job")
            form.convictions = data.get("convictions")
            form.bankruptcy = data.get("bankruptcy")
            form.late_payments = data.get("late_payments")
            form.marriage = data.get("marriage")
            form.children_amount = data.get("children_amount")
            session.commit()
            await state.finish()
