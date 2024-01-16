from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from cachetools import TTLCache  # https://cachetools.readthedocs.io/en/stable/
from aiogram import types

cache = TTLCache(maxsize=float('inf'), ttl=1)


class ThrottleMiddleware(BaseMiddleware):
    """Middleware for throttling callback queries"""
    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        if not cache.get(call.message.message_id):
            cache[call.message.message_id] = True
            return
        else:
            raise CancelHandler
