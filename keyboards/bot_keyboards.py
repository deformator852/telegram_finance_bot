from aiogram.utils.keyboard import ReplyKeyboardBuilder

class Keyboards:
    @staticmethod
    async def user_kb():
        builder = ReplyKeyboardBuilder()
        builder.button(text="Add new category")
        builder.button(text="Show categories")
        builder.adjust(1)
        return builder.as_markup()
