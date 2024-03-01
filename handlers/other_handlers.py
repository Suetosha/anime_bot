from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from utils.callback_factories import AddAnimeCallbackFactory, AddDubCallbackFactory, DeleteCallbackFactory, \
    AddAllDubCallbackFactory, Pagination
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from utils.fsm import FSMFillForm
from database.db_connection import get_from_db, add_to_db
from keyboards.add_anime_kb import create_anime_kb, create_dub_kb, create_anime_list_kb
from keyboards.anime_list import edit_anime_kb
from services.services import get_anime_list, add_all_dubbing, add_dubbing
from constants.callback_data import CANCEL
from constants import queries
from lexicon.lexicon import LEXICON


router = Router()


@router.callback_query(DeleteCallbackFactory.filter())
async def process_edit_anime_list(callback: CallbackQuery, callback_data: DeleteCallbackFactory):
    user_id = callback.from_user.id
    request = queries.delete_from_subscription(user_id, callback_data.dub_id, callback_data.anime_id)
    add_to_db(request)
    request = queries.get_subscriptions_for_user(user_id)
    data = get_from_db(request)

    await callback.message.edit_text(LEXICON['list_edit'], reply_markup=edit_anime_kb(data))


@router.message(StateFilter(FSMFillForm.fill_anime))
async def process_fill_command(message: Message, state: FSMContext):
    anime_title = message.text.lower()
    query = queries.get_from_table('anime')
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
    user_id = callback.from_user.id

    await state.clear()
    request = queries.get_copy_subscription(user_id, data['dub_id'], data['anime_id'])

    if not get_from_db(request):
        add_dubbing(user_id, data['dub_id'], data['anime_id'])
        await callback.message.edit_text(LEXICON['title_added'])
    else:
        await callback.message.edit_text(LEXICON['title_exist'])


@router.callback_query(AddAllDubCallbackFactory.filter(), StateFilter(FSMFillForm.fill_dubbing))
async def process_add_all_dubbing(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    added_dub = add_all_dubbing(data['user_id'], data['anime_id'])

    if added_dub:
        await callback.message.edit_text(LEXICON['title_added'])
    else:
        await callback.message.edit_text(LEXICON['title_exist'])


@router.callback_query(Pagination.filter())
async def process_pagination_press(callback: CallbackQuery, callback_data: Pagination, state: FSMContext):
    page_num = int(callback_data.page)
    total_pages = callback_data.total_pages
    try:
        if callback_data.action == 'forward':
            page = page_num + 1 if page_num < total_pages else page_num
        else:

            page = page_num - 1 if page_num - 1 > 0 else 1

        await state.set_state(FSMFillForm.add_anime)
        await callback.message.edit_text(LEXICON['choose_the_title'], reply_markup=create_anime_list_kb(page=page))

    except Exception:
        pass


@router.callback_query(F.data == CANCEL)
async def process_cancel_press(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()


@router.message()
async def process_other_command(message: Message):
    await message.answer(LEXICON['help'])

