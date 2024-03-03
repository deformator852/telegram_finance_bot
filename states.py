from aiogram.fsm.state import State, StatesGroup


class AddNewSpending(StatesGroup):
    amount = State()
    description = State()
    category = State()


class AddNewCategory(StatesGroup):
    category_name = State()
