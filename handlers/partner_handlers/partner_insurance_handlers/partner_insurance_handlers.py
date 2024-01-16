from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def partner_menu_insurance_btn(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_partner_menu_btn'))
    await call.message.edit_text(text="По вопросам страховки обратитесь, пожалуйста, к @himyanta", reply_markup=keyboard)





def register_partner_insurance_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        partner_menu_insurance_btn,
        lambda callback_query: callback_query.data == 'partner_menu_insurance_btn',
        state='*'
    )
