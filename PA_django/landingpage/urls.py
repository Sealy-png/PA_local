from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("discord/", views.discord, name="discord"),
    path("socials/", views.socials, name="socials"),
]