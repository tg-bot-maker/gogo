import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ContentTypeFilter
from handlers.states import SG
from models.adapters.history_adapter import HistoryAdapter
from models.adapters.base_adapter import BaseAdapter
from handlers.base_handlers import back_hendler_btn
from models.utils.google_api import upload_files_to_drive
from models.adapters.upload_documents_adapter import UploadDocumentsAdapter
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os


async def check_credit_history_btn(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    history_adapter = HistoryAdapter()
    keyboard = await history_adapter.check_credit_history_btn(call.from_user.id)
    msg = history_adapter.message_text
    await state.update_data(call=call)
    if call.message.text:
        await call.message.edit_text(text=msg, reply_markup=keyboard)
    else:
        await call.message.delete()
        await call.message.answer(text=msg, reply_markup=keyboard)


async def check_done_no_debts_btn(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    history_adapter = HistoryAdapter()
    keyboard = await history_adapter.check_done_no_debts_btn(call.from_user.id)
    msg = history_adapter.message_text
    await call.message.delete()
    await call.message.answer(text=msg, reply_markup=keyboard)



async def check_history_bki_btn(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    history_adapter = HistoryAdapter()
    keyboard = await history_adapter.check_history_bki_btn()
    msg = history_adapter.message_text
    await state.update_data(call=call)
    if call.message.text:
        await call.message.edit_text(text=msg, reply_markup=keyboard)
    else:
        await call.message.delete()
        await call.message.answer(text=msg, reply_markup=keyboard)



async def history_view_video_instruction_bki_btn(call: types.CallbackQuery, state: FSMContext):
    history_adapter = HistoryAdapter()
    keyboard = await history_adapter.history_view_video_instruction_bki_btn()
    await state.update_data(call=call)
    await call.message.delete()
    await call.message.answer_video(video="BAACAgUAAxkBAAIII2TsptY7cjsdrPDFnfVPRHV-_SWUAAJ-CwACfgphV3lconNdNDFWMAQ", reply_markup=keyboard)





async def check_history_okb_btn(call: types.CallbackQuery, state: FSMContext):
    history_adapter = HistoryAdapter()
    keyboard = await history_adapter.check_history_okb_btn()
    msg = history_adapter.message_text
    data = await state.get_data()
    call = data.get('call')
    if call.message.text:
        await call.message.edit_text(text=msg, reply_markup=keyboard)
    else:
        await call.message.delete()
        await call.message.answer(text=msg, reply_markup=keyboard)



async def history_view_video_instruction_okb_btn(call: types.CallbackQuery, state: FSMContext):
    history_adapter = HistoryAdapter()
    keyboard = await history_adapter.history_view_video_instruction_okb_btn()
    await call.message.delete()
    await call.message.answer_video(video="BAACAgUAAxkBAAIDk2SvU4jM3SyVKRFnEVfFumPupRqRAAI-CQACg7CAVSCGcvO9DOylLwQ", reply_markup=keyboard)


async def history_check_debts_btn(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await state.update_data(call=call)
    history_adapter = HistoryAdapter()
    keyboard = await history_adapter.check_debts_btn()
    with open("files/templates/fssp.jpg", "rb") as file:
        await call.message.reply_photo(photo=file, reply_markup=keyboard)
    await call.message.delete()



async def upload_file_okb_btn(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(call=call)
    history_adapter = HistoryAdapter()
    keyboard, take_file = await history_adapter.upload_file_okb_btn(call.message.chat.id)
    msg = history_adapter.message_text
    await call.message.edit_text(text=msg, reply_markup=keyboard)
    if take_file:
        await SG.upload_file_okb.set()


async def upload_file_bki_btn(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(call=call)
    history_adapter = HistoryAdapter()
    keyboard, take_file = await history_adapter.upload_file_bki_btn(call.message.chat.id)
    msg = history_adapter.message_text
    await call.message.edit_text(text=msg, reply_markup=keyboard)
    if take_file:
        await SG.upload_file_bki.set()



async def upload_bki(message: types.Message, state: FSMContext, scheduler: AsyncIOScheduler):
    data = await state.get_data()
    call = data.get('call')
    await state.finish()
    if message.document.mime_type == "application/pdf":
        file_name = "bki_file#" + str(message.from_user.id) + ".pdf"
        file_path = os.path.join(os.getcwd() + f"/files/user_documents/{message.from_user.id}", file_name)
        await message.document.download(destination_file=file_path)
        folder_link = await upload_files_to_drive(message.from_user.id, file_name)
        upload_documents_adapter = UploadDocumentsAdapter()
        await upload_documents_adapter.write_drive_link_to_db(message.from_user.id, folder_link)
        history_adapter = HistoryAdapter()
        new_stage = await history_adapter.add_bki(message.from_user.id, file_path, call, scheduler)
    elif message.text is None:
        await call.message.edit_text(text="Неверный формат файла")
        await asyncio.sleep(2)
        new_stage = False
    else:
        await call.message.edit_text(text="Неверный формат файла")
        await asyncio.sleep(2)
        new_stage = False

    await message.delete()

    if new_stage:
        await back_hendler_btn(call, state)
    else:
        await upload_file_bki_btn(call, state)


async def upload_okb(message: types.Message, state: FSMContext, scheduler: AsyncIOScheduler):
    data = await state.get_data()
    call = data.get('call')
    if message.document.mime_type == "application/pdf":
        file_name = "okb_file#" + str(message.from_user.id) + ".pdf"
        file_path = os.path.join(os.getcwd() + f"/files/user_documents/{message.from_user.id}", file_name)
        await message.document.download(destination_file=file_path)
        await upload_files_to_drive(message.from_user.id, file_name)
        history_adapter = HistoryAdapter()
        new_stage = await history_adapter.add_okb(message.from_user.id, file_path, call, scheduler)
    else:
        await call.message.edit_text(text="Неверный формат файла")
        await asyncio.sleep(2)
        new_stage = False

    await message.delete()

    if new_stage:
        await back_hendler_btn(call, state)
    else:
        await upload_file_okb_btn(call, state)



async def upload_history_bki_type_hint(message: types.Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    call = data.get("call")
    history_adapter = HistoryAdapter()
    keyboard = await history_adapter.check_history_bki_btn()
    msg = history_adapter.message_text
    await call.message.edit_text(text=msg+"\n\n<b><i>Обратите внимание, что вам необходимо скачать "
                                 "файл с вашей кредитной историей и прислать в бот "
                                 "именно файл, а не ссылку или скриншот.\nДля загрузки файла в бот нажмите кнопку ниже 👇</i></b>", reply_markup=keyboard, disable_web_page_preview=True)

async def upload_history_okb_type_hint(message: types.Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    call = data.get("call")
    history_adapter = HistoryAdapter()
    keyboard = await history_adapter.check_history_okb_btn()
    msg = history_adapter.message_text
    await call.message.edit_text(text=msg+"\n\n<b><i>Обратите внимание, что вам необходимо скачать "
                                 "файл с вашей кредитной историей и прислать в бот "
                                 "именно файл, а не ссылку или скриншот.\nДля загрузки файла в бот нажмите кнопку ниже 👇</i></b>", reply_markup=keyboard, disable_web_page_preview=True)


async def video_id(message):
    print(message)


async def layer_to_save_call(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(call=call)
    await check_history_okb_btn(call, state)

async def in_dev(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    base_adapter = BaseAdapter()
    keyboard = await base_adapter.back_kb()
    await call.message.edit_caption("В разработке", reply_markup=keyboard)

def register_check_credit_history_handlers(dp: Dispatcher):
    dp.register_message_handler(
        upload_bki,
        content_types=types.ContentType.DOCUMENT,
        state=SG.upload_file_bki,
    )
    dp.register_message_handler(
        video_id,
        content_types=types.ContentType.VIDEO,
        state="*",
    )
    dp.register_message_handler(
        upload_history_bki_type_hint,
        content_types=types.ContentType.TEXT,
        state=SG.upload_file_bki,
    )
    dp.register_message_handler(
        upload_history_bki_type_hint,
        content_types=types.ContentType.PHOTO,
        state=SG.upload_file_bki,
    )
    dp.register_message_handler(
        upload_history_okb_type_hint,
        content_types=types.ContentType.TEXT,
        state=SG.upload_file_okb,
    )
    dp.register_message_handler(
        upload_history_okb_type_hint,
        content_types=types.ContentType.PHOTO,
        state=SG.upload_file_okb,
    )
    dp.register_message_handler(
        upload_okb,
        content_types=types.ContentType.DOCUMENT,
        state=SG.upload_file_okb,
    )
    dp.register_callback_query_handler(
        check_credit_history_btn,
        lambda callback_query: callback_query.data == 'check_credit_history_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        history_view_video_instruction_bki_btn,
        lambda callback_query: callback_query.data == 'history_view_video_instruction_bki_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        check_history_bki_btn,
        lambda callback_query: callback_query.data == 'back_to_check_credit_history_bki_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        check_history_bki_btn,
        lambda callback_query: callback_query.data == 'history_check_bki_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        history_view_video_instruction_okb_btn,
        lambda callback_query: callback_query.data == 'history_view_video_instruction_okb_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        check_history_okb_btn,
        lambda callback_query: callback_query.data == 'back_to_check_credit_history_okb_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        check_history_okb_btn,
        lambda callback_query: callback_query.data == 'history_check_okb_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        check_credit_history_btn,
        lambda callback_query: callback_query.data == 'back_to_check_credit_history_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        check_history_okb_btn,
        lambda callback_query: callback_query.data == 'back_to_check_credit_history_okb_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        check_history_bki_btn,
        lambda callback_query: callback_query.data == 'back_to_check_credit_history_bki_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        history_check_debts_btn,
        lambda callback_query: callback_query.data == 'history_check_debts_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        upload_file_okb_btn,
        lambda callback_query: callback_query.data == 'upload_file_okb_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        upload_file_bki_btn,
        lambda callback_query: callback_query.data == 'upload_file_bki_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        check_done_no_debts_btn,
        lambda callback_query: callback_query.data == 'check_done_no_debts_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        layer_to_save_call,
        lambda callback_query: callback_query.data == 'to_ltsc_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        in_dev,
        lambda callback_query: callback_query.data == 'in_dev',
        state='*'
    )

