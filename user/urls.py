from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path("login", views.login, name="login"),
    path("login_check", views.login_check, name="login_check"),
    path("register", views.register_view, name="register"),
    path("confirm_register", views.register, name="confirm_register"),
    path("logout", views.logout, name="logout"),
    # path("admin",views.admin_view,name="admin"),
    # path("my_profile", views.my_profile, name="my_profile"),
    # path("update_profile", views.update_profile, name="update_profile"),
    # path("change_password", views.change_password, name="change_password")
]
