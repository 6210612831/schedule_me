from time import daylight
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from pandas import notnull
from zmq import NULL
from .models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from collections import OrderedDict
# Index view


def index(request):
    schedule_tables = schedule_table(request)
    return render(request, "schedule/index.html", {"schedule_data": schedule_tables})


def index2(request):
    schedule_tables = schedule_table(request)
    return render(request, "schedule/index2.html", {"schedule_data": schedule_tables})


# Select Day for find free time (start hour)
def index_day(request, day):
    temp = []
    data = Day.objects.get(user=request.user, day_code=day)

    # Get schedule table data
    schedule_data = schedule_table(request)

    for x in data.todolist_id.all():
        temp.append(x.td_start)
        temp.append(x.td_end)

    if len(temp) != 0:
        # clean data time_stamp
        i = 0
        time_stamp = []
        while i < len(temp):
            time_stamp.append([((temp[i].hour * 60) + temp[i].minute),
                               ((temp[i+1].hour * 60) + temp[i+1].minute)])
            i += 2
        time_stamp.sort()
    else:
        time_stamp = [[0, 0]]
        # find free time
    free_time = []
    temp_free_hr = []
    i = 0
    if (time_stamp[0][0] != 0):
        free_time.append([0, time_stamp[0][0]-1])
        m = 0
        while m <= time_stamp[0][0]-1:
            temp_free_hr.append(int(m/60))
            m += 1
    if (time_stamp[-1][1] != 1439):
        free_time.append([time_stamp[-1][1]+1, 1439])
        m = time_stamp[-1][1]+1
        while m <= 1439:
            temp_free_hr.append(int(m/60))
            m += 1
    while i < len(time_stamp)-1:
        free_time.append([time_stamp[i][1]+1, time_stamp[i+1][0]-1])
        m = time_stamp[i][1]+1
        while m <= time_stamp[i+1][0]-1:
            temp_free_hr.append(int(m/60))
            m += 1
        i += 1
    free_time.sort()
    temp_free_hr.sort()
    free_hr = list(OrderedDict.fromkeys(temp_free_hr))

    task = Task.objects.filter(user=request.user)

    return render(request, "schedule/index.html", {
        "free_time": free_time,
        "free_hr_start": free_hr,
        "task": task,
        "day": day,
        "schedule_data": schedule_data,
    })


# comment old code
def comment(request):
    # def schedule_table(request, day):
    # def schedule_table(request, day):
    #     temp = []
    #     thing_temp = []
    #     data = Day.objects.get(user=request.user, day_code=day)

    #     for x in data.todolist_id.all():
    #         temp.append(x.td_start)
    #         temp.append(x.td_end)
    #         thing_temp.append(x.td_thing)

    #     if len(temp) != 0:
    #         # clean data schedule_data
    #         i = 0
    #         j = 0
    #         schedule_data = []
    #         while i < len(temp):
    #             schedule_data.append([((temp[i].hour * 60) + temp[i].minute),
    #                                   ((temp[i+1].hour * 60) + temp[i+1].minute),
    #                                   thing_temp[j]])
    #             i += 2
    #             j += 1
    #         schedule_data.sort()
    #     else:
    #         schedule_data = [[0, 1439, "Void"]]

    #     free_time = []
    #     i = 0
    #     if (schedule_data[0][0] != 0):
    #         free_time.append([0, schedule_data[0][0]-1, "Void"])
    #     if (schedule_data[-1][1] != 1439):
    #         free_time.append([schedule_data[-1][1]+1, 1439, "Void"])
    #     while i < len(schedule_data)-1:
    #         free_time.append(
    #             [schedule_data[i][1]+1, schedule_data[i+1][0]-1, "Void"])
    #         i += 1
    #     free_time.sort()

    #     comeplete_schedule = schedule_data + free_time
    #     comeplete_schedule.sort()

    #     return comeplete_schedule
    pass


# def schedule_table(request, day):
def schedule_table(request):
    schedule_day = []
    if(request.user.is_authenticated):
        for data in Day.objects.filter(user=request.user):
            temp = []
            thing_temp = []
            schedule_data = []
            for x in data.todolist_id.all():
                temp.append(x.td_start)
                temp.append(x.td_end)
                temp.append(x.td_id)
                thing_temp.append(x.td_thing)

            if len(temp) != 0:
                # clean data schedule_data
                i = 0
                j = 0

                while i < len(temp):
                    schedule_data.append([((temp[i].hour * 60) + temp[i].minute),
                                          ((temp[i+1].hour * 60) +
                                           temp[i+1].minute),
                                          thing_temp[j], temp[i+2]])
                    i += 3
                    j += 1
                schedule_data.sort()
            else:
                schedule_data = [[0, 1439, "-", -1]]

            free_time = []
            i = 0
            if (schedule_data[0][0] != 0):
                free_time.append([0, schedule_data[0][0]-1, "-", -1])
            if (schedule_data[-1][1] != 1439):
                free_time.append([schedule_data[-1][1]+1, 1439, "-", -1])
            while i < len(schedule_data)-1:
                free_time.append(
                    [schedule_data[i][1]+1, schedule_data[i+1][0]-1, "-", -1])
                i += 1
            free_time.sort()

            comeplete_schedule = schedule_data + free_time
            comeplete_schedule.sort()
            schedule_day.append([comeplete_schedule, data.day_code])
        return schedule_day
    else:
        return []


# Default Assign Data
def defualt_index(request, day):
    temp = []
    data = Day.objects.get(user=request.user, day_code=day)

    for x in data.todolist_id.all():
        temp.append(x.td_start)
        temp.append(x.td_end)

    if len(temp) != 0:
        # clean data time_stamp
        i = 0
        time_stamp = []
        while i < len(temp):
            time_stamp.append([((temp[i].hour * 60) + temp[i].minute),
                               ((temp[i+1].hour * 60) + temp[i+1].minute)])
            i += 2
        time_stamp.sort()
    else:
        time_stamp = []
    # find free time
    free_time = []
    temp_free_hr = []
    i = 0

    if len(time_stamp) != 0:
        if (time_stamp[0][0] != 0):
            free_time.append([0, time_stamp[0][0]-1])
            m = 0
            while m <= time_stamp[0][0]-1:
                temp_free_hr.append(int(m/60))
                m += 1
        if (time_stamp[-1][1] != 1439):
            free_time.append([time_stamp[-1][1]+1, 1439])
            m = time_stamp[-1][1]+1
            while m <= 1439:
                temp_free_hr.append(int(m/60))
                m += 1
        while i < len(time_stamp)-1:
            free_time.append([time_stamp[i][1]+1, time_stamp[i+1][0]-1])
            m = time_stamp[i][1]+1
            while m <= time_stamp[i+1][0]-1:
                temp_free_hr.append(int(m/60))
                m += 1
            i += 1
    else:
        free_time = [[0, 1439]]
        for x in range(0, 24):
            temp_free_hr.append(x)
    free_time.sort()
    temp_free_hr.sort()
    free_hr = list(OrderedDict.fromkeys(temp_free_hr))

    # define remain task
    task = Task.objects.filter(user=request.user)

    # define remain todolist
    # todolist = Todolist.objects.filter(user=request.user)
    return ([free_time, free_hr, time_stamp, task, day])


# Search for free start min
def index_start_hr(request, day, start_hr):
    data = defualt_index(request, day)
    free_time = data[0]
    free_hr_start = data[1]
    task = data[3]

    # Get schedule table data
    schedule_data = schedule_table(request)

    # find free_min_start
    temp_free_min_start = []
    free_min_start = []
    for x in free_time:
        if int(x[0]/60) <= int(start_hr) <= int(x[1]/60):
            m = (int(x[0]))
            while m <= x[1] and m < ((int(start_hr)+1)*60):
                if int(start_hr) == 0:
                    if int(m/(60)) < 1:
                        temp_free_min_start.append(int(m))
                    m += 1
                else:
                    if int(m/(int(start_hr)*60)) == 1:
                        temp_free_min_start.append(int(m % (int(start_hr)*60)))
                    m += 1
    temp_free_min_start.sort()
    free_min_start = list(OrderedDict.fromkeys(temp_free_min_start))

    return render(request, "schedule/index.html", {
        "day": day,
        "task": task,
        "free_time": free_time,
        "free_hr_start": free_hr_start,
        # implement start hr
        "start_hr": start_hr,
        "free_min_start": free_min_start,
        # "free_min_start": temp_free_min_start,
        "schedule_data": schedule_data,
    })


# Search for free end hour
def index_start_min(request, day, start_hr, start_min):
    data = defualt_index(request, day)
    free_time = data[0]
    free_hr_start = data[1]
    time_stamp = data[2]
    task = data[3]

    # Get schedule table data
    schedule_data = schedule_table(request)

    # find free_min_start
    temp_free_min_start = []
    free_min_start = []
    for x in free_time:
        if int(x[0]/60) <= int(start_hr) <= int(x[1]/60):
            m = (int(x[0]))
            while m <= x[1] and m < ((int(start_hr)+1)*60):
                if int(start_hr) == 0:
                    if int(m/(60)) < 1:
                        temp_free_min_start.append(int(m))
                    m += 1
                else:
                    if int(m/(int(start_hr)*60)) == 1:
                        temp_free_min_start.append(int(m % (int(start_hr)*60)))
                    m += 1
    temp_free_min_start.sort()
    free_min_start = list(OrderedDict.fromkeys(temp_free_min_start))

    # find free time end
    temp_free_hr_end = []
    i = 0

    if len(time_stamp) != 0:
        if (time_stamp[0][0] != 0):
            m = 0
            while m <= time_stamp[0][0]-1:
                if m > ((int(start_hr)*60)+int(start_min)):
                    temp_free_hr_end.append(int(m/60))
                m += 1
        if (time_stamp[-1][1] != 1439):
            m = time_stamp[-1][1]+1
            while m <= 1439:
                if m > ((int(start_hr)*60)+int(start_min)):
                    temp_free_hr_end.append(int(m/60))
                m += 1
        while i < len(time_stamp)-1:
            m = time_stamp[i][1]+1
            while m <= time_stamp[i+1][0]-1:
                if m > ((int(start_hr)*60)+int(start_min)):
                    temp_free_hr_end.append(int(m/60))
                m += 1
            i += 1
    else:
        m = 0
        while m <= 1439:
            if m > ((int(start_hr)*60)+int(start_min)):
                temp_free_hr_end.append(int(m/60))
            m += 1
    temp_free_hr_end.sort()
    free_hr_end = list(OrderedDict.fromkeys(temp_free_hr_end))

    return render(request, "schedule/index.html", {
        "day": day,
        "task": task,
        "free_time": free_time,
        "free_hr_start": free_hr_start,
        # implement start hr
        "start_hr": start_hr,
        "free_min_start": free_min_start,
        # implement end hr
        "start_min": start_min,
        "free_hr_end": free_hr_end,
        # "temp_free_hr_end": temp_free_hr_end,
        "schedule_data": schedule_data,
    })


# Search for free end minute
def index_end_hr(request, day,  start_hr, start_min, end_hr):
    data = defualt_index(request, day)
    free_time = data[0]
    free_hr_start = data[1]
    time_stamp = data[2]
    task = data[3]

    # Get schedule table data
    schedule_data = schedule_table(request)

    # find free_min_start
    temp_free_min_start = []
    free_min_start = []
    for x in free_time:
        if int(x[0]/60) <= int(start_hr) <= int(x[1]/60):
            m = (int(x[0]))
            while m <= x[1] and m < ((int(start_hr)+1)*60):
                if int(start_hr) == 0:
                    if int(m/(60)) < 1:
                        temp_free_min_start.append(int(m))
                    m += 1
                else:
                    if int(m/(int(start_hr)*60)) == 1:
                        temp_free_min_start.append(int(m % (int(start_hr)*60)))
                    m += 1
    temp_free_min_start.sort()
    free_min_start = list(OrderedDict.fromkeys(temp_free_min_start))

    # find free_hr_end
    temp_free_hr_end = []
    i = 0

    if len(time_stamp) != 0:
        if (time_stamp[0][0] != 0):
            m = 0
            while m <= time_stamp[0][0]-1:
                if m > ((int(start_hr)*60)+int(start_min)):
                    temp_free_hr_end.append(int(m/60))
                m += 1
        if (time_stamp[-1][1] != 1439):
            m = time_stamp[-1][1]+1
            while m <= 1439:
                if m > ((int(start_hr)*60)+int(start_min)):
                    temp_free_hr_end.append(int(m/60))
                m += 1
        while i < len(time_stamp)-1:
            m = time_stamp[i][1]+1
            while m <= time_stamp[i+1][0]-1:
                if m > ((int(start_hr)*60)+int(start_min)):
                    temp_free_hr_end.append(int(m/60))
                m += 1
            i += 1
    else:
        m = 0
        while m <= 1439:
            if m > ((int(start_hr)*60)+int(start_min)):
                temp_free_hr_end.append(int(m/60))
            m += 1

    temp_free_hr_end.sort()
    free_hr_end = list(OrderedDict.fromkeys(temp_free_hr_end))

    # find free_min_end
    temp_free_min_end = []
    free_min_end = []
    for x in free_time:
        if int(x[0]/60) <= int(end_hr) <= int(x[1]/60):
            m = (int(x[0]))
            while m <= x[1] and m < ((int(end_hr)+1)*60):
                if int(end_hr) == 0:
                    if int(m/60) < 1:
                        if m > ((int(start_hr)*60)+int(start_min)):
                            temp_free_min_end.append(int(m))
                    m += 1
                else:
                    if int(m/(int(end_hr)*60)) == 1:
                        if m > ((int(start_hr)*60)+int(start_min)):
                            temp_free_min_end.append(int(m % (int(end_hr)*60)))
                    m += 1
    temp_free_min_end.sort()
    free_min_end = list(OrderedDict.fromkeys(temp_free_min_end))

    return render(request, "schedule/index.html", {
        "day": day,
        "task": task,
        "free_time": free_time,
        "free_hr_start": free_hr_start,
        # implement by start hr
        "start_hr": start_hr,
        "free_min_start": free_min_start,
        # implement by start min
        "start_min": start_min,
        "free_hr_end": free_hr_end,
        # implement by end hr
        "end_hr": end_hr,
        "free_min_end": free_min_end,
        # "temp_free_hr_end": temp_free_hr_end,
        "schedule_data": schedule_data,
    })


# INSERT TODOLIST
def insert_schdule(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login First to proceed")
        return HttpResponseRedirect(reverse("schedule:index"))

    if request.method == "POST":
        day = request.POST["day"]
        td_thing = request.POST["td_thing"]
        start_hr = request.POST["start_hr"]
        start_min = request.POST["start_min"]
        end_hr = request.POST["end_hr"]
        end_min = request.POST["end_min"]
        task_id = request.POST["task_id"]

        start_time = start_hr+":"+start_min
        end_time = end_hr + ":" + end_min
        task = Task.objects.get(task_id=task_id)
        new_todolist = Todolist.objects.create(td_thing=td_thing, td_start=start_time, td_end=end_time,
                                               task=task, user=request.user)
        new_todolist.save()
        new_day = Day.objects.get(day_code=day, user=request.user)
        new_day.todolist_id.add(new_todolist)
        new_day.save()
        return HttpResponseRedirect(reverse("schedule:index"))
    else:
        return HttpResponseRedirect(reverse("schedule:index"))


# Search Todolist for Delete in A Day
def search_day_todolist(request, day_delete):
    todolist_for_delete = []
    data = Day.objects.get(user=request.user, day_code=day_delete)

    # Get schedule table data
    schedule_data = schedule_table(request)

    for x in data.todolist_id.all():
        todolist_for_delete.append(x)

    return render(request, "schedule/index.html", {
        "todolist_for_delete": todolist_for_delete,
        "day_delete": day_delete,
        "schedule_data": schedule_data,
    })


# Delete Todolist in A Day
def delete_day_todolist(request, day_delete, td_id):
    td_item = Todolist.objects.get(td_id=td_id, user=request.user)
    day = Day.objects.get(user=request.user, day_code=day_delete)
    day.todolist_id.remove(td_item)
    day.save()

    # Get schedule table data
    schedule_data = schedule_table(request)

    return render(request, "schedule/index.html", {"schedule_data": schedule_data, })


# Search Todolist for Delete
def search_todolist(request):
    todolist = []
    search_check = 1

    if request.method == "POST":
        search = request.POST["search"]
        for x in Todolist.objects.filter(user=request.user).all():
            if x.search(search):
                todolist.append(x)
    else:
        for x in Todolist.objects.filter(user=request.user).all():
            todolist.append(x)

    # Get schedule table data
    schedule_data = schedule_table(request)

    return render(request, "schedule/index.html", {
        "todolist": todolist,
        "search_check": search_check,
        "schedule_data": schedule_data,
    })


# Delete Todolist
def delete_todolist(request, td_id):
    Todolist.objects.get(td_id=td_id, user=request.user).delete()
    return render(request, "schedule/index.html")


# INSERT TODOLIST
def insert_todolist_schdule(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login First to proceed")
        return HttpResponseRedirect(reverse("schedule:index"))

    if request.method == "POST":
        day = request.POST["day"]
        td_thing = request.POST["td_thing"]
        start_hr = request.POST["start_hr"]
        start_min = request.POST["start_min"]
        end_hr = request.POST["end_hr"]
        end_min = request.POST["end_min"]
        task_id = request.POST["task_id"]

        start_time = start_hr+":"+start_min
        end_time = end_hr + ":" + end_min
        task = Task.objects.get(task_id=task_id)
        new_todolist = Todolist.objects.create(td_thing=td_thing, td_start=start_time, td_end=end_time,
                                               task=task, user=request.user)
        new_todolist.save()
        new_day = Day.objects.get(day_code=day, user=request.user)
        new_day.todolist_id.add(new_todolist)
        new_day.save()
        return HttpResponseRedirect(reverse("schedule:index"))
    else:
        return HttpResponseRedirect(reverse("schedule:index"))


def index_day_todolist(request, day):
    temp = []
    data = Day.objects.get(user=request.user, day_code=day)

    # Get schedule table data
    schedule_data = schedule_table(request)

    for x in data.todolist_id.all():
        temp.append(x.td_start)
        temp.append(x.td_end)

    if len(temp) != 0:
        # clean data time_stamp
        i = 0
        time_stamp = []
        while i < len(temp):
            time_stamp.append([((temp[i].hour * 60) + temp[i].minute),
                               ((temp[i+1].hour * 60) + temp[i+1].minute)])
            i += 2
        time_stamp.sort()
    else:
        time_stamp = [[0, 0]]
        # find free time
    free_time = []
    i = 0
    if (time_stamp[0][0] != 0):
        free_time.append([0, time_stamp[0][0]-1])
    if (time_stamp[-1][1] != 1439):
        free_time.append([time_stamp[-1][1]+1, 1439])
    while i < len(time_stamp)-1:
        free_time.append([time_stamp[i][1]+1, time_stamp[i+1][0]-1])
        i += 1
    free_time.sort()
    # free_time = [[0,0],[1,1]]
    can_insert_todolist = []

    for x in Todolist.objects.filter(user=request.user):
        for y in free_time:
            if (x.td_start.hour * 60)+(x.td_start.minute) >= y[0] and (x.td_end.hour * 60)+(x.td_end.minute) <= y[1]:
                if len(can_insert_todolist) != 0:
                    if [x.td_id, x.td_thing] != can_insert_todolist[-1]:
                        can_insert_todolist.append([x.td_id, x.td_thing])
                else:
                    can_insert_todolist.append([x.td_id, x.td_thing])

    can_insert_todolist.sort()
    # can_insert_todolists = list(OrderedDict.fromkeys(can_insert_todolist))

    return render(request, "schedule/index.html", {
        "can_insert_todolists": can_insert_todolist,
        "day_insert_todolist": day,
        "schedule_data": schedule_data,
    })


# INSERT EXIST TODOLIST
def insert_exist_todolist_schdule(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login First to proceed")
        return HttpResponseRedirect(reverse("schedule:index"))

    if request.method == "POST":
        day = request.POST["day_todolist"]
        td_id = request.POST["todolist"]
        todolist = Todolist.objects.get(td_id=td_id)
        new_day = Day.objects.get(day_code=day, user=request.user)
        new_day.todolist_id.add(todolist)
        new_day.save()
        return HttpResponseRedirect(reverse("schedule:index"))
    else:
        return HttpResponseRedirect(reverse("schedule:index"))
