import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TOR_VM.settings')

app = Celery('TOR_VM', broker='amqp://guest@localhost//')
app.config_from_object('django.conf:settings')
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()
