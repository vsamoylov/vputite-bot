from config import *
import random
from create_bot import bot

TEXT_APPROVE = "Подтвердить"
TEXT_REJECT = "Отказать"
TEXT_LINKS = "+ ссылки"
TEXT_BOT_DESCRIPTION = "Через этот бот можно присылать фото и видео для публикации в канале @vputite"
TEXT_HELP = "Помощь"
TEXT_WELCOME = "Здравствуйте"
TEXT_WELCOME_DESCRIPTION = "На связи с вами для формирования актуальной информации о ситуации в общественном транспорте"
TEXT_SUBMIT_CONFIRMATION = "Ваше сообщение отправлено на рассмотрение"
TEXT_SUBMIT_ERROR = "Ошибка при отправлении сообщения"
TEXT_SUBMIT_RULES = "Пришлите пожалуйста фотографию и описание"
TEXT_PHOTO_REQUEST = "Пришлите пожалуйста фотографию"
TEXT_CAPTION_REQUEST = "Пришлите пожалуйста описание"
TEXT_THANKS = "Спасибо за информацию, после одобрения модератором, она будет размещена в канале"
TEXT_USER_REJECT_CONFIRMATION = "К сожалению модераторы отклонили публикацию"
TEXT_USER_APPROVE_CONFIRMATION = "Сообщение отправлено в канал"
TEXT_ADMIN_REJECT_CONFIRMATION = "Отклонено администратором"
TEXT_ADMIN_APPROVE_CONFIRMATION = "Одобрено администратором"
TEXT_SUBSCRIBE = "Подписаться на канал"
TEXT_SENDINFO = "Прислать информацию"

LINK_TO_CHANNEL="https://t.me/" + CHANNEL_NAME.replace("@", "")
# LINK_TO_SUBSCRIBE="https://t.me/" + CHANNEL_NAME.replace("@", "")
HTML_SUBSCRIBE_LINK = "<a href='" + LINK_TO_CHANNEL + "'>Подписаться на канал</a>"   # parse_mode = ParseMode.HTML
# TODO: get it dynamic
HTML_SENDINFO_LINK = "<a href='https://t.me/vputite_reportbot'>Прислать информацию</a>" # parse_mode = ParseMode.HTML
HTML_INFO = HTML_SUBSCRIBE_LINK + "\n" + HTML_SENDINFO_LINK # parse_mode = ParseMode.HTML

def getValue(v):
        if type(v) == type(list()):
                print("This is a list of {} items!".format(len(v)))
        
                r_idx=random.randint(0, len(v)-1)
                print(r_idx)
                return v[r_idx]

        if isinstance(v, str):
                print("This is a string!")
                return v

        return str(v)