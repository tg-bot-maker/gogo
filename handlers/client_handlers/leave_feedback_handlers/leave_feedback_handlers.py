from aiogram import types, Dispatcher


async def leave_feedback_btn(call: types.CallbackQuery):
    pass








def register_leave_feedback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        leave_feedback_btn,
        lambda callback_query: callback_query.data == 'leave_feedback_btn',
        state='*'
    )