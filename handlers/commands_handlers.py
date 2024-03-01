from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from utils.fsm import FSMFillForm
from database.db_connection import get_from_db, add_to_db
from keyboards.add_anime_kb import create_anime_list_kb
from keyboards.anime_list import edit_anime_kb
from constants import queries
from lexicon.lexicon import LEXICON
from services.mailing import send_updates_now


router = Router()


@router.message(Command(commands='added_anime_list'))
async def process_list_of_anime(message: Message, state: FSMContext):
    await state.clear()
    request = queries.get_subscriptions_for_user(message.from_user.id)
    data = get_from_db(request)
    await message.answer(LEXICON['list_edit'], reply_markup=edit_anime_kb(data))


@router.message(Command(commands='add_anime'), StateFilter(default_state))
async def process_help_command(message: Message, state: FSMContext):
    await message.answer(LEXICON['send_anime_title'])
    await state.set_state(FSMFillForm.fill_anime)


@router.message(Command(commands='get_anime_list'), StateFilter(default_state))
async def process_get_anime_list(message: Message, state: FSMContext):
    await state.set_state(FSMFillForm.add_anime)
    await message.answer(LEXICON['choose_the_title'], reply_markup=create_anime_list_kb())


@router.message(Command(commands='get_updates'), StateFilter(default_state))
async def process_help_command(message: Message):
    user_id = message.from_user.id
    updates = send_updates_now(user_id)

    if updates:
        await message.answer(updates, parse_mode='HTML')
    else:
        await message.answer(LEXICON['update_is_empty'])


@router.message(Command(commands='mailing'))
async def process_list_of_anime(message: Message):
    user_id = message.from_user.id
    status = get_from_db(queries.get_mailing_status(user_id))[0]['sending_messages']
    if status:
        add_to_db(queries.change_mailing_status(user_id, False))
        await message.answer(LEXICON['turn_off_mailing'])
    else:
        add_to_db(queries.change_mailing_status(user_id, True))
        await message.answer(LEXICON['turn_on_mailing'])



