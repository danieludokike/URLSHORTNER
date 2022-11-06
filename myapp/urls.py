from django.urls import path
from .views import (home_view, user_login,
                    register_view, user_logout,
                    add_url_view, delete_url_view, get_url, text_to_speech_view
)

app_name = "myapp"
urlpatterns = [
    path("", home_view, name="home"),
    path("convert-text-to-speech/", text_to_speech_view, name="text_to_speech"),
    path("login/", user_login, name="user_login"),
    path("register/", register_view, name="register"),
    path("logout/", user_logout, name="user_logout"),
    path("add_url/", add_url_view, name="add_url"),
    path("delete-url/<int:id>/", delete_url_view, name="delete_url"),
    path("<str:slug>/", get_url, name="get_url"),
]