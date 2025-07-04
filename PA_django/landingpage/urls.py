from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("socials/", views.socials, name="socials"),
    path("supported_brokers/", views.supported_brokers, name="supported_brokers"),
    path("pricing/", views.pricing, name="pricing"),
    path("about/", views.about, name="about"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
]