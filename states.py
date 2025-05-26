from aiogram.fsm.state import State, StatesGroup

class RegisterState(StatesGroup):
    phone = State()

class AddCategoryState(StatesGroup):
    name = State()

class AddProductState(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()
    category = State()

class GetProductState(StatesGroup):
    category = State()
    product = State()

class CreateOrderState(StatesGroup):
    address = State()
    phone = State()


class AddAdvertState(StatesGroup):
    image = State()
    content = State()