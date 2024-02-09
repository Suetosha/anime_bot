import requests
from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from environs import Env
# from bot import bot, dp

env = Env()
env.read_env()

WEBHOOK_PATH = f'/{env("BOT_TOKEN")}/'
# WEBHOOK_URL = 'https://anime-bot-8yh3.onrender.com' + WEBHOOK_PATH
WEBHOOK_URL = 'https://a21e-87-116-163-213.ngrok-free.app' + WEBHOOK_PATH

app = FastAPI()
# bot = Bot(token=env('BOT_TOKEN'))
# dp = Dispatcher()


@app.on_event('startup')
async def on_startup():
    pass
    # tg_bot_webhook = await bot.get_webhook_info()
    #
    # if tg_bot_webhook != WEBHOOK_URL:
    #     await bot.set_webhook(url=WEBHOOK_URL)


# @dp.message(Command('get'))
# async def get(message):
#     res = requests.get('https://google.com')
#     await message.answer(str(res.status_code))
#
#
# @dp.message()
# async def wtf(message):
#     await message.answer('not found')


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    tg_update = types.Update(**update)
    # await dp.feed_update(bot=bot, update=tg_update)
    return 200


@app.get('/')
async def unhandled():
    return 'huinya'


@app.on_event('shutdown')
async def on_shutdown():
    # await bot.session.close()
    pass
