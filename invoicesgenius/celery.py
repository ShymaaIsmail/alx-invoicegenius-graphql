import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'invoicesgenius.settings')

app = Celery('invoicesgenius')

# Load settings from Django with CELERY_ namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Explicit SSL config for rediss (Upstash Redis)
app.conf.broker_use_ssl = {
    'ssl_cert_reqs': None  # Disable cert verification, required for Upstash
}

app.autodiscover_tasks()

# Optional: Configure periodic tasks
app.conf.beat_schedule = {
    'process-invoices-every-10-minutes': {
        'task': 'invoices.tasks.process_pending_invoices',
        'schedule': 600.0,  # every 10 minutes
    },
}
