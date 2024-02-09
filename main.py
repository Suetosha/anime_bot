from fastapi import FastAPI
from bot import bot, dp, config
from aiogram import types


WEBHOOK_PATH = f'/{config.tg_bot.token}/'
WEBHOOK_URL = 'https://anime-bot-8yh3.onrender.com' + WEBHOOK_PATH

app = FastAPI()


@app.on_event('startup')
async def on_startup():
    tg_bot_webhook = await bot.get_webhook_info()

    if tg_bot_webhook != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    tg_update = types.Update(**update)
    await dp._process_update(bot=bot, update=tg_update)
    return 200


@app.on_event('shutdown')
async def on_shutdown():
    pass
