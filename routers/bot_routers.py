from aiogram.filters.command import Command
from aiogram import Router
from aiogram import F
from aiogram.filters.logic import and_f
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
)
from keyboards import bot_keyboards  # pyright:ignore
from states import AddNewSpending, GetSpendingByCategory  # pyright:ignore
from create_bot import sheet, currency_symbol  # pyright:ignore
from custom_filters import IsOwnerFilter

router = Router(name=__name__)
keyboards = bot_keyboards.Keyboards()


@router.message(and_f(IsOwnerFilter(F.text), F.text == "Get all spending by category"))
async def command_get_spending_by_category(message: Message, state: FSMContext):
    await message.answer("Write the name of category: ")
    await state.set_state(GetSpendingByCategory.category_name)


@router.message(GetSpendingByCategory.category_name)
async def get_spending_total_category(message: Message, state: FSMContext):
    await state.clear()
    category_name = message.text
    worksheet = sheet.sheet1
    all_spending = worksheet.get_all_values()
    for row in all_spending:
        if row[1] == category_name:
            await message.answer(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}")


@router.message(and_f(IsOwnerFilter(F.text), F.text == "Get all spending"))
async def get_all_spending(message: Message):
    worksheet = sheet.sheet1
    all_spending = worksheet.get_all_values()
    for row in all_spending:
        await message.answer(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}")


@router.message(
    and_f(IsOwnerFilter(F.text), F.text == "Get the sum total of all the spending")
)
async def command_get_sum_total_spending(message: Message):
    worksheet = sheet.sheet1
    spending_amounts = worksheet.col_values(1)
    spending_sum = 0
    for spending_amount in spending_amounts:
        spending_sum += int(spending_amount[0:-1])
    await message.answer(str(spending_sum) + currency_symbol)


@router.message(and_f(IsOwnerFilter(F.text), Command("start")))
async def command_start(message: Message):
    await message.answer(
        "Hello this is a bot to keep track of your finances.",
        reply_markup=await keyboards.user_kb(),
    )


@router.message(and_f(IsOwnerFilter(F.text), F.text == "Add new spending"))
async def add_new_spending(message: Message, state: FSMContext):
    await message.answer(
        "Write amount: ", reply_markup=await keyboards.cancel_state_kb()
    )
    await state.set_state(AddNewSpending.amount)


@router.message(AddNewSpending.amount)
async def get_spending_amount(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)
    await message.answer(
        "Write description: ", reply_markup=await keyboards.cancel_state_kb()
    )
    await state.set_state(AddNewSpending.description)


@router.message(AddNewSpending.description)
async def get_spending_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(
        "Write category: ", reply_markup=await keyboards.cancel_state_kb()
    )
    await state.set_state(AddNewSpending.category)


@router.message(AddNewSpending.category)
async def get_spending_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text.lower())
    await message.answer(
        "Write date(example - 2024/02/24): ",
        reply_markup=await keyboards.cancel_state_kb(),
    )
    await state.set_state(AddNewSpending.date)


@router.message(AddNewSpending.date)
async def get_spending_date(message: Message, state: FSMContext):
    data = await state.get_data()
    worksheet = sheet.sheet1
    error_text = "Failed with add new spending!"
    date = message.text
    amount = str(data["amount"]) + currency_symbol
    category = data["category"]
    description = data["description"]
    try:
        if worksheet.append_row([amount, category, description, date]):
            await message.answer("Your successfully add new spending!")
        else:
            await message.answer(error_text)
    except Exception as e:
        print(e)
    await state.clear()


@router.callback_query(F.data == "cancel_state")
async def cancel_state(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.answer("Canceled add new data!")  # pyright:ignore
