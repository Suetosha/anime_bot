from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.callback_factories import AddAnimeCallbackFactory, AddDubCallbackFactory, AddAllDubCallbackFactory, Pagination
from database.db_connection import get_from_db
from constants.queries import get_from_dubbing, get_from_table
from constants.callback_data import CANCEL, BACKWARD, FORWARD
from lexicon.lexicon import LEXICON


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


class Pages:
    def __init__(self):
        self.anime_pages = get_from_db(get_from_table('anime'))
        self.total_pages = round(len(self.anime_pages) / 5)

    def get_page(self, page):
        return self.anime_pages[(page-1)*5:page*5]


def create_anime_list_kb(page=1):
    anime_pages = get_from_db(get_from_table('anime'))
    total_pages = round(len(anime_pages) / 5)
    anime_page = anime_pages[(page-1)*5:page*5]

    anime_buttons = [[InlineKeyboardButton(text=anime['title'],
                                           callback_data=AddAnimeCallbackFactory(id=anime['anime_id']).pack())] for anime in anime_page]

    pagination_buttons = [
        InlineKeyboardButton(text=LEXICON['backward'], callback_data=Pagination(action=BACKWARD,
                                                                                page=page,
                                                                                total_pages=total_pages).pack()),

        InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data='None'),

        InlineKeyboardButton(text=LEXICON['forward'], callback_data=Pagination(action=FORWARD,
                                                                               page=page,
                                                                               total_pages=total_pages).pack())
    ]

    cancel_btn = [[InlineKeyboardButton(text='Отменить', callback_data=CANCEL)]]

    keyboard = InlineKeyboardMarkup(inline_keyboard=anime_buttons + [pagination_buttons] + cancel_btn)

    return keyboard
