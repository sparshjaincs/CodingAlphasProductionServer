from django.urls import path
from . import views
urlpatterns = [
    path("",views.homepage,name="explore"),
    path("dailycontest/<title>/<id>/",views.daily,name="daily"),
]