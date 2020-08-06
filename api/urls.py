from django.urls import path
from . import views


urlpatterns = [
    path('rank', views.AverageRanker.as_view(), name = "ranker"),
]
