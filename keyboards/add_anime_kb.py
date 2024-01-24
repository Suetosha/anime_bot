from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.callback_factories import AddAnimeCallbackFactory, AddDubCallbackFactory


def create_anime_kb(animes):
    anime_buttons = [[InlineKeyboardButton(text=f'{title}',
                                           callback_data=AddAnimeCallbackFactory(id=id).pack())] for id, title in animes]

    keyboard = InlineKeyboardMarkup(inline_keyboard=anime_buttons)
    return keyboard


def create_dub_kb():
    dub = {'Студийная банда': '11', 'AniLibria': '12', 'AnimeVost': '13', 'AniDUB': '14', 'Dream Cast': '15'}
    dub_buttons = [[InlineKeyboardButton(text=title,
                                         callback_data=AddDubCallbackFactory(id=id).pack())] for title, id in dub.items()]
    keyboard = InlineKeyboardMarkup(inline_keyboard=dub_buttons)
    return keyboard
