from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from google_auth import authenticate  # pyright:ignore

TOKEN = ""
finance_bot_spending_sheet_id = ""
OWNER_ID = 0
currency_symbol = "₴"
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
router = Router()
google_client = authenticate()
sheet = google_client.open_by_key(finance_bot_spending_sheet_id)
dp = Dispatcher()
