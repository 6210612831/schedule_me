from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schedule_me.settings')
app = Celery('schedule_me')
app.conf.broker_url = 'redis://localhost:6379/0'
app.autodiscover_tasks()