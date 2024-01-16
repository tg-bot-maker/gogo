import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from models.adapters.form_adapter import FormAdapter
from handlers.states import SG
from handlers.base_handlers import back_hendler_btn
from models.adapters.user_adapter import UserAdapter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from apscheduler.schedulers.asyncio import AsyncIOScheduler

symbols = {False: "❌", True: "✅"}

async def get_back_btn(question):
    return InlineKeyboardMarkup().add(InlineKeyboardButton(text="◀️   Назад    ", callback_data=f"previous_question#{question}"))


# fio
async def form_question_0(call: types.CallbackQuery, state: FSMContext, updating_form=False):
    form_adapter = FormAdapter()
    await state.update_data(call=call)
    await form_adapter.form_question_0()
    if updating_form is True:
        await state.update_data(updating_form=True)
        form = await form_adapter.get_form(call.from_user.id)
        await call.message.edit_text(text=form_adapter.message_text + f"\n<i>Было: {form.user_fio}</i>")
    else:
        await call.message.edit_text(text=form_adapter.message_text)
    await SG.citizenship.set()


# number пропускаем так как он вводится при регистрации
async def form_question_0_1(message: types.Message, state: FSMContext):
    form_adapter = FormAdapter()
    data = await state.get_data()
    call = data.get("call")
    updating_form = data.get("updating_form")
    await state.update_data(fio=message.text)
    await message.delete()
    await form_adapter.form_question_0_1()
    if updating_form is True:
        form = await form_adapter.get_form(call.from_user.id)
        await call.message.edit_text(text=form_adapter.message_text + f"\n<i>Было: {form.user_number}</i>", reply_markup=await get_back_btn("form_question_0"))
        await SG.citizenship.set()
    else:
        await call.message.edit_text(text=form_adapter.message_text, reply_markup=await get_back_btn("form_question_0"))
        await SG.citizenship.set()

#number_from_tg
async def number_from_tg(message: types.Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    form_adapter = FormAdapter()
    keyboard = await form_adapter.form_question_1()
    await message.answer("test")
    await message.delete()



# citizenship
async def form_question_1(message: types.Message, state: FSMContext):
    await state.update_data(fio=message.text)
    description = {"ru": "Российская Федерация", "different": "Другое"}
    data = await state.get_data()
    call = data.get("call")
    form_adapter = FormAdapter()
    data = await state.get_data()
    updating_form = data.get("updating_form")
    await message.delete()
    keyboard = await form_adapter.form_question_1()
    if updating_form is True:
        form = await form_adapter.get_form(call.from_user.id)
        await call.message.edit_text(text=form_adapter.message_text + f"\n<i>Было: {description[form.citizenship]}</i>", reply_markup=keyboard)
    else:
        await call.message.edit_text(text=form_adapter.message_text, reply_markup=keyboard)


async def q1_russian(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(call=call)
    await state.update_data(citizenship='ru')
    await form_question_2(call, state)


async def q1_different(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(call=call)
    await state.update_data(citizenship='different')
    await form_question_2(call, state)


# estimated_mortgage_amount
async def form_question_2(call: types.CallbackQuery, state: FSMContext):
    form_adapter = FormAdapter()
    await form_adapter.form_question_2()
    data = await state.get_data()
    updating_form = data.get("updating_form")
    if updating_form is True:
        form = await form_adapter.get_form(call.from_user.id)
        await call.message.edit_text(text=form_adapter.message_text + f"\n<i>Было: {form.estimated_mortgage_amount}</i>")
    else:
        await call.message.edit_text(text=form_adapter.message_text)
    await SG.accommodation_type.set()


# accommodation_type
async def form_question_3(message: types.Message, state: FSMContext):
    description = {"house": "Дом", "new_house": "Строительство дома", "flat": "Квартира", "new_flat": "Новостройка", "commercial": "Коммерческая", "apart": "Апартаменты"}
    await message.delete()
    form_adapter = FormAdapter()
    data = await state.get_data()
    call = data.get("call")
    updating_form = data.get("updating_form")


    try:
        await state.update_data(estimated_mortgage_amount=int(message.text))
        keyboard = await form_adapter.form_question_3()
        if updating_form is True:
            form = await form_adapter.get_form(call.from_user.id)
            await call.message.edit_text(text=form_adapter.message_text + f"\n<i>Было: {description[form.accommodation_type]}</i>", reply_markup=keyboard)
        else:
            await call.message.edit_text(text=form_adapter.message_text, reply_markup=keyboard)
    except ValueError:
        await form_adapter.form_question_2()
        await call.message.edit_text(text="<i>Необходимо ввести только цифры, без букв и других символов!</i>\n\n" + form_adapter.message_text)
        await SG.accommodation_type.set()



# down_payment_amount
async def form_question_4(call: types.CallbackQuery, state: FSMContext):
    btn_to_db_dict = {"accommodation_type_house_btn": "house", "accommodation_type_new_house_btn": "new_house",
                      "accommodation_type_flat_btn": "flat", "accommodation_type_new_flat_btn": "new_flat",
                      "accommodation_type_commercial_btn": "commercial", "accommodation_type_apart_btn":"apart"}
    await state.update_data(accommodation_type=btn_to_db_dict[call.data])
    form_adapter = FormAdapter()
    keyboard = await form_adapter.form_question_4()
    data = await state.get_data()
    updating_form = data.get("updating_form")
    if updating_form is True:
        form = await form_adapter.get_form(call.from_user.id)
        await call.message.edit_text(text=form_adapter.message_text + f"\n<i>Было: {form.down_payment_amount}</i>", reply_markup=keyboard)
    else:
        await call.message.edit_text(text=form_adapter.message_text, reply_markup=keyboard)
    await SG.mortgage_term.set()


async def q4_no_down_payment(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(down_payment_amount=0)
    form_adapter = FormAdapter()
    keyboard = await form_adapter.form_question_5()
    data = await state.get_data()
    updating_form = data.get("updating_form")
    if updating_form is True:
        form = await form_adapter.get_form(call.from_user.id)
        await call.message.edit_text(text=form_adapter.message_text + f"\n<i>Было: {form.mortgage_term}</i>", reply_markup=keyboard)
    else:
        await call.message.edit_text(text=form_adapter.message_text, reply_markup=keyboard)



# mortgage_term
async def form_question_5(message: types.Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    call = data.get("call")
    updating_form = data.get("updating_form")
    try:
        await state.update_data(down_payment_amount=int(message.text))
        form_adapter = FormAdapter()
        keyboard = await form_adapter.form_question_5()
        if updating_form is True:
            form = await form_adapter.get_form(call.from_user.id)
            await call.message.edit_text(text=form_adapter.message_text + f"\n<i>Было: {form.mortgage_term}</i>", reply_markup=keyboard)
        else:
            await call.message.edit_text(text=form_adapter.message_text, reply_markup=keyboard)
    except ValueError:
        form_adapter = FormAdapter()
        keyboard = await form_adapter.form_question_4()
        await call.message.edit_text(text="<i>Необходимо ввести только цифры, без букв и других символов!</i>\n\n" + form_adapter.message_text, reply_markup=keyboard)
        await SG.mortgage_term.set()



async def q5_call(call: types.CallbackQuery, state: FSMContext):
    form_adapter = FormAdapter()
    data = await state.get_data()
    updating_form = data.get("updating_form")
    if call.data.split("#")[1] == "different":
        await form_adapter.form_question_5_1()
        if updating_form is True:
            form = await form_adapter.get_form(call.from_user.id)
            await call.message.edit_text(text=form_adapter.message_text + f"\n<i>Было: {form.mortgage_term}</i>")
        else:
            await call.message.edit_text(text=form_adapter.message_text)
        await SG.children_after_2018.set()
    else:
        keyboard = await form_adapter.form_question_6()
        await state.update_data(mortgage_term=call.data.split("#")[1])
        if updating_form is True:
            form = await form_adapter.get_form(call.from_user.id)
            await call.message.edit_text(text=form_adapter.message_text + f"\n<i>Было: {symbols[form.children_after_2018]}</i>", reply_markup=keyboard)
        else:
            await call.message.edit_text(text=form_adapter.message_text, reply_markup=keyboard)


# children_after_2018
async def form_question_6(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data(mortgage_term=int(message.text))
    data = await state.get_data()
    call = data.get("call")
    updating_form = data.get("updating_form")
    form_adapter = FormAdapter()
    keyboard = await form_adapter.form_question_6()
    if updating_form is True:
        form = await form_adapter.get_form(call.from_user.id)
        await call.message.edit_text(text=form_adapter.message_text + f"\n<i>Было: {symbols[form.children_after_2018]}</i>", reply_markup=keyboard)
    else:
        await call.message.edit_text(text=form_adapter.message_text, reply_markup=keyboard)


async def q6_yes(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(children_after_2018=True)
    await form_question_7(call, state)

async def q6_no(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(children_after_2018=False)
    await form_question_7(call, state)


# credits_in_the_past
async def form_question_7(call: types.CallbackQuery, state: FSMContext):
    form_adapter = FormAdapter()
    data = await state.get_data()
    updating_form = data.get("updating_form")
    keyboard = await form_adapter.form_question_7()
    if updating_form is True:
        form = await form_adapter.get_form(call.from_user.id)
        await call.message.edit_text(text=form_adapter.message_text + f"\n<i>Было: {symbols[form.credits_in_the_past]}</i>", reply_markup=keyboard)
    else:
        await call.message.edit_text(text=form_adapter.message_text, reply_markup=keyboard)


async def q7_yes(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(credits_in_the_past=True)
    await form_question_8(call, state)

async def q7_no(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(credits_in_the_past=False)
    await form_question_8(call, state)


# official_job
async def form_question_8(call: types.CallbackQuery, state: FSMContext):
    form_adapter = FormAdapter()
    keyboard = await form_adapter.form_question_8()
    data = await state.get_data()
    updating_form = data.get("updating_form")
    if updating_form is True:
        form = await form_adapter.get_form(call.from_user.id)
        await call.message.edit_text(text=form_adapter.message_text + f"\n<i>Было: {symbols[form.official_job]}</i>", reply_markup=keyboard)
    else:
        await call.message.edit_text(text=form_adapter.message_text, reply_markup=keyboard)


async def q8_yes(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(official_job=True)
    await form_question_9(call, state)

async def q8_no(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(official_job=False)
    await form_question_9(call, state)



# convictions
async def form_question_9(call: types.CallbackQuery, state: FSMContext):
    form_adapter = FormAdapter()
    keyboard = await form_adapter.form_question_9()
    data = await state.get_data()
    updating_form = data.get("updating_form")
    if updating_form is True:
        form = await form_adapter.get_form(call.from_user.id)
        await call.message.edit_text(text=form_adapter.message_text + f"\n<i>Было: {symbols[form.convictions]}</i>", reply_markup=keyboard)
    else:
        await call.message.edit_text(text=form_adapter.message_text, reply_markup=keyboard)


async def q9_yes(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(convictions=True)
    await form_question_10(call, state)

async def q9_no(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(convictions=False)
    await form_question_10(call, state)


# bankruptcy
async def form_question_10(call: types.CallbackQuery, state: FSMContext):
    form_adapter = FormAdapter()
    keyboard = await form_adapter.form_question_10()
    data = await state.get_data()
    updating_form = data.get("updating_form")
    if updating_form is True:
        form = await form_adapter.get_form(call.from_user.id)
        await call.message.edit_text(text=form_adapter.message_text + f"\n<i>Было: {symbols[form.bankruptcy]}</i>", reply_markup=keyboard)
    else:
        await call.message.edit_text(text=form_adapter.message_text, reply_markup=keyboard)


async def q10_yes(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(bankruptcy=True)
    await form_question_11(call, state)

async def q10_no(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(bankruptcy=False)
    await form_question_11(call, state)



# late_payments
async def form_question_11(call: types.CallbackQuery, state: FSMContext):
    form_adapter = FormAdapter()
    keyboard = await form_adapter.form_question_11()
    data = await state.get_data()
    updating_form = data.get("updating_form")
    if updating_form is True:
        form = await form_adapter.get_form(call.from_user.id)
        await call.message.edit_text(text=form_adapter.message_text + f"\n<i>Было: {symbols[form.late_payments]}</i>", reply_markup=keyboard)
    else:
        await call.message.edit_text(text=form_adapter.message_text, reply_markup=keyboard)


async def q11_yes(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(late_payments=True)
    await form_question_12(call, state)

async def q11_no(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(late_payments=False)
    await form_question_12(call, state)



# marriage
async def form_question_12(call: types.CallbackQuery, state: FSMContext):
    form_adapter = FormAdapter()
    keyboard = await form_adapter.form_question_12()
    data = await state.get_data()
    updating_form = data.get("updating_form")
    if updating_form is True:
        form = await form_adapter.get_form(call.from_user.id)
        await call.message.edit_text(text=form_adapter.message_text + f"\n<i>Было: {symbols[form.marriage]}</i>", reply_markup=keyboard)
    else:
        await call.message.edit_text(text=form_adapter.message_text, reply_markup=keyboard)


async def q12_yes(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(marriage=True)
    await form_question_13(call, state)

async def q12_no(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(marriage=False)
    await form_question_13(call, state)


# children_amount
async def form_question_13(call: types.CallbackQuery, state: FSMContext):
    form_adapter = FormAdapter()
    keyboard = await form_adapter.form_question_13()
    await state.update_data(call=call)
    data = await state.get_data()
    updating_form = data.get("updating_form")
    if updating_form is True:
        form = await form_adapter.get_form(call.from_user.id)
        await call.message.edit_text(text=form_adapter.message_text + f"\n<i>Было: {form.children_amount}</i>", reply_markup=keyboard)
    else:
        await call.message.edit_text(text=form_adapter.message_text, reply_markup=keyboard)
    await SG.check_form.set()


async def q13_no_children(call: types.CallbackQuery, state: FSMContext, scheduler: AsyncIOScheduler):
    data = await state.get_data()
    call = data.get("call")
    await state.update_data(children_amount=0)
    await check_form(message=call, state=state, scheduler=scheduler)



#check form
async def check_form(message: types.Message, state: FSMContext, scheduler: AsyncIOScheduler):
    form_adapter = FormAdapter()
    data = await state.get_data()
    call = data.get("call")
    try:   #проверяю нет ли букв в ответе клиента
        if type(message) != types.callback_query.CallbackQuery:
            await state.update_data(children_amount=int(message.text))
            await message.delete()
        form_adapter = FormAdapter()
        data = await state.get_data()
        keyboard = await form_adapter.check_form(data)
        await call.message.edit_text(text=form_adapter._msg, reply_markup=keyboard)
    except ValueError:
        await message.delete()
        keyboard = await form_adapter.form_question_13()
        await call.message.edit_text(
            text="<i>Необходимо ввести только цифры, без букв и других символов!</i>\n\n" + form_adapter.message_text,
            reply_markup=keyboard)
        await SG.check_form.set()



async def check_form_callback(call: types.CallbackQuery, state: FSMContext, scheduler: AsyncIOScheduler):
    choice = call.data.split("#")[-1]
    if choice == "approve_my_form_btn":
        await form_final(call, state, scheduler)
    elif choice == "disapprove_my_form_btn":
        await call.message.edit_text("Анкета сброшена!")
        await asyncio.sleep(1)
        await back_hendler_btn(call, state)




# form_final
async def form_final(call: types.CallbackQuery, state: FSMContext, scheduler: AsyncIOScheduler):
    form_adapter = FormAdapter(call.from_user.id)
    data = await state.get_data()
    updating_form = data.get("updating_form")
    call = data.get("call")
    await state.update_data(form_user_id=call.from_user.id)
    if updating_form is None or updating_form is False:
        await form_adapter.form_final(state)
        # меняем этап на "check_credit_history"
        user_adapter = UserAdapter()
        await user_adapter.update_user_stage(call.from_user.id, "upload_docs", call, scheduler)
        await back_hendler_btn(call, state)

    elif updating_form is True:
        await form_adapter.update_form(state)
        await call.message.edit_text(text="Ваша анкета была обновлена!", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text="Вернуться в личный кабинет", callback_data="back_to_client_panel_btn")))
        # Добавить в бд дату последнего обновления анкеты и прошлые данные анкеты


def register_fill_form_handlers(dp: Dispatcher):
    dp.register_message_handler(
        form_question_3,
        state=SG.accommodation_type
    )
    dp.register_message_handler(
        form_question_5,
        state=SG.mortgage_term
    )
    dp.register_message_handler(
        form_question_6,
        state=SG.children_after_2018
    )
    dp.register_message_handler(
        form_final,
        state=SG.form_final
    )
    dp.register_message_handler(
        form_question_1,
        state=SG.citizenship
    )
    dp.register_message_handler(
        form_question_0_1,
        state=SG.number
    )
    dp.register_message_handler(
        check_form,
        state=SG.check_form
    )
    dp.register_message_handler(
        number_from_tg,
        content_types="contact",
        state="*"
    )
    dp.register_callback_query_handler(
        form_question_0,
        lambda callback_query: callback_query.data == 'form_question_0',
        state='*'
    )
    dp.register_callback_query_handler(
        q1_russian,
        lambda callback_query: callback_query.data == 'russian_citizenship_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        q1_different,
        lambda callback_query: callback_query.data == 'q1_different_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        form_question_4,
        lambda callback_query: callback_query.data in ["accommodation_type_house_btn",
                                                       "accommodation_type_new_house_btn",
                                                       "accommodation_type_flat_btn",
                                                       "accommodation_type_new_flat_btn",
                                                       "accommodation_type_apart_btn",
                                                       "accommodation_type_commercial_btn"],
        state='*'
    )
    dp.register_callback_query_handler(
        q6_yes,
        lambda callback_query: callback_query.data == "yes_children_after_2018_btn",
        state='*'
    )
    dp.register_callback_query_handler(
        q6_no,
        lambda callback_query: callback_query.data == "no_children_after_2018_btn",
        state='*'
    )
    dp.register_callback_query_handler(
        q7_yes,
        lambda callback_query: callback_query.data == "yes_credits_in_the_past_btn",
        state='*'
    )
    dp.register_callback_query_handler(
        q7_no,
        lambda callback_query: callback_query.data == "no_credits_in_the_past_btn",
        state='*'
    )
    dp.register_callback_query_handler(
        q8_yes,
        lambda callback_query: callback_query.data == "yes_official_job_btn",
        state='*'
    )
    dp.register_callback_query_handler(
        q8_no,
        lambda callback_query: callback_query.data == "no_official_job_btn",
        state='*'
    )
    dp.register_callback_query_handler(
        q9_yes,
        lambda callback_query: callback_query.data == "yes_convictions_btn",
        state='*'
    )
    dp.register_callback_query_handler(
        q9_no,
        lambda callback_query: callback_query.data == "no_convictions_btn",
        state='*'
    )
    dp.register_callback_query_handler(
        q10_yes,
        lambda callback_query: callback_query.data == "yes_bankruptcy_btn",
        state='*'
    )
    dp.register_callback_query_handler(
        q10_no,
        lambda callback_query: callback_query.data == "no_bankruptcy_btn",
        state='*'
    )
    dp.register_callback_query_handler(
        q11_yes,
        lambda callback_query: callback_query.data == "yes_late_payments_btn",
        state='*'
    )
    dp.register_callback_query_handler(
        q11_no,
        lambda callback_query: callback_query.data == "no_late_payments_btn",
        state='*'
    )
    dp.register_callback_query_handler(
        q12_yes,
        lambda callback_query: callback_query.data == "yes_marriage_btn",
        state='*'
    )
    dp.register_callback_query_handler(
        q12_no,
        lambda callback_query: callback_query.data == "no_marriage_btn",
        state='*'
    )
    dp.register_callback_query_handler(
        q13_no_children,
        lambda callback_query: callback_query.data == "q13_no_children_btn",
        state='*'
    )
    dp.register_callback_query_handler(
        q4_no_down_payment,
        lambda callback_query: callback_query.data == "q4_no_down_payment",
        state='*'
    )
    dp.register_callback_query_handler(
        check_form_callback,
        lambda callback_query: callback_query.data.split("#")[0] == "check_form_callback",
        state='*'
    )
    dp.register_callback_query_handler(
        q5_call,
        lambda callback_query: callback_query.data.split("#")[0] == 'form_question_5_btn',
        state='*'
    )
