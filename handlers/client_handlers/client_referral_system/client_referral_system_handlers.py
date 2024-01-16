from aiogram import types, Dispatcher

from models.adapters.client_referral_system_adapter import ClientReferralSystemAdapter




async def client_referral_system_btn(call: types.CallbackQuery):
    client_panel_adapter = ClientReferralSystemAdapter()
    keyboard = await client_panel_adapter.client_referral_system_btn(call)
    await call.message.edit_text(text=client_panel_adapter._msg, reply_markup=keyboard)






def register_client_referral_system_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        client_referral_system_btn,
        lambda callback_query: callback_query.data.split("#")[0] == 'client_referral_system_btn',
        state='*'
    )