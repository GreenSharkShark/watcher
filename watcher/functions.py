from config.settings import Session, bot
from watcher.models import Site


def parse_url(url: str) -> str:
    """ Парсит ссылку на сайт, чтобы убедиться что с этого сайта можно парсить инфу """
    site = url.split('/')
    return site[2]


def make_new_site_object(site_url: str, site_name: str) -> None:
    """ Функция для ручного создания объектов модели Site. Просто запустить один раз
    с нужными параметрами когда добавляется новый сайт в список доступных для отслеживания """
    with Session() as session:
        new_site = Site(url=site_url, name=site_name)
        session.add(new_site)
        session.commit()


# make_new_site_object('https://kinogo.fm/', 'kinogo.fm')


def send_a_notificatio_about_new_episode(watching_users: list, notification: str):
    for user in watching_users:
        telegram_id = user.tg_user_id
        bot.send_message(telegram_id, notification)

