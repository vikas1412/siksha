from django.urls import path

from create_exam import views

urlpatterns = [
    path("", views.home, name="home"),
]