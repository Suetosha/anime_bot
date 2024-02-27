from aiogram.filters.callback_data import CallbackData
from constants.callback_data import ADD_ANIME, ADD_DUB, DELETE, ADD_ALL_DUB


class AddAnimeCallbackFactory(CallbackData, prefix=ADD_ANIME):
    id: int


class AddDubCallbackFactory(CallbackData, prefix=ADD_DUB):
    id: int


class AddAllDubCallbackFactory(CallbackData, prefix=ADD_ALL_DUB):
    pass


class DeleteCallbackFactory(CallbackData, prefix=DELETE):
    anime_id: int
    dub_id: int

