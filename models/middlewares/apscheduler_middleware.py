from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types



class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler):
        super().__init__()
        self.scheduler = scheduler

    async def on_pre_process_message(self, message: types.Message, data: dict):
        # Передача объекта scheduler в обработчик сообщения
        data["scheduler"] = self.scheduler

    async def on_pre_process_callback_query(self, message: types.Message, data: dict):
        # Передача объекта scheduler в обработчик сообщения
        data["scheduler"] = self.scheduler

