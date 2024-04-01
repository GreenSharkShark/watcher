from celery import shared_task
from config.settings import Session
from watcher.functions import send_a_notification_about_new_episode
from watcher.models import Serial
from watcher.parser import kinogo_by_parser


@shared_task
def check_for_updates():
    with Session() as session:
        last_registered_episode_in_all_serials = session.query(Serial).all()
        for serial in last_registered_episode_in_all_serials:
            last_episode_on_website = kinogo_by_parser(serial.url)
            if last_episode_on_website != serial.last_episode:
                watching_users = serial.watching_users
                notification = f"У сериала {serial.url} вышла новая серия {last_episode_on_website}"
                send_a_notification_about_new_episode(watching_users, notification)
                serial.last_episode = last_episode_on_website
        session.commit()
