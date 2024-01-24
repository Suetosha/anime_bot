from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import constants.callback_data as callback_data_types
from utils.callback_factories import DeleteCallbackFactory


def edit_anime_kb(anime_list):
    print(anime_list)
    edit_anime_buttons = [[InlineKeyboardButton(text=f"{'❌'} {row['title']} - {row['studio']}",
                                                callback_data=DeleteCallbackFactory(anime_id=row['anime_id'],
                                                                                    dub_id=row['dubbing_id']).pack())]
                          for row in anime_list]

    cancel_btn = [InlineKeyboardButton(text='Отменить', callback_data=callback_data_types.CANCEL)]

    inline_edit_anime_kb = InlineKeyboardMarkup(inline_keyboard=edit_anime_buttons + [cancel_btn])

    return inline_edit_anime_kb
