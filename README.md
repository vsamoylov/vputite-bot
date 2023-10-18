# vputite-bot
Suggestion's bot for #vputite telegram channel

# Vputite Suggestions Telegram Bot - Telegram 🇬🇧

Bot was created originally for IASA Student Council to handle suggestions, questions and requests. However, you can 
freely fork this repository and create your own bot.

## How bot works

1. User sends a message to the bot
2. Bot forwards the message to the chat, configured by administrator 
3. One of the chat participants with the administrator permissions approve or reject the forwarded message
4. Bot send it to the channel

## Features

- __Text, Photos, Videos, Documents, GIFs, Voice Messages__ and __Geolocation__ are supported
- Customisable messages for bot to answer
- Bot is stateless, no database is required for operation 
- Docker files for docker-compose for easy testing/development/deployment 

> ❗ __Note: changing pictures/videos is not possible, only their captions__


## Config

To setup a bot for your own usage, you should specify those variables in 
[`.env`](https://github.com/ehorohorin/vputite-bot/blob/main/.env).

``` bash
# Bot Data
TOKEN = # your bot's token
CHAT_ID = # chat id where the bot will forward users' messages
CHANNEL_NAME = # name of the channel to publish suggested post


To change default text to your custom, redefine values of the dictionary for each phrase in 
[`config.py`](https://github.com/dimaplel/telegram-suggestions-bot/blob/main/config.py).

``` bash
# Predefined text to send
TEXT_MESSAGES = {
    'start': 'Welcome to Suggestions Bot 👋 \n\n Please, send your message and we will process your request.',
    'message_template': '<i>Message from: <b>@{0}</b>.</i>\n\n{1}<b>id: {2}</b>',
    'is_banned': '❌ User is banned!', 'has_banned': '✅ User has been successfully banned!',
    'already_banned': '❌ User is already banned!', 'has_unbanned': '✅ User has been successfully un-banned!',
    'not_banned': '❌ There is no such user in the ban list!',
    'user_banned': '🚫 You cannot send messages to this bot!',
    'user_unbanned': '🥳 You have proven your innocence, and now you can write to this bot again!',
    'user_reason_banned': '🚫 You cannot send messages to this bot due to the reason: <i>{}</i>.',
    'pending': 'Thank you for your request! We are already into processing it.',
    'unsupported_format': '❌ Format of your message is not supported and it will not be forwarded.',
    'message_not_found': '❌ It looks like your message was sent more that a day ago. Message to edit was not found!',
    'message_was_not_edited': '❌ Unfortunately you cannot edit images/videos themselves.'
                              'Please, send a new message.',
    'reply_error': '❌ Please, reply with /ban or /unban only on forwarded from user messages!'
}
```

## Installation guide

1. Clone this repository using terminal or tools in your IDE: 
`git clone https://github.com/dimaplel/telegram-suggestions-bot.git`
2. Change directory in terminal `cd $repository-direcory`
3. Download requirements `pip install -r requirements.txt`
4. Edit and update [`config.py`](https://github.com/dimaplel/telegram-suggestions-bot/blob/main/config.py)
5. Create a new routine operator in your SQL database and insert script from 
[`sql_script.txt`](https://github.com/dimaplel/telegram-suggestions-bot/blob/main/sql_script.txt) so that database 
could delete rows by itself after some time. By the way, don't forget to configure SQL user instead of `<user>` tag
6. Run the bot `python bot.py` or by deploying it to [__Heroku__](https://heroku.com/deploy)

## Authors

* [Eugene Horohorin]()

