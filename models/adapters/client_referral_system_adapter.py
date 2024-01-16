from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Optional
from database.db import session_factory
from models.controls.client_referral_system_controls import ClientReferralSystemControl

class ClientReferralSystemAdapter:
    def __init__(self, user_id: Optional[int] = None):
        self._user_id = user_id
        self._inline_keyboard = InlineKeyboardMarkup()
        self._msg = ''

    @property
    def inline_keyboard(self) -> InlineKeyboardMarkup:
        return self._inline_keyboard

    @property
    def message_text(self) -> str:
        return self._msg


    async def add_referral(self, client_user_id, client_referrer_id):
        with session_factory() as session:
            client_referral_system_control = ClientReferralSystemControl(session)
            await client_referral_system_control.add(client_user_id, client_referrer_id)
            session.commit()


    async def client_referral_system_btn(self, call):
        with session_factory() as session:
            client_referral_system_control = ClientReferralSystemControl(session)
            referrals = await client_referral_system_control.get_all_referrals(call.from_user.id)
            session.commit()

        ref_link = f"https://t.me/{call.message.from_user.username}?start={call.from_user.id}crs"
        self._msg = "<b>Ваша реферальная ссылка:</b>\n" \
                    f"<code>{ref_link}</code>\n\n" \
                    f"Количество рефералов: <b>{len(referrals)}</b>\n" \

        keyboard = InlineKeyboardMarkup() \
            .add(InlineKeyboardButton('Поделиться ссылкой', url=f"https://t.me/share/url?url={ref_link}")) \
            .add(InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_client_panel_btn'))

        return keyboard

# .add(InlineKeyboardButton('Мои рефералы', callback_data=f'client_referrals_btn#{call.from_user.id}')) \



