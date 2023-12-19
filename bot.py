from aiogram import Bot, Dispatcher
from environs import Env

env = Env()
BOT_TOKEN = env('BOT_TOKEN')

env = Env()
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot)

if __name__ == '__main__':
    dp.run_polling(bot)