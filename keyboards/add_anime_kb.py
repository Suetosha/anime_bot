from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.callback_factories import AddAnimeCallbackFactory, AddDubCallbackFactory
from db_connection import get_from_db

def create_anime_kb(animes):
    anime_buttons = [[InlineKeyboardButton(text=f'{title}',
                                           callback_data=AddAnimeCallbackFactory(id=id).pack())] for id, title in animes]

    keyboard = InlineKeyboardMarkup(inline_keyboard=anime_buttons)
    return keyboard


def create_dub_kb():
    dub = get_from_db("""SELECT dubbing_id, studio FROM dubbing""")

    dub_buttons = [[InlineKeyboardButton(text=d['studio'], callback_data=AddDubCallbackFactory(id=d['dubbing_id']).pack())] for d in dub]
    keyboard = InlineKeyboardMarkup(inline_keyboard=dub_buttons)
    return keyboard
