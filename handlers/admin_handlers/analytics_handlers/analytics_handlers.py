from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from handlers.states import SG
from models.adapters.base_adapter import BaseAdapter
from models.adapters.user_adapter import UserAdapter
from models.adapters.upload_documents_adapter import UploadDocumentsAdapter
from models.adapters.form_adapter import FormAdapter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pagination.MagicPaginator import ButtonPagination
from aiogram.utils import exceptions
from configs.config import stages






async def analytics_btn(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(call=call)
    base_adapter = BaseAdapter()
    keyboard_data = await base_adapter.get_users_as_buttons()
    keyboard_data = dict(reversed(keyboard_data.items()))
    custom_keyboard = [InlineKeyboardButton(text='◀︎', callback_data='back_to_admin_menu_btn')]
    paginator = ButtonPagination(button_data=keyboard_data, amount_elements=5)
    await state.update_data(paginator=paginator)
    try:
        keyboard = paginator.pagination(custom_keyboard=custom_keyboard)
        await call.message.edit_text(text="<b>Выберите пользователя:</b>", reply_markup=keyboard)
        await SG.user_list_pagination.set()
    except KeyError:
        await call.message.edit_text(text="<b>Пользователей пока нет!</b>")



async def go_back_to_analytics_btn(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await analytics_btn(call, state)


async def view_detail_user(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user_id = int(call.data.split("#")[2])
    base_adapter = BaseAdapter(user_id)
    form_adapter = FormAdapter()
    user = await base_adapter.get_user(user_id)
    form = await form_adapter.get_form(user_id)
    await state.update_data(user_id=user_id)
    documents_adapter = UploadDocumentsAdapter()
    drive_link = await documents_adapter.get_drive_link(user_id)

    # нажал старт
    if user.user_number is None and form is None:
        user_fio = "Не заполнено"
        user_number = "Не заполнено"
        keyboard = await base_adapter.analytics_kb(show_form_button=False)
    # прошел регистрацию
    elif user.user_number is not None and form is None:
        user_fio = "Не заполнено"
        user_number = user.user_number
        keyboard = await base_adapter.analytics_kb(show_form_button=False)
    # заполнил анкету
    else:
        user_fio = user.user_fio
        user_number = user.user_number
        keyboard = await base_adapter.analytics_kb(show_form_button=True)





    products = {"mortgage_btn": "Ипотека под ключ", "mortgage_new_flat_btn": "Покупка новостройки под ключ", "None": "Пока не выбран" }


    if user.user_manager_id != 0000000000:
        partner = await base_adapter.get_user(user.user_manager_id)
        partner_name = f"@{partner.user_name}"
    else:
        partner_name = "Без партнера"
    text = "<b>Аналитика</b>  🔎\n\n"\
           f"<b>------------------------</b>\n" \
           f"<b>Username:</b> @{user.user_name}\n" \
           f"<b>Telegram ID:</b> <code>{str(user.user_id)}</code>\n" \
           f"<b>Дата регистрации:</b> {user.register_date}\n" \
           f"<b>Имя:</b> {user_fio}\n" \
           f"<b>Телефон:</b> <code>{user_number}</code>\n\n" \
           f"<b>📈 Этап:</b> {stages[user.user_stage]}\n" \
           f"<b>📍 Выбранный продукт:</b> {products[str(user.product_choice)]}\n" \
           f"<b>🔗 Ссылка на файлы:</b> {drive_link}\n" \
           f"<b>🧲 Партнер клиента:</b> {partner_name}"
    await call.message.edit_text(text=text, reply_markup=keyboard)


async def show_form(call: types.CallbackQuery, state: FSMContext):
    await SG.user_list_pagination.set()
    accomodation_types = {"house": "Дом", "new_house": "Строительство дома", "flat": "Квартира", "new_flat": "Новостройка", "commercial": "Коммерческая", "apart": "Апартаменты"}
    symbols = {False:"❌", True:"✅"}
    citizenship = {"ru": "Российская Федерация", "different": "Другое"}

    data = await state.get_data()
    user_id = data.get("user_id")
    keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('◀️   Назад    ', callback_data=f'item#user_number#{user_id}'))
    form_adapter = FormAdapter()
    form = await form_adapter.get_form(user_id)
    await call.message.edit_text(f"<b>ID Клиента:</b> {form.form_user_id}\n" 
                                 f"<b>Гражданство:</b> {citizenship[form.citizenship]}\n" 
                                 f"<b>Размер ипотеки:</b> {form.estimated_mortgage_amount}\n" 
                                 f"<b>Тип недвижимости:</b> {accomodation_types[form.accommodation_type]}\n" 
                                 f"<b>Размер первого взноса:</b> {form.down_payment_amount}\n"
                                 f"<b>Срок ипотеки:</b> {form.mortgage_term}\n"
                                 f"<b>Дети после 2018:</b> {symbols[form.children_after_2018]}\n"
                                 f"<b>Наличие кредитов:</b> {symbols[form.credits_in_the_past]}\n"
                                 f"<b>Официальная работа:</b> {symbols[form.official_job]}\n"
                                 f"<b>Судимости:</b> {symbols[form.convictions]}\n"
                                 f"<b>Банкротство:</b> {symbols[form.bankruptcy]}\n"
                                 f"<b>Просрочки по платежам:</b> {symbols[form.late_payments]}\n"
                                 f"<b>Брак:</b> {symbols[form.marriage]}\n"
                                 f"<b>Количество детей:</b> {form.children_amount}\n",
                                 reply_markup=keyboard)



# pagination handler
async def user_list_pagination(call: types.CallbackQuery, state: FSMContext):
    paginator = (await state.get_data()).get('paginator')
    keyboard = paginator.page_switch(call.data.split('#')[1])
    try:
        await call.message.edit_text(text="<b>Выберите пользователя:</b>",
                                       reply_markup=keyboard)
        await state.update_data(paginator=paginator)
    except exceptions.MessageNotModified:
        await call.answer(text='Больше нет пользователей!', show_alert=True)






def register_analytics_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        analytics_btn,
        lambda callback_query: callback_query.data == 'admin_analytics_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        user_list_pagination,
        lambda callback_query: callback_query.data.split("#")[0] == 'amg',
        state=SG.user_list_pagination
    )
    dp.register_callback_query_handler(
        view_detail_user,
        lambda callback_query: callback_query.data.split("#")[1] == "user_number",
        state=SG.user_list_pagination,
    )
    dp.register_callback_query_handler(
        show_form,
        lambda callback_query: callback_query.data == "show_form",
        state="*"
    )
    dp.register_callback_query_handler(
        go_back_to_analytics_btn,
        lambda callback_query: callback_query.data == "go_back_to_analytics_btn",
        state="*"
    )