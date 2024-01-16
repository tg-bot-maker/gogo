from MagicPaginator import MagicKeyboardMarkup, ButtonPagination


def demo_handlers():
    # -------- ПРИМЕР ХЕНДЛЕРОВ ДЛЯ ПРАВИЛЬНОЙ РАБОТЫ КЛАССА ПАГИНАЦИИ
    @dp.message_handler(commands=['test'], state='*')
    async def test(message, state: FSMContext):
        list_data = {'callback_1': 'button_body_1', 'callback_2': 'button_body_2', 'callback_3': 'button_body_3'}
        amg = MagicKeyboardMarkup()  # Создаем экзембляр класса
        amg.pagination(list_data, 2)  # Пагинируем список в постраничный словарь
        keyboard = []
        button_0 = InlineKeyboardButton(text='◀️ОТМЕНА', callback_data='cancel_report')
        keyboard.append(button_0)
        magic.magic_markup(1)  # Получаем готовую клавиатуру с указанной страницей
        await state.update_data(magic=magic)
        await bot.send_message(message.from_user.id, 'test', reply_markup=magic.markup)
        await SystemEditor.test.set()

    # Принимаем нажатие на клавиши перелистывания
    @dp.callback_query_handler(lambda callback_query: callback_query.data.split('#')[0] == 'pages',
                               state=SystemEditor.test)
    async def start_my_cabinet(callback_query: types.CallbackQuery, state: FSMContext):
        magic = (await state.get_data()).get('magic')
        magic.page_switch(callback_query.data.split('#')[1])
        await bot.edit_message_text(text=f'Page {magic.currant_page}', chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id, reply_markup=magic.markup)
        await state.update_data(magic=magic)

    # Хендлер для обработки клавишь нажатий на товары
    @dp.callback_query_handler(lambda callback_query: callback_query.data.split('#')[0] == 'item',
                               state=SystemEditor.test)
    async def test_pagination(callback_query: types.CallbackQuery, state: FSMContext):
        keyboard = InlineKeyboardMarkup()
        button_0 = InlineKeyboardButton(text='◀️ОТМЕНА', callback_data='cancel_report')
        keyboard.row(button_0)
        await bot.edit_message_text(text=f'ТОВАР: {[callback_query.data.split("#")[1]]}\n',
                                    chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id, reply_markup=keyboard)


list_data = {'callback_1': 'button_body_1', 'callback_2': 'button_body_2', 'callback_3': 'button_body_3'}
test = ['горячий ключ', 'краснодар', 'москва']
amg = ButtonPagination(test, 2,)
keyboard = amg.pagination(random_callback_data=True)

