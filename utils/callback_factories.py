from aiogram.filters.callback_data import CallbackData
from constants.callback_data import ADD_ANIME, ADD_DUB, DELETE


class AddAnimeCallbackFactory(CallbackData, prefix=ADD_ANIME):
    id: int


class AddDubCallbackFactory(CallbackData, prefix=ADD_DUB):
    id: int


class DeleteCallbackFactory(CallbackData, prefix=DELETE):
    anime_id: int
    dub_id: int

