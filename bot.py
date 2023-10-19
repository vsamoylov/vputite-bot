import asyncio
import logging
import sys
from os import getenv
import random
from constants import *

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.utils.markdown import hbold

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("TELEGRAM_TOKEN")      # Get your bot token using https://t.me/BotFather
CHAT_ID = getenv("CHAT_ID") 
CHANNEL_NAME = getenv("CHANNEL_NAME") 

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
bot = None


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(TEXT_WELCOME + f", {hbold(message.from_user.full_name)}! " + TEXT_WELCOME_DESCRIPTION)

@dp.message(Command("stop"))
async def command_stop_handler(message: Message) -> None:
    await message.answer(f"Bye, {hbold(message.from_user.full_name)}!")

@dp.message(Command("random"))
async def command_random(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Нажми меня", callback_data="random_value"))
    await message.answer("Нажмите на кнопку, чтобы бот отправил число от 1 до 10",
        reply_markup=builder.as_markup())
    
    
@dp.callback_query(F.data == "random_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(random.randint(1, 10)))

# approved it the CHAT_ID
@dp.callback_query(F.data == "callback_approve")
async def forward_to_channel(callback: types.CallbackQuery):
    global bot
    # callback.message.delete_reply_markup(callback.inline_message_id)

    await callback.answer("userID: " + str(callback.message.from_user.id) + " caption: " + callback.message.caption + " chat_name: " + callback.message.chat.title + " from: " + callback.message.from_user.first_name + " msg ID: " + str(callback.message.message_id))
    await bot.edit_message_caption(chat_id=callback.message.chat.id, message_id=callback.message.message_id, caption = 'Edited caption')
    
#    user_ID = callback.message.from_user.id
#    await bot.send_message(chat_id=user_ID, text=TEXT_APPROVE_CONFIRMATION)

    emptyBuilder = InlineKeyboardBuilder()
    await callback.message.send_copy(chat_id=CHANNEL_NAME, reply_markup=emptyBuilder.as_markup())
    await bot.send_message(chat_id=CHAT_ID, text=TEXT_APPROVE_CONFIRMATION)
    await bot.send_message(chat_id=CHANNEL_NAME, text=HTML_INFO, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

# rejected in the CHAT_ID
@dp.callback_query(F.data == "callback_reject")
async def reject_suggestion(callback: types.CallbackQuery):
    await callback.message.answer(TEXT_REJECT_CONFIRMATION)

@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message

        builder = InlineKeyboardBuilder()
        builder.button(text=TEXT_APPROVE, callback_data="callback_approve")
        builder.button(text=TEXT_REJECT, callback_data="callback_reject")
        await message.send_copy(chat_id=CHAT_ID, reply_markup=builder.as_markup())

        # markup = types.InlineKeyboardMarkup()
        # btn0 = types.InlineKeyboardButton(text='Подтвердить', callback_data="1")
        # markup.add(btn0)

        
        #for index in range(1, 11):
        #    builder.button(text=f"Set {index}", callback_data=f"set:{index}")
        #builder.adjust(3, 2)
        #await message.answer(f"Твой ID: {message.from_user.id}", reply_markup=builder.as_markup())
        # await message.answer("Some text here", reply_markup=builder.as_markup())
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    global bot
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    ADMINS = await bot.get_chat_administrators(chat_id=CHAT_ID)
    admins_list = ""
    for x in ADMINS:
        if admins_list != "":
            admins_list += ", "
        admins_list += ("@" + x.user.username + " ")

    await bot.send_message(chat_id=CHAT_ID, text="I've started! :)\nAdministrators of the chat: " + admins_list)

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
