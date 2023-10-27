import asyncio
import logging
import sys
from constants import *
from config import *
from create_bot import dp, bot

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, BotCommand
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.utils.markdown import hbold

import os
from aiogram.types import InputFile
from aiogram.types import FSInputFile


class VptCallbackData(CallbackData, prefix="vpt"):
    action: str
    message_id: int
    chat_id: int


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

@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    """
    This handler receives messages with `/help` command
    """
    await message.answer(TEXT_HELP)

    # Path to the local photo file
    photo_moto = FSInputFile("help_photo.png")
    await bot.send_photo(message.chat.id, photo_moto)



@dp.message(Command("stop"))
async def command_stop_handler(message: Message) -> None:
    await message.answer(f"Bye, {hbold(message.from_user.full_name)}!")


# approved in the CHAT_ID
@dp.callback_query(VptCallbackData.filter(F.action == "callback_approve"))
async def approve_suggestion(callback: types.CallbackQuery, callback_data: VptCallbackData):
    global bot
    logging.debug(callback)

    await callback.answer("user ID: " + str(callback.message.from_user.id) +"caption: " + callback.message.caption + " chat_name: " + callback.message.chat.title + " from: " + callback.message.from_user.first_name + " msg ID: " + str(callback.message.message_id))
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=None)

    await bot.copy_message(chat_id=CHANNEL_NAME, from_chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=None)
    await bot.send_message(chat_id=callback_data.chat_id, reply_to_message_id=callback_data.message_id, text=TEXT_ADMIN_APPROVE_CONFIRMATION )



# rejected in the CHAT_ID
@dp.callback_query(VptCallbackData.filter(F.action == "callback_reject"))
async def reject_suggestion(callback: types.CallbackQuery, callback_data: VptCallbackData):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=None)
    await bot.send_message(chat_id=callback_data.chat_id, reply_to_message_id=callback_data.message_id, text=TEXT_ADMIN_REJECT_CONFIRMATION )


@dp.message()
async def echo_handler(message: types.Message) -> None:
    try:
        global builder
        logging.debug(message)
        logging.debug(message.caption)
        logging.debug(message.photo)
        logging.debug(message.media_group_id)
        if (message.media_group_id == None):
            # Send a copy of the received message
            builder = InlineKeyboardBuilder()
       
            logging.debug("Message from echo_handler() function:")
            logging.debug(message)
            builder.button(text=TEXT_APPROVE, callback_data=VptCallbackData(action="callback_approve", message_id=message.message_id, chat_id=message.chat.id).pack())
            builder.button(text=TEXT_REJECT, callback_data=VptCallbackData(action="callback_reject", message_id=message.message_id, chat_id=message.chat.id).pack())

            if (message.caption and message.photo):
                copy = await message.send_copy(chat_id=CHAT_ID, reply_markup=builder.as_markup())
                new_caption = ""
                if (copy.caption):
                    new_caption = copy.caption
                await bot.edit_message_caption(chat_id=copy.chat.id, message_id=copy.message_id, caption = new_caption + "\n\n" + HTML_INFO, reply_markup=builder.as_markup())
                return
            if (message.caption and message.video):
                file_id = message.video.file_id
                #media = InputMediaVideo(media=file_id)
                copy = await bot.send_video(chat_id=CHAT_ID, video=file_id, caption=message.caption, reply_markup=builder.as_markup())
                new_caption = ""
                if (copy.caption):
                    new_caption = copy.caption
                await bot.edit_message_caption(chat_id=copy.chat.id, message_id=copy.message_id, caption = new_caption + "\n\n" + HTML_INFO, reply_markup=builder.as_markup())
                return
            await message.answer(TEXT_SUBMIT_RULES)
        else: 
            await message.answer(TEXT_SUBMIT_RULES)

    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer(TEXT_SUBMIT_ERROR)

async def set_default_commands(dp):
    await bot.set_my_commands([
        types.BotCommand(command="/start", description="Запустить бота"),
        types.BotCommand(command="/help", description="Помощь"),
    ])

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    # And the run events dispatching
    await set_default_commands(bot)
    
    info = await bot.get_me()
    name = info.username
    print(name)

    ADMINS = await bot.get_chat_administrators(chat_id=CHAT_ID)
    admins_list = ""
    for x in ADMINS:
        if admins_list != "":
            admins_list += ", "
        admins_list += ("@" + x.user.username + " ")

    await bot.send_message(chat_id=CHAT_ID, text="I've started! :)\nAdministrators of the chat: " + admins_list)

    await dp.start_polling(bot)


if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(main())