from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from utils.callback_factories import AddAnimeCallbackFactory, AddDubCallbackFactory, DeleteCallbackFactory
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from utils.fsm import FSMFillForm
from db_connection import get_from_db, add_to_db
from keyboards.add_anime_kb import create_anime_kb, create_dub_kb
from keyboards.anime_list import edit_anime_kb
from services.services import get_anime_list
from constants.callback_data import CANCEL
from constants import requests
from lexicon.lexicon import LEXICON

router = Router()


@router.message(Command(commands='anime_list'))
async def process_list_of_anime(message: Message):
    request = requests.get_from_subscription(message.from_user.id)
    data = get_from_db(request)
    await message.answer(LEXICON['list_edit'], reply_markup=edit_anime_kb(data))


@router.callback_query(DeleteCallbackFactory.filter())
async def process_edit_anime_list(callback: CallbackQuery, callback_data: DeleteCallbackFactory):
    user_id = callback.from_user.id
    request = requests.delete_from_subscription(user_id, callback_data.dub_id, callback_data.anime_id)

    add_to_db(request)
    request = requests.get_from_subscription(user_id)
    data = get_from_db(request)

    await callback.message.edit_text(LEXICON['list_edit'], reply_markup=edit_anime_kb(data))


@router.callback_query(F.data == CANCEL)
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.delete()


@router.message(Command(commands='add_anime'), StateFilter(default_state))
async def process_help_command(message: Message, state: FSMContext):
    await message.answer(LEXICON['send_anime_title'])
    await state.set_state(FSMFillForm.fill_anime)


@router.message(StateFilter(FSMFillForm.fill_anime))
async def process_other_command(message: Message, state: FSMContext):
    anime_title = message.text.lower()
    query = requests.get_from_table('anime')
    anime_list = get_anime_list(query, anime_title)

    if anime_list:
        await state.update_data(user_id=message.from_user.id)
        await state.set_state(FSMFillForm.add_anime)
        await message.answer(LEXICON['choose_the_title'], reply_markup=create_anime_kb(anime_list))
    else:
        await message.answer(LEXICON['title_is_not_found'])


@router.callback_query(AddAnimeCallbackFactory.filter(), StateFilter(FSMFillForm.add_anime))
async def process_add_anime_command(callback: CallbackQuery, callback_data: AddAnimeCallbackFactory, state: FSMContext):
    await state.update_data(anime_id=callback_data.id)
    await state.set_state(FSMFillForm.fill_dubbing)
    await callback.message.edit_text(LEXICON['choose_the_dub'], reply_markup=create_dub_kb())


@router.callback_query(AddDubCallbackFactory.filter(), StateFilter(FSMFillForm.fill_dubbing))
async def process_add_dubbing(callback: CallbackQuery, callback_data: AddDubCallbackFactory, state: FSMContext):
    await state.update_data(dub_id=callback_data.id)
    data = await state.get_data()
    await state.clear()
    request = requests.add_to_subscription(data['user_id'], data['dub_id'], data['anime_id'])

    if not requests.get_copy_subscription(data['user_id'], data['dub_id'], data['anime_id']):
        add_to_db(request)
        await callback.message.edit_text(LEXICON['title_added'])
    else:
        await callback.message.edit_text('Вы уже добавляли такое аниме')
        await state.set_state(FSMFillForm.fill_anime)

