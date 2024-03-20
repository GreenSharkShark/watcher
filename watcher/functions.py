from config.settings import Session, bot
from watcher.models import Site, User


def parse_url(url: str) -> str or dict:
    """ Парсит ссылку на сайт, чтобы убедиться что с этого сайта можно парсить инфу """
    try:
        site = url.split('/')
        return {'site': site[2]}
    except IndexError:
        return {'error': 'Вы ввели неверную ссылку. Ссылка должна быть в формате "https://название.сайта/..."'}


def make_new_site_object(site_url: str, site_name: str) -> None:
    """ Функция для ручного создания объектов модели Site. Просто запустить один раз
    с нужными параметрами когда добавляется новый сайт в список доступных для отслеживания """
    with Session() as session:
        new_site = Site(url=site_url, name=site_name)
        session.add(new_site)
        session.commit()


# make_new_site_object('https://kinogo.fm/', 'kinogo.fm')


def send_a_notification_about_new_episode(watching_users: list, notification: str) -> None:
    """ Отправляет уведомление о выходе новой серии """

    for user in watching_users:
        telegram_id = user.tg_user_id
        bot.send_message(telegram_id, notification)


def save_user_data(message) -> None:
    """ Сохраняет данные пользователя при первом старте бота """
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
            notif = 'Пользователь уже зарегистрирован'
            bot.send_message(message.from_user.id, notif)
