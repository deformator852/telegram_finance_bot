from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from google_auth import authenticate #pyright:ignore

TOKEN = "6197552285:AAGoPCi4lETR1y3JITUZc_M3sojsEpD-D6c"
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
router = Router()
google_client = authenticate()
dp = Dispatcher()
