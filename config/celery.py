import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Use database as broker
app.conf.broker_url = 'db+postgresql://user:password@localhost/dbname'  # We'll use django-environ to set this