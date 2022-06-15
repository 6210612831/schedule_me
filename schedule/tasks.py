from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django_celery_beat.models import PeriodicTask,IntervalSchedule
from datetime import timedelta, datetime
# from schedule.models import Task
# from datetime import datetime
# from django.utils import timezone
import requests

TOKEN = 'Bearer VaQiVzn5SqjJysdYSblOaJuS5xCBDw3qucIfzmJPyI5'

@shared_task
def line_alert(task_name):
    global TOKEN
    requests.post("https://notify-api.line.me/api/notify",headers={'Authorization': TOKEN},data={"message":f"{task_name}"})

    # Update celery next week
    pre = PeriodicTask.objects.get(name=task_name)
    old = pre.start_time
    new = old + timedelta(days=7)
    pre.start_time=new
    pre.enabled = True
    pre.save()

    return "Done line_alert()"

