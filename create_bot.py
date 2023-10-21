from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config import *

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

