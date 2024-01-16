from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from models.adapters.pick_credit_product_adapter import PickProductAdapter
from models.adapters.admin_panel_adapter import AdminPanelAdapter
from models.adapters.user_adapter import UserAdapter
from handlers.states import SG
from handlers.base_handlers import back_hendler_btn
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def pick_credit_product(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    pick_product_adapter = PickProductAdapter()
    keyboard = await pick_product_adapter.pick_credit_product()
    await state.update_data(call=call)
    await call.message.edit_text(text=pick_product_adapter.message_text, reply_markup=keyboard)


async def pick_product_key(call: types.CallbackQuery, state: FSMContext):
    mortgage_key_text = """Почему выгодно с нами? 
Вы хотите выгодные условия по ипотеке
У вас плохая кредитная история
Нет или не можете подтвердить официальный доход
У вас уже есть отказ банка
Недостаточный первоначальный взнос
Вы в декрете, блогер, самозанятый, фрилансер, собственник бизнеса или ИП

Как мы работаем? 
Взаимодействие с клиентом происходит онлайн по всей территории России, вам не нужно будет ехать к нам в офис и в банки. 

Услуга включает в себя:
▪️ проверка кредитной истории 
▪️ анализ текущей ситуации клиента 
▪️ стратегия одобрения, с учетом всех нюансов клиента 
▪️ подбор банков и выгодных ипотечных программ с минимальными ставками 
▪️ подбор льготных госпрограмм и использование маткапитала 
▪️ заполнение анкет и заявлений 
▪️ подача заявок в банки (без вашего выезда в банки) 
▪️ партнерские преференции от банков со сниженной % ставкой 
▪️ получение положительного решения от банка, исходя из нужной суммы и ранее оговорённой % ставки с клиентом 
▪️ рекомендации юриста по сопровождению сделки и юридической проверки объекта 

Результат услуги:
положительное решение с выгодными условиями координация дальнейших действий контакты банка экономия на оформлении ипотеки до 50 000 руб. 
В подарок:
 • Список необходимых документов для проведения сделки
 • Скидка до 50% на оформление страховки в нашей компании
 • Консультация по налоговым вычетам
 • Подбор страховой компании и оформление полиса со скидкой до 50%
 • Подбор новостройки в г. Москва и МО (кроме ПИК и Гранель), г.Санкт-Петербург и ЛО, Краснодар
Стоимость: от 140 000 руб.

Мы работаем с топовыми банками России. Подробную информацию об условиях работы и стоимости можно получить на бесплатной консультации"""

    if call.data.split("#")[1] == "mortgage_btn":
        text = mortgage_key_text
    elif call.data.split("#")[1] == "buy_property_btn":
        text = "Помощь в подборе недвижимости, покупке и оформлении сделки."
    elif call.data.split("#")[1] == "sell_property_btn":
        text = "Помощь в продаже вашей недвижимости и сопровождение сделки."
    else:
        raise ValueError(f"Unknown callback data - {call.data.split('#')[1]}")
    pick_product_adapter = PickProductAdapter()
    keyboard = await pick_product_adapter.pick_credit_product_choice(call.data.split("#")[1])
    await call.message.edit_text(text=text, reply_markup=keyboard)





async def pick_product_choice_btn(call: types.CallbackQuery, state: FSMContext, scheduler: AsyncIOScheduler):
    choice = call.data.split("#")[1]
    stages_dict = {"mortgage_btn": "form", "buy_property_btn": "buy_estate_form", "sell_property_btn": "sell_estate_form"}
    user_id = call.from_user.id
    pick_product_adapter = PickProductAdapter()
    user_adapter = UserAdapter()
    await pick_product_adapter.pick_credit_product_finish(user_id, choice)
    await user_adapter.update_user_stage(user_id, stages_dict[choice], call, scheduler)
    await back_hendler_btn(call, state)



def register_pick_credit_product_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        pick_credit_product,
        lambda callback_query: callback_query.data == 'pick_credit_product_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        pick_product_key,
        lambda callback_query: callback_query.data.split("#")[0] == 'pick_product_choice',
        state='*'
    )
    dp.register_callback_query_handler(
        pick_product_choice_btn,
        lambda callback_query: callback_query.data.split("#")[0] == 'pick_credit_product_choice',
        state='*'
    )
