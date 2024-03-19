from celery import Celery
from datetime import timedelta
from config.settings import CELERY_BROKER_URL
from watcher.celery_tasks import check_for_updates


app = Celery('config', broker=CELERY_BROKER_URL)
app.conf.timezone = 'UTC'
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check_for_updates': {
        'task': 'watcher.celery_tasks.check_for_updates',
        'schedule': timedelta(hours=1,)
    },
}
