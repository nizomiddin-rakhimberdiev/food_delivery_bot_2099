from aiogram.fsm.state import State, StatesGroup

class RegisterState(StatesGroup):
    phone = State()

class AddCategoryState(StatesGroup):
    name = State()