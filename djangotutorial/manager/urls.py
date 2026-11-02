from django.urls import path

from . import views

app_name = "manager"
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("app_conf/", views.app_conf, name="app_conf"),
    path("toggle_app/<int:app_id>/", views.toggle_app , name="toggle_app"),
]