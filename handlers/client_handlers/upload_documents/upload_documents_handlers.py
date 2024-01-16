import asyncio
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ContentTypeFilter
from handlers.states import SG
from models.adapters.history_adapter import HistoryAdapter
from models.adapters.form_adapter import FormAdapter
from models.adapters.upload_documents_adapter import UploadDocumentsAdapter
from models.utils.google_api import upload_files_to_drive
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import os

async def upload_documents_btn(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    upload_documents_adapter = UploadDocumentsAdapter()
    keyboard = await upload_documents_adapter.upload_documents_btn(call.from_user.id)
    msg = upload_documents_adapter.message_text
    await state.update_data(call=call)
    await call.message.delete()
    await call.message.answer_photo(photo=open("files/templates/documents_photo.jpg", "rb"), caption=msg, reply_markup=keyboard)


async def upload_documents_passport_btn(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    upload_documents_adapter = UploadDocumentsAdapter()
    was_uploaded = await upload_documents_adapter.was_uploaded(call.message.chat.id)
    if was_uploaded == False:
        await state.update_data(call=call)
        text = await upload_documents_adapter.upload_documents_passport_btn("2-3")
        with open("files/templates/ruspasport_23.jpeg", "rb") as photo:
            await call.message.edit_media(media=types.InputMediaPhoto(media=photo, caption=text), reply_markup=None)
        await SG.upload_documents_passport_page23.set()
    else:
        with open("files/templates/documents_photo.jpg", "rb") as photo:
            await call.message.edit_media(media=types.InputMediaPhoto(media=photo, caption=was_uploaded[0]), reply_markup=was_uploaded[1])


async def upload_documents_passport_page23(message: types.Message, state: FSMContext):
    data = await state.get_data()
    call = data.get("call")
    file_extension = ".jpg"
    file_name = "passport_page23#" + str(message.from_user.id) + file_extension
    file_path = os.path.join(os.getcwd() + f"/files/user_documents/{message.from_user.id}", file_name)
    await message.photo[-1].download(destination_file=file_path)
    await upload_files_to_drive(user_id=message.from_user.id, file_name=file_name)
    await message.delete()

    upload_documents_adapter = UploadDocumentsAdapter()
    text = await upload_documents_adapter.upload_documents_passport_btn("4-5")
    with open("files/templates/rupassport_45.jpeg", "rb") as photo:
        await call.message.edit_media(media=types.InputMediaPhoto(media=photo, caption=text), reply_markup=None)
    await SG.upload_documents_passport_page45.set()


async def upload_documents_passport_page45(message: types.Message, state: FSMContext):
    data = await state.get_data()
    call = data.get("call")

    file_extension = ".jpg"
    file_name = "passport_page45#" + str(message.from_user.id) + file_extension
    file_path = os.path.join(os.getcwd() + f"/files/user_documents/{message.from_user.id}", file_name)
    await message.photo[-1].download(destination_file=file_path)
    await upload_files_to_drive(user_id=message.from_user.id, file_name=file_name)
    await message.delete()

    user_documents_passport23 = os.path.join(os.getcwd() + f"/files/user_documents/{message.from_user.id}", "passport_page23#" + str(message.from_user.id) + file_extension)
    user_documents_passport45 = os.path.join(os.getcwd() + f"/files/user_documents/{message.from_user.id}", "passport_page45#" + str(message.from_user.id) + file_extension)

    upload_documents_adapter = UploadDocumentsAdapter()
    await upload_documents_adapter.upload_passport(message.from_user.id, user_documents_passport23,
                                                   user_documents_passport45)
    await upload_snils_btn(call, state)



async def upload_snils_btn(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await state.update_data(call=call)
    upload_documents_adapter = UploadDocumentsAdapter()
    snils_was_uploaded = await upload_documents_adapter.snils_was_uploaded(call.message.chat.id)
    if snils_was_uploaded == False:
        text, keyboard = await upload_documents_adapter.upload_snils_btn()
        with open("files/templates/snils.jpeg", "rb") as photo:
            await call.message.edit_media(media=types.InputMediaPhoto(media=photo, caption=text), reply_markup=keyboard)
        await SG.upload_snils.set()
    else:
        with open("files/templates/documents_photo.jpg", "rb") as photo:
            await call.message.edit_media(media=types.InputMediaPhoto(media=photo, caption=snils_was_uploaded[0]), reply_markup=snils_was_uploaded[1])


async def upload_snils(message: types.Message, state: FSMContext, scheduler: AsyncIOScheduler):
    data = await state.get_data()
    call = data.get("call")

    file_extension = ".jpg"
    file_name = "snils#" + str(message.from_user.id) + file_extension
    file_path = os.path.join(os.getcwd() + f"/files/user_documents/{message.from_user.id}", file_name)
    await message.photo[-1].download(destination_file=file_path)
    await upload_files_to_drive(user_id=message.from_user.id, file_name=file_name)
    await message.delete()

    upload_documents_adapter = UploadDocumentsAdapter()
    await upload_documents_adapter.upload_snils(message.from_user.id, file_path, call, scheduler)
    await upload_snils_btn(call, state)



def register_upload_documents_handlers(dp: Dispatcher):
    dp.register_message_handler(
        upload_documents_passport_page23,
        content_types=types.ContentType.PHOTO,
        state=SG.upload_documents_passport_page23,
    )
    dp.register_message_handler(
        upload_documents_passport_page45,
        content_types=types.ContentType.PHOTO,
        state=SG.upload_documents_passport_page45,
    )
    dp.register_message_handler(
        upload_snils,
        content_types=types.ContentType.PHOTO,
        state=SG.upload_snils,
    )
    dp.register_callback_query_handler(
        upload_documents_btn,
        lambda callback_query: callback_query.data in ['upload_documents_btn','back_to_upload_documents_btn'],
        state='*'
    )
    dp.register_callback_query_handler(
        upload_documents_passport_btn,
        lambda callback_query: callback_query.data == 'upload_documents_passport_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        upload_snils_btn,
        lambda callback_query: callback_query.data == 'upload_documents_snils_btn',
        state='*'
    )
