from django.urls import path

from . import views

app_name = 'schedule'
urlpatterns = [
    path("", views.index, name="index"),
    path("index2", views.index2, name="index2"),
    path("index_day/<str:day>",
         views.index_day, name="index_day"),

    path("index_start_hr/<str:day>/<str:start_hr>",
         views.index_start_hr, name="index_start_hr"),
    path("index_start_min/<str:day>/<str:start_hr>/<str:start_min>",
         views.index_start_min, name="index_start_min"),
    path("index_end_hr/<str:day>/<str:start_hr>/<str:start_min>/<str:end_hr>",
         views.index_end_hr, name="index_end_hr"),
    path("insert_schdule", views.insert_schdule, name="insert_schdule"),
    path("search_day_todolist/<str:day_delete>",
         views.search_day_todolist, name="search_day_todolist"),
    path("delete_day_todolist/<str:day_delete>/<str:td_id>",
         views.delete_day_todolist, name="delete_day_todolist"),
    path("search_todolist", views.search_todolist, name="search_todolist"),
    path("delete_todolist/<str:td_id>",
         views.delete_todolist, name="delete_todolist"),
    path("insert_todolist_schdule", views.insert_todolist_schdule,
         name="insert_todolist_schdule"),
    path("index_day_todolist/<str:day>",
         views.index_day_todolist, name="index_day_todolist"),

    path("test", views.test, name="test"),

]
