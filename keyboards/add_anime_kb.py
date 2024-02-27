from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.callback_factories import AddAnimeCallbackFactory, AddDubCallbackFactory, AddAllDubCallbackFactory
from database.db_connection import get_from_db
from constants.queries import get_from_dubbing


def create_anime_kb(animes):
    anime_buttons = [[InlineKeyboardButton(text=f'{title}',
                                           callback_data=AddAnimeCallbackFactory(id=id).pack())] for id, title in animes]

    keyboard = InlineKeyboardMarkup(inline_keyboard=anime_buttons)
    return keyboard


def create_dub_kb():
    dub = get_from_db(get_from_dubbing())
    dub_buttons = [[InlineKeyboardButton(text=d['studio'], callback_data=AddDubCallbackFactory(id=d['dubbing_id']).pack())] for d in dub]
    all_dub_buttons = [[InlineKeyboardButton(text='Все озвучки', callback_data=AddAllDubCallbackFactory().pack())]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=dub_buttons + all_dub_buttons)
    return keyboard
