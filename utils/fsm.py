from aiogram.fsm.state import State, StatesGroup


class FSMFillForm(StatesGroup):
    fill_anime = State()
    add_anime = State()
    fill_dubbing = State()
