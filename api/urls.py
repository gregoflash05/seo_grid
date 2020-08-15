from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    path('dashboard/', views.dashboard, name="logout"),
    # path('campaign/', views.CampaignView.as_view(), name='campaign'),
	# path('campaign/<int:pk>/', views.CampaignView.as_view(), name='campaign-user-id'),

    path('campaign/<int:pk>/', views.campaign_info_by_id, name='campaign-user-id'),
    path('campaign/', views.CampaignInfoView, name='campaign'),
    path('campaign_user/', views.CampaignInfoByUser, name='campaign'),

    path('keyword/<int:pk>/', views.Keyword_info_by_id, name='Keywords'),
    path('keyword/', views.KeywordsInfoView, name='Keywords'),
    path('keyword_campaign/', views.KeywordsInfoByCampaign, name='Keywords'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)