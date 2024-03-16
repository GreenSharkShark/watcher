from settings import Session
from models import Site, User


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
