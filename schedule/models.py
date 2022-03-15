from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"task_id: {self.task_id} --|-- task_name:{self.task_name} --|-- user:{self.user}"


class Todolist(models.Model):
    td_id = models.AutoField(primary_key=True)
    td_thing = models.CharField(max_length=50)
    td_start = models.TimeField()
    td_end = models.TimeField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"td_id: {self.td_id} --|-- td_thing:{self.td_thing} --|-- td_start:{self.td_start} --|-- td_end:{self.td_end} --|-- user:{self.user}"


class Day(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day_code = models.CharField(max_length=2)
    todolist_id = models.ManyToManyField(Todolist, blank=True)

    def __str__(self):
        return f"id: {self.id} --|-- day:{self.day_code} --|-- user:{self.user} "
