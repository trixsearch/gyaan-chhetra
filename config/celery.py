import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Broker-agnostic configuration
broker_url = os.getenv('CELERY_BROKER_URL', 'django-db://')

app = Celery('gyaan_chhetra')

# Using database as broker initially
if broker_url.startswith('django-db://'):
    app.conf.broker_url = 'django://'
    app.conf.result_backend = 'django-db'
else:
    # Future: RabbitMQ/Redis
    app.conf.broker_url = broker_url
    app.conf.result_backend = broker_url

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Kolkata',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    worker_max_tasks_per_child=1000,
    worker_prefetch_multiplier=1,  # Fair dispatch
)

# Task routing
app.conf.task_routes = {
    'tasks.tasks.process_large_csv': {'queue': 'csv_processing'},
    'tasks.tasks.calculate_penalties': {'queue': 'penalty_calculation'},
    'tasks.tasks.generate_report': {'queue': 'report_generation'},
}