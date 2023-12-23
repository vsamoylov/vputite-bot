import asyncio
import sys
from os import environ

from aiogram import types, F
from aiogram.filters import CommandStart, Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import FSInputFile
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hbold

from config import *
from constants import *
from create_bot import dp


class VptCallbackData(CallbackData, prefix="vpt"):
    action: str
    message_id: int
    chat_id: int

bot_name = ""
AUTHORS = ""

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
    help_photo = FSInputFile("help_photo.png")
    await bot.send_photo(message.chat.id, help_photo)


@dp.message(Command("stop"))
async def command_stop_handler(message: Message) -> None:
    await message.answer(f"Bye, {hbold(message.from_user.full_name)}!")

# approved in the CHAT_ID
@dp.callback_query(VptCallbackData.filter(F.action == "callback_approve"))
async def approve_suggestion(callback: types.CallbackQuery, callback_data: VptCallbackData):
    global bot

    #await callback.answer("user ID: " + str(callback.message.from_user.id) +"caption: " + callback.message.caption + " chat_name: " + callback.message.chat.title + " from: " + callback.message.from_user.first_name + " msg ID: " + str(callback.message.message_id))
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=None)

    await bot.copy_message(chat_id=CHANNEL_NAME, from_chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=None)
    await bot.send_message(chat_id=callback_data.chat_id, reply_to_message_id=callback_data.message_id, text=TEXT_ADMIN_APPROVE_CONFIRMATION )

    new_caption = "\n\n одобрено: "
    if callback.from_user.username is not None:
        new_caption = new_caption + callback.from_user.username 
    else:
        new_caption = new_caption + callback.from_user.first_name + " " + callback.from_user.last_name 
    await bot.edit_message_caption(chat_id=callback.message.chat.id, message_id=callback.message.message_id, caption = callback.message.caption + new_caption, parse_mode='html')

# rejected in the CHAT_ID
@dp.callback_query(VptCallbackData.filter(F.action == "callback_reject"))
async def reject_suggestion(callback: types.CallbackQuery, callback_data: VptCallbackData):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=None)
    await bot.send_message(chat_id=callback_data.chat_id, reply_to_message_id=callback_data.message_id, text=TEXT_ADMIN_REJECT_CONFIRMATION )

    new_caption = "\n\n отказано: "
    if callback.from_user.username is not None:
        new_caption = new_caption + callback.from_user.username 
    else:
        new_caption = new_caption + callback.from_user.first_name + " " + callback.from_user.last_name 
    await bot.edit_message_caption(chat_id=callback.message.chat.id, message_id=callback.message.message_id, caption = callback.message.caption + new_caption, parse_mode='html')

def is_reporter_user(user_id):
    logging.debug("is_reporter_user: " + str(user_id))
    logging.debug("AUTHORS: " + str(AUTHORS))
    return (str(user_id) in AUTHORS)

@dp.message()
async def echo_handler(message: types.Message) -> None:
    links = "<a href='https://t.me/" + CHANNEL_NAME.replace("@", "") + "'>" + TEXT_SUBSCRIBE + "</a>\n" + "<a href='https://t.me/" + bot_name + "'>" + TEXT_SENDINFO + "</a>"	
    try:
        global builder
#        logging.debug(message.entities[0].type)

        if (message.media_group_id == None):
            # Send a copy of the received message
            builder = InlineKeyboardBuilder()
       
            logging.debug("Message from echo_handler() function:")
            logging.debug(message)
            builder.button(text=TEXT_APPROVE, callback_data=VptCallbackData(action="callback_approve", message_id=message.message_id, chat_id=message.chat.id).pack())
            builder.button(text=TEXT_REJECT, callback_data=VptCallbackData(action="callback_reject", message_id=message.message_id, chat_id=message.chat.id).pack())

            if (message.photo):
                if (message.caption):
                    username = message.from_user.username or ""
                    first_name = message.from_user.first_name or ""
                    last_name = message.from_user.last_name or ""
                    from_user_counter = "прислано от: " + "<a href='tg://user?id=" + str(message.from_user.id) + "'>" + "userID: " + str(message.from_user.id) + ", username: " + username + ", name: " + first_name + " " + last_name + "</a>" 
                    logging.debug("from_user_counter:" + from_user_counter)
                    await bot.send_message(chat_id=CHAT_ID, text = from_user_counter)
                    logging.debug("message sent")

                    copy = await message.send_copy(chat_id=CHAT_ID, reply_markup=builder.as_markup())
                    logging.debug("copy message sent")

                    new_caption = ""
                    if (copy.caption):
                        new_caption = copy.caption
                 
                    logging.debug("check the author (id): " + str(message.from_user.id))                 
                    if (is_reporter_user(message.from_user.id)):
                        logging.debug("reporter user (username): " + message.from_user.username)
                        new_caption = new_caption + '\n\n прислано: ' + '<a href="tg://user?id=' + str(message.from_user.id) + '">' + message.from_user.username + '</a>'

                    await bot.edit_message_caption(chat_id=copy.chat.id, message_id=copy.message_id, caption = new_caption + "\n\n" + links, reply_markup=builder.as_markup())
                    return
                else: 
                    await message.answer(TEXT_SUBMIT_RULES_PHOTO)   
                    return
            if (message.video):
                if (message.caption):
                    username = message.from_user.username or ""
                    first_name = message.from_user.first_name or ""
                    last_name = message.from_user.last_name or ""
                    from_user_counter = "прислано от: " + "<a href='tg://user?id=" + str(message.from_user.id) + "'>" + "userID: " + str(message.from_user.id) + ", username: " + username + ", name: " + first_name + " " + last_name + "</a>" + ", дата: " + message.date.strftime('%d-%m-%Y')
                    await bot.send_message(chat_id=CHAT_ID, text = from_user_counter)

                    file_id = message.video.file_id
                    copy = await bot.send_video(chat_id=CHAT_ID, video=file_id, caption=message.caption, reply_markup=builder.as_markup())
                    new_caption = ""
                    if (copy.caption):
                        new_caption = copy.caption

                    if (is_reporter_user(message.from_user.id)):
                        new_caption = new_caption + '\n\n прислано: ' + '<a href="tg://user?id=' + str(message.from_user.id) + '">' + message.from_user.username + '</a>'
                    await bot.edit_message_caption(chat_id=copy.chat.id, message_id=copy.message_id, caption = new_caption + "\n\n" + links, reply_markup=builder.as_markup())
                    return
                else:    
                    await message.answer(TEXT_SUBMIT_RULES_VIDEO)   
                    return
            await message.answer(TEXT_SUBMIT_RULES)
        else:
            await message.answer(TEXT_SUBMIT_RULES_GROUP)
            
    except TypeError as e:
        # But not all the types is supported to be copied so need to handle it
        logging.ERROR("Failed to send message: %s ", e)
        await message.answer(TEXT_SUBMIT_ERROR)

async def set_default_commands(dp):
    await bot.set_my_commands([
        types.BotCommand(command="/start", description="Запустить бота"),
        types.BotCommand(command="/help", description="Помощь"),
    ])

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    # And the run events dispatching
    #await bot.set_my_description(TEXT_BOT_DESCRIPTION)
    await set_default_commands(bot)
    
    global bot_name	
    bot_info = await bot.get_me()
    bot_name = bot_info.username
    logging.debug(bot_name)
    
    ADMINS = await bot.get_chat_administrators(chat_id=CHAT_ID)
    admins_list = ""
    for x in ADMINS:
        if admins_list != "":
            admins_list += ", "
        admins_list += ("@" + x.user.username + " ")

    GREETING_MESSAGE = "I've started! :)\nAdministrators of the chat: " + admins_list

    global AUTHORS
    if "AUTHORS" in environ:
        AUTHORS=getenv("AUTHORS").split(",")
        GREETING_MESSAGE += "\nList of Authors:" 
        for author in AUTHORS:
            GREETING_MESSAGE += " " + author

    await bot.send_message(chat_id=CHAT_ID, text=GREETING_MESSAGE)
    await dp.start_polling(bot)


if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    #logging.basicConfig(level=logging.ERROR, stream=sys.stdout)
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(main())
