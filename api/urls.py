from django.urls import path
from . import views
from .views import search


urlpatterns = [
    path('rank', views.AverageRanker.as_view(), name = "ranker"),
    path('search', search), 
]
