from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from handlers.states import SG
from models.adapters.user_archive_adapter import UserArchiveAdapter
from models.utils import encrypto



async def add_client_to_archive_btn(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(call=call)
    user_archive_adapter = UserArchiveAdapter()
    keyboard = await user_archive_adapter.add_to_archive_btn()
    await call.message.edit_text(text=user_archive_adapter._msg, reply_markup=keyboard)
    await SG.add_to_archive_fio.set()



async def get_fio(message: types.Message, state: FSMContext):
    data = await state.get_data()
    call = data.get("call")
    await state.update_data(fio=str(message.text))
    await message.delete()
    user_archive_adapter = UserArchiveAdapter()
    keyboard = await user_archive_adapter.add_to_archive_get_fio()
    await call.message.edit_text(text=user_archive_adapter._msg, reply_markup=keyboard)
    await SG.add_to_archive_number.set()


async def get_number(message: types.Message, state: FSMContext):
    data = await state.get_data()
    call = data.get("call")
    await state.update_data(number=str(message.text))
    await message.delete()
    user_archive_adapter = UserArchiveAdapter()
    keyboard = await user_archive_adapter.add_to_archive_get_number()
    await call.message.edit_text(text=user_archive_adapter._msg, reply_markup=keyboard)
    await SG.add_to_archive_mark.set()



async def get_mark(message: types.Message, state: FSMContext):
    data = await state.get_data()
    call = data.get("call")
    await state.update_data(mark=str(message.text))
    await message.delete()
    user_archive_adapter = UserArchiveAdapter()
    keyboard = await user_archive_adapter.add_to_archive_get_mark()
    await call.message.edit_text(text=f"ФИО: <b>{data.get('fio')}</b>\n"
                                      f"Номер: <b>{data.get('number')}</b>\n\n"
                                      f"Пометка: <b>{str(message.text)}</b>", reply_markup=keyboard)
    await SG.add_to_archive_final.set()



async def add_to_archive_final(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    generated_user_id = 000 + int(encrypto.Encrypto().get_id)
    fio = data.get("fio")
    number = data.get("number")
    mark_from_partner = data.get("mark")
    user_archive_adapter = UserArchiveAdapter()
    keyboard = await user_archive_adapter.back_to_archive_kb()
    await user_archive_adapter.add_user_to_archive(user_id=generated_user_id, user_fio=fio,
                                                   user_number=number, user_added_manually=True,
                                                   user_status=False, mark_from_partner=mark_from_partner)
    await state.finish()
    await call.message.edit_text(text="Клиент успешно добавлен в архив!", reply_markup=keyboard)














def register_add_to_archive_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        add_client_to_archive_btn,
        lambda callback_query: callback_query.data == 'add_client_to_archive_btn',
        state='*'
    )
    dp.register_callback_query_handler(
        add_to_archive_final,
        lambda callback_query: callback_query.data == 'add_to_archive_final',
        state=SG.add_to_archive_final
    )
    dp.register_message_handler(
        get_fio,
        state=SG.add_to_archive_fio
    )
    dp.register_message_handler(
        get_number,
        state=SG.add_to_archive_number
    )
    dp.register_message_handler(
        get_mark,
        state=SG.add_to_archive_mark
    )