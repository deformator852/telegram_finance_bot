from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


class Keyboards:
    @staticmethod
    async def user_kb():
        builder = ReplyKeyboardBuilder()
        builder.button(text="Add new spending")
        builder.button(text="Get the sum total of all the spending")
        builder.button(text="Get all spending")
        builder.button(text="Get all spending by category")
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    async def cancel_state_kb():
        builder = InlineKeyboardBuilder()
        builder.button(text="cancel", callback_data="cancel_state")
        return builder.as_markup()
