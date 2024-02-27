from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter
from database.db_connection import get_from_db, add_to_db
from lexicon.lexicon import LEXICON
from aiogram.fsm.state import default_state
from constants import queries
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    data = get_from_db(queries.get_from_users(user_id))

    if not data:
        add_to_db(queries.add_user(user_id))

    await message.answer(LEXICON['start'])


@router.message(Command(commands='help'))
async def process_help_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(LEXICON['help'])

