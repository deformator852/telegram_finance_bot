from aiogram.fsm.state import State, StatesGroup


class AddNewSpending(StatesGroup):
    amount = State()
    description = State()
    category = State()
    date = State()


class GetSpendingByCategory(StatesGroup):
    category_name = State()
