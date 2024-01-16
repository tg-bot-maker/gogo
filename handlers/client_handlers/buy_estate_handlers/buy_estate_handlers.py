from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def check_the_objects_btn(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    webAppTest = types.WebAppInfo(url="https://max-test-domain.site/get_map1", isExpanded=True)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Категория номер один", web_app=webAppTest))
    keyboard.add(InlineKeyboardButton(text="Категория номер два", web_app=webAppTest))
    keyboard.add(InlineKeyboardButton(text='◀︎', callback_data='back_to_admin_menu_btn'))
    await call.message.edit_text(text="<b>Выберите категорию:</b>", reply_markup=keyboard)






def register_buy_estate_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        check_the_objects_btn,
        lambda callback_query: callback_query.data == "check_the_objects_btn",
        state='*'
    )