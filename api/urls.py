from django.urls import path
from . import views

urlpatterns = [
	path('campaign/', views.CampaignView.as_view(), name='campaign'),
	path('campaign/<int:pk>/', views.CampaignView.as_view(), name='campaign-user-id'),
    path('rank', views.AverageRanker.as_view(), name = "ranker"),
	path('get_seo_data', views.get_seo_data, name = "compare"),
]