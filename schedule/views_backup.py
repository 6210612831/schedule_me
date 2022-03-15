from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from pandas import notnull
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
    temp = []
    data = Day.objects.get(user=request.user)
    for x in data.todolist_id.all():
        temp.append(x.td_start)
        temp.append(x.td_end)

    # clean data time_stamp
    i = 0
    time_stamp = []
    while i < len(temp):
        time_stamp.append([((temp[i].hour * 60) + temp[i].minute),
                           ((temp[i+1].hour * 60) + temp[i+1].minute)])
        i += 2
    time_stamp.sort()

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

    return render(request, "schedule/index.html", {
        "check": time_stamp,
        "free_time": free_time,
        "free_hr_start": free_hr,
    })


def index_start_hr(request, start_hr):
    temp = []
    data = Day.objects.get(user=request.user)
    for x in data.todolist_id.all():
        temp.append(x.td_start)
        temp.append(x.td_end)

    # clean data time_stamp
    i = 0
    time_stamp = []
    while i < len(temp):
        time_stamp.append([((temp[i].hour * 60) + temp[i].minute),
                           ((temp[i+1].hour * 60) + temp[i+1].minute)])
        i += 2
    time_stamp.sort()

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

    # find free_min_start
    temp_free_min_start = []
    free_min_start = []
    for x in free_time:
        if int(x[0]/60) <= int(start_hr) <= int(x[1]/60):
            m = (int(x[0]))
            while m <= x[1] and m < ((int(start_hr)+1)*60):
                if int(m/(int(start_hr)*60)) == 1:
                    temp_free_min_start.append(int(m % (int(start_hr)*60)))
                m += 1
    temp_free_min_start.sort()
    free_min_start = list(OrderedDict.fromkeys(temp_free_min_start))

    return render(request, "schedule/index.html", {
        "free_time": free_time,
        "free_hr_start": free_hr,
        # implement start hr
        "start_hr": start_hr,
        "free_min_start": free_min_start,
        # "free_min_start": temp_free_min_start,
    })


def index_start_hr_backup(request, start_hr):
    temp = []
    data = Day.objects.get(user=request.user)
    for x in data.todolist_id.all():
        temp.append(x.td_start)
        temp.append(x.td_end)

    # clean data time_stamp
    i = 0
    time_stamp = []
    while i < len(temp):
        time_stamp.append([((temp[i].hour * 60) + temp[i].minute),
                           ((temp[i+1].hour * 60) + temp[i+1].minute)])
        i += 2
    time_stamp.sort()

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

    # find free_min_start
    temp_free_min_start = []
    free_min_start = []
    for x in free_time:
        if int(x[0]/60) <= int(start_hr) <= int(x[1]/60):
            m = (int(x[0]))
            while m <= x[1] and m < ((int(start_hr)+1)*60):
                if int(m/(int(start_hr)*60)) == 1:
                    temp_free_min_start.append(int(m % (int(start_hr)*60)))
                m += 1
    temp_free_min_start.sort()
    free_min_start = list(OrderedDict.fromkeys(temp_free_min_start))

    return render(request, "schedule/index.html", {
        "check": time_stamp,
        "free_time": free_time,
        "free_hr_start": free_hr,
        # implement start hr
        "start_hr": start_hr,
        "free_min_start": free_min_start,
        # "free_min_start": temp_free_min_start,
    })


def index_start_min(request, start_hr, start_min):
    temp = []
    data = Day.objects.get(user=request.user)
    for x in data.todolist_id.all():
        temp.append(x.td_start)
        temp.append(x.td_end)

    # clean data time_stamp
    i = 0
    time_stamp = []
    while i < len(temp):
        time_stamp.append([((temp[i].hour * 60) + temp[i].minute),
                           ((temp[i+1].hour * 60) + temp[i+1].minute)])
        i += 2
    time_stamp.sort()

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

    # find free_min_start
    temp_free_min_start = []
    free_min_start = []
    for x in free_time:
        if int(x[0]/60) <= int(start_hr) <= int(x[1]/60):
            m = (int(x[0]))
            while m <= x[1] and m < ((int(start_hr)+1)*60):
                if int(m/(int(start_hr)*60)) == 1:
                    temp_free_min_start.append(int(m % (int(start_hr)*60)))
                m += 1
    temp_free_min_start.sort()
    free_min_start = list(OrderedDict.fromkeys(temp_free_min_start))

    # find free time end
    temp_free_hr_end = []
    i = 0
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
    temp_free_hr_end.sort()
    free_hr_end = list(OrderedDict.fromkeys(temp_free_hr_end))

    return render(request, "schedule/index.html", {
        "check": time_stamp,
        "free_time": free_time,
        "free_hr_start": free_hr,
        # implement start hr
        "start_hr": start_hr,
        "free_min_start": free_min_start,
        # implement end hr
        "start_min": start_min,
        "free_hr_end": free_hr_end,
        # "temp_free_hr_end": temp_free_hr_end,
    })


def index_end_hr(request, start_hr, start_min, end_hr):
    temp = []
    data = Day.objects.get(user=request.user)
    for x in data.todolist_id.all():
        temp.append(x.td_start)
        temp.append(x.td_end)

    # clean data time_stamp
    i = 0
    time_stamp = []
    while i < len(temp):
        time_stamp.append([((temp[i].hour * 60) + temp[i].minute),
                           ((temp[i+1].hour * 60) + temp[i+1].minute)])
        i += 2
    time_stamp.sort()

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

    # find free_min_start
    temp_free_min_start = []
    free_min_start = []
    for x in free_time:
        if int(x[0]/60) <= int(start_hr) <= int(x[1]/60):
            m = (int(x[0]))
            while m <= x[1] and m < ((int(start_hr)+1)*60):
                if int(m/(int(start_hr)*60)) == 1:
                    temp_free_min_start.append(int(m % (int(start_hr)*60)))
                m += 1
    temp_free_min_start.sort()
    free_min_start = list(OrderedDict.fromkeys(temp_free_min_start))

    # find free_hr_end
    temp_free_hr_end = []
    i = 0
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
    temp_free_hr_end.sort()
    free_hr_end = list(OrderedDict.fromkeys(temp_free_hr_end))

    # find free_min_start
    temp_free_min_end = []
    free_min_end = []
    for x in free_time:
        if int(x[0]/60) <= int(end_hr) <= int(x[1]/60):
            m = (int(x[0]))
            while m <= x[1] and m < ((int(end_hr)+1)*60):
                if int(m/(int(end_hr)*60)) == 1:
                    if m > ((int(start_hr)*60)+int(start_min)):
                        temp_free_min_end.append(int(m % (int(end_hr)*60)))
                m += 1
    temp_free_min_end.sort()
    free_min_end = list(OrderedDict.fromkeys(temp_free_min_end))

    return render(request, "schedule/index.html", {
        "check": time_stamp,
        "free_time": free_time,
        "free_hr_start": free_hr,
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
    })


def insert_schdule(request):
    # Check user is already login
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse("schedule:index"))
    # # Check this view use when submit login or not if not return to index
    # if request.method == "POST":
    #     # login process
    #     username = request.POST["username"]
    #     password = request.POST["password"]
    #     user = authenticate(request, username=username, password=password)
    #     if user is not None:
    #         auth_login(request, user)
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    #     else:
    #         messages.warning(request, "Invalid credential")
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    # return render(request, "dormitory/index.html")
    pass
