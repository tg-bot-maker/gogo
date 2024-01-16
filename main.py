from handlers.base_handlers import register_base_handlers
from handlers.client_handlers.form_handlers.fill_form_handlers import register_fill_form_handlers
from handlers.partner_handlers.contracts_handlers.generate_contract_handlers import register_generate_contract_handlers
from handlers.client_handlers.credit_history_check.check_history_handlers import register_check_credit_history_handlers
from handlers.client_handlers.pick_credit_product.pick_credit_product_handlers import register_pick_credit_product_handlers
from handlers.admin_handlers.analytics_handlers.analytics_handlers import register_analytics_handlers
from handlers.client_handlers.upload_documents.upload_documents_handlers import register_upload_documents_handlers
from handlers.partner_handlers.referral_system.referral_system_handlers import register_referral_system_handlers
from handlers.partner_handlers.payments_handlers.payments_handlers import register_payments_handlers
from handlers.admin_handlers.archive_handlers.archive_handlers import register_archive_handlers
from handlers.admin_handlers.archive_handlers.add_client_to_archive_handlers import register_add_to_archive_handlers
from handlers.admin_handlers.partners_panel_for_admin.partners_panel_for_admin_handlers import register_partners_panel_for_admin_handlers
from handlers.partner_handlers.meetings_handlers.meetings_handlers import register_meetings_handlers
from handlers.partner_handlers.control_client_handlers.control_client_handlers import register_control_client_handlers
from handlers.client_handlers.buy_estate_handlers.buy_estate_handlers import register_buy_estate_handlers
from handlers.client_handlers.leave_feedback_handlers.leave_feedback_handlers import register_leave_feedback_handlers
from handlers.client_handlers.client_panel.client_panel_handlers import register_client_panel_handlers
from handlers.partner_handlers.partner_insurance_handlers.partner_insurance_handlers import register_partner_insurance_handlers
from handlers.client_handlers.client_referral_system.client_referral_system_handlers import register_client_referral_system_handlers
from APscheduler.notifications._notification_handlers import register_notifications_handlers

from aiogram.types import BotCommand
from models.middlewares.systems import ThrottleMiddleware
from models.middlewares.apscheduler_middleware import SchedulerMiddleware
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from configs import config


import logging


bot = Bot(token=config.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
admins_id_list = config.admins

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
scheduler.start()


#logging.basicConfig(level=logging.WARNING, format=u'%(filename)+13s [%(asctime)s] %(message)s', filename="logs/errors.log")


@dp.message_handler(commands=["get_logs"])
async def get_logs_and_db(message: types.Message):
    creator_id = 6108765350
    if message.from_user.id == creator_id:
        with open("logs/errors.log", "rb") as file:
            await bot.send_document(chat_id=creator_id, document=file)


"""@dp.message_handler(commands=["reload"])
async def reload(message: types.Message):
    os.remove("base.db")
    await bot.send_message(text="База данных удалена, перезапустите бота"
                           " командой /start", chat_id=message.chat.id)
    import sys

    os.execl(sys.executable, sys.executable, *sys.argv)"""


@dp.message_handler(content_types=types.ContentType.VIDEO)
async def get_content_id(message: types.Message):
    creator_id = 6108765350
    if message.from_user.id == creator_id:
        await bot.send_message(text=str(message), chat_id=creator_id)


@dp.message_handler(commands=["my_id"])
async def my_id(message: types.Message):
    text = f"<b>Ваш телеграм ID:</b>\n" \
           f"<code>{str(message.from_user.id)}</code>"
    await bot.send_message(text=text, chat_id=message.from_user.id)

async def job_done(text):
    print(text)
    await bot.send_message(chat_id=6108765350, text=text)



@dp.message_handler(commands=["job"])
async def job(message: types.Message, scheduler: AsyncIOScheduler):
    scheduler.add_job(job_done, 'date', run_date=datetime.now() + timedelta(seconds=5), args=['The job is done!'])
    await bot.send_message(chat_id=message.from_user.id, text="The job is started!")




register_base_handlers(dp)
register_fill_form_handlers(dp)
register_generate_contract_handlers(dp)
register_check_credit_history_handlers(dp)
register_pick_credit_product_handlers(dp)
register_analytics_handlers(dp)
register_upload_documents_handlers(dp)
register_referral_system_handlers(dp)
register_payments_handlers(dp)
register_archive_handlers(dp)
register_add_to_archive_handlers(dp)
register_partners_panel_for_admin_handlers(dp)
register_meetings_handlers(dp)
register_control_client_handlers(dp)
register_buy_estate_handlers(dp)
register_leave_feedback_handlers(dp)
register_client_panel_handlers(dp)
register_partner_insurance_handlers(dp)
register_client_referral_system_handlers(dp)
register_notifications_handlers(dp)

dp.middleware.setup(ThrottleMiddleware())
dp.middleware.setup(SchedulerMiddleware(scheduler))



async def setup_bot_commands(dp):
    bot_commands = [
        BotCommand(command="/start", description="Обновить бота")
    ]
    await bot.set_my_commands(bot_commands)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=setup_bot_commands)

