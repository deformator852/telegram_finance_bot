from aiogram.filters.command import Command
from aiogram import Router
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
)
import gspread
from keyboards import bot_keyboards  # pyright:ignore
from states import AddNewCategory  # pyright:ignore
from create_bot import google_client  # pyright:ignore

router = Router(name=__name__)
keyboards = bot_keyboards.Keyboards()
finance_bot_categories_sheet_id = "1CZ6ugu_sJzgtdxxxEuownGDTO99PoSSH0slCVZzRfqU"


@router.message(Command("start"))
async def command_start(message: Message):
    await message.answer(
        "Hello this is a bot to keep track of your finances.",
        reply_markup=await keyboards.user_kb(),
    )


@router.message(F.text == "Show categories")
async def command_show_categories(message:Message):
    sheet = google_client.open_by_key(finance_bot_categories_sheet_id)
    worksheet = sheet.sheet1
    worksheet_colums_len = worksheet.get_all_values()
    categories = ""
    for category in worksheet_colums_len[0]:
        categories += category + ", "
    await message.answer(categories[0:-2])
    


@router.message(F.text == "Add new category")
async def command_add_new_categories(message: Message, state: FSMContext):
    await state.set_state(AddNewCategory.category_name)
    await message.answer("Write the category name: ")


@router.message(AddNewCategory.category_name)
async def get_new_category_name(message: Message, state: FSMContext):
    name = message.text
    sheet = google_client.open_by_key(finance_bot_categories_sheet_id)
    worksheet = sheet.sheet1
    worksheet_colums_len = len(worksheet.get_all_values()[0])
    start_cell = gspread.utils.rowcol_to_a1(1, worksheet_colums_len + 1)
    try:
        if worksheet.update(start_cell, [[name.lower()]]):
            await message.answer("Your successfully add new category!")
        else:
            await message.answer("Something came from!You didn't add new category!")
    except:
        await message.answer("Something came from!You didn't add new category!")
    await state.clear()


@router.message(F.text == "add new spending")
async def command_add_new_spending(message: Message):
    pass


@router.message(F.text == "features")
async def command_features(message: Message):
    pass


# @router.message(F.text == "categories list")
# async def command_categories_list(message: Message):
#     category_answer = ""
#     for category in categories:
#         category_answer += f"{category["category_name"]}, "
#     await message.answer(f"Categories: {category_answer[0:-2]}")
