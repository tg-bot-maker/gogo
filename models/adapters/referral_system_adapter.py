from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Optional



class ReferralSystemAdapter:
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


    async def referral_system_kb(self, call) -> InlineKeyboardMarkup:
        ref_link = f"https://t.me/{call.message.from_user.username}?start={call.from_user.id}"
        return InlineKeyboardMarkup() \
            .add(InlineKeyboardButton('Поделиться ссылкой', url=f"https://t.me/share/url?url={ref_link}")) \
            .add(InlineKeyboardButton('Мои клиенты', callback_data='ref_my_clients')) \
            .add(InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_partner_menu_btn'))

"""    async def ref_my_clients(self, referrer_id):
        with session_factory() as session:
            user_control = UserControl(session)
            referrer_clients = await user_control.get_clients_of_referrer(referrer_id)
            session.commit()
        clients = ""
        for i in referrer_clients:
            if i.user_fio != "Аноним":
                clients = clients + f"<b>{i.user_fio} - @{i.user_name}</b> \nЭтап: <b>{i.user_stage}</b>\n\n"
            else:
                clients = clients + f"<b>@{i.user_name}</b> | Этап: <b>{i.user_stage}</b>\n\n"
        if clients == "":
            clients = "<b>У вас пока нет клиентов 🤷‍♂</b>"
        self._msg = clients
        return InlineKeyboardMarkup().add(InlineKeyboardButton('◀️   Назад    ', callback_data='back_to_referral_system_btn'))
    """