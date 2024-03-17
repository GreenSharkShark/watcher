import telebot
from config.settings import BOT_TOKEN, Session, SUPPORTED_SITES
from models import User, Serial, Site
from functions import parse_url

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_bot(message):
    """ Запускается при первом старте бота, сохраняет данные пользователя """

    with Session() as session:
        existing_user = session.query(User).filter_by(tg_user_id=message.from_user.id).first()
        if existing_user is None:
            new_user = User()
            new_user.username = message.from_user.username
            new_user.first_name = message.from_user.first_name
            new_user.last_name = message.from_user.last_name
            new_user.tg_user_id = message.from_user.id
            session.add(new_user)
            session.commit()
        else:
            pass
    bot.send_message(message.chat.id, 'Что умеет этот бот?')


@bot.message_handler(commands=['tracking'])
def tracking(message):
    """ Ожидает отправку пользователем ссылки на сериал """

    sent = bot.send_message(text='Отправьте ссылку на страницу с сериалом', chat_id=message.chat.id)
    bot.register_next_step_handler(sent, track)


def track(message):
    """ Парсит ссылку полученную из def tracking(message) """

    website = parse_url(message.text)
    if website in SUPPORTED_SITES:
        with Session() as session:
            user_object = session.query(User).filter_by(tg_user_id=message.from_user.id).first()
            new_serial = Serial()
            new_serial.url = message.text
            new_serial.site = session.query(Site).filter_by(name=website).first()
            new_serial.watching_users.append(user_object)
            session.add(new_serial)
            session.commit()

    else:
        bot.send_message(text='Сайт не поддерживается', chat_id=message.chat.id)
