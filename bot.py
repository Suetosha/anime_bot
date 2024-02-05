import asyncio
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from keyboards.main_keyboard import set_main_menu
from handlers import commands_handlers, main_handlers
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from parser import send_updates, get_new_anime, clean_up_table
from datetime import datetime, date


async def main() -> None:
    config: Config = load_config()

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    # планировщик по отправке апдейтов
    scheduler.add_job(send_updates, trigger='cron', hour=12, minute=00, kwargs={'bot': bot})
    scheduler.add_job(send_updates, trigger='cron', hour=18, minute=00, kwargs={'bot': bot})
    scheduler.add_job(send_updates, trigger='cron', hour=23, minute=59, kwargs={'bot': bot})
    # планировщик по очищению таблицы рассылок
    scheduler.add_job(clean_up_table, trigger='cron', hour=0, minute=0)
    # планировщик по добавлениям аниме по сезонам
    scheduler.add_job(get_new_anime, trigger='date', run_date=date(datetime.now().year, 1, 1), args=[1])
    scheduler.add_job(get_new_anime, trigger='date', run_date=date(datetime.now().year, 4, 1), args=[4])
    scheduler.add_job(get_new_anime, trigger='date', run_date=date(datetime.now().year, 7, 1), args=[7])
    scheduler.add_job(get_new_anime, trigger='date', run_date=date(datetime.now().year, 10, 1), args=[10])
    scheduler.start()

    await set_main_menu(bot)

    dp.include_router(main_handlers.router)
    dp.include_router(commands_handlers.router)

    dp.startup.register(set_main_menu)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


