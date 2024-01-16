from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from models.adapters.partners_adapter import PartnersAdapter
from models.adapters.user_adapter import UserAdapter
from models.adapters.base_adapter import BaseAdapter
from models.adapters.upload_documents_adapter import UploadDocumentsAdapter
from models.adapters.form_adapter import FormAdapter
from models.adapters.meetings_adapter import MeetingsAdapter
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pagination.MagicPaginator import ButtonPagination
from aiogram.utils import exceptions


async def meetings_btn(call: types.CallbackQuery, state: FSMContext):
    meetings_adapter = MeetingsAdapter()
    keyboard = await meetings_adapter.meetings_btn()
    await call.message.edit_text(text=meetings_adapter._msg, reply_markup=keyboard)



async def meetings_message_templates_btn(call: types.CallbackQuery, state: FSMContext):
    meetings_adapter = MeetingsAdapter()
    keyboard = await meetings_adapter.meetings_message_templates_btn()
    await call.message.edit_text(text=meetings_adapter._msg, reply_markup=keyboard)






async def templates_in_dev(call: types.CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text='◀︎', callback_data='meetings_message_templates_btn'))
    await call.message.edit_text(text="<b>Шаблон в разработке 📝</b>", reply_markup=keyboard)


def register_meetings_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        meetings_btn,
        lambda callback_query: callback_query.data == 'meetings_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        meetings_message_templates_btn,
        lambda callback_query: callback_query.data == 'meetings_message_templates_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        templates_in_dev,
        lambda callback_query: callback_query.data in ["meeting_reminder_template_btn", "meeting_dox_list_template_btn"],
        state='*'
    )



