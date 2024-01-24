import asyncio
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from keyboards.main_keyboard import set_main_menu
from handlers import commands_handlers, other_handlers, main_handlers
from aiogram.fsm.storage.memory import MemoryStorage


async def main() -> None:
    config: Config = load_config()

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    await set_main_menu(bot)

    dp.include_router(main_handlers.router)
    dp.include_router(commands_handlers.router)
    dp.include_router(other_handlers.router)
    dp.startup.register(set_main_menu)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
