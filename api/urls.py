from django.contrib import admin
from django.urls import path
from . import views
from .views import search

urlpatterns = [
    path('site-data/', views.data),
    path('campaign/', views.CampaignView.as_view(), name='campaign'),
	path('campaign/<int:pk>/', views.CampaignView.as_view(), name='campaign-user-id'),
    path('rank', views.AverageRanker.as_view(), name = "ranker"),
    path('search', search), 
]

