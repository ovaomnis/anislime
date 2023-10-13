import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'parse_from_tracker': {
        'task': 'apps.parser.tasks.parse_from_tracker',
        'schedule': crontab(minute=16, hour=15)
    }
}
