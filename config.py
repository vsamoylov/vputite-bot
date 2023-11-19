from os import getenv
import logging

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("TELEGRAM_TOKEN")      # Get your bot token using https://t.me/BotFather
CHAT_ID = getenv("CHAT_ID") 
CHANNEL_NAME = getenv("CHANNEL_NAME")

LOG_LEVEL=logging.INFO
if (getenv("LOG_LEVEL") is not None) and (type(getenv("LOG_LEVEL")) is str):
    LOG_LEVEL = int(getenv("LOG_LEVEL"))