from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    path('dashboard/', views.dashboard, name="Dashboard"),
    path('dashboard/<int:pk>/', views.camp_dashboard, name="Dashboard"),
    # path('campaign/', views.CampaignView.as_view(), name='campaign'),
	# path('campaign/<int:pk>/', views.CampaignView.as_view(), name='campaign-user-id'), 

    path('create_campaign/', views.Createcampaignpage, name="Create campaign"),
    path('edit_campaign/<int:pk>/', views.edit_campaign_info_by_id, name="Edit campaign"),

    path('edit_keyword/<int:pk>/', views.delete_keyword, name="Edit Keyword"),
    path('edit_keyword/', views.add_a_keyword, name="Edit Keyword"), 

    path('compare/<int:pk>/', views.compare_page, name="Compare keyword"), 
    path('url_compare/<int:pk>/', views.url_compare_data, name="Compare keyword"),
    path('url_compare_competitor/<int:pk>/', views.url_compare_competitor_data, name="Compare keyword"),

    path('url_compare_title/<int:pk>/', views.url_compare_data_title, name="Compare keyword"),
    path('url_compare_responsive/<int:pk>/', views.url_compare_data_responsive, name="Compare keyword"),
    path('url_compare_sitemap/<int:pk>/', views.url_compare_data_sitemap, name="Compare keyword"),
    path('url_compare_ssl_status/<int:pk>/', views.url_compare_data_ssl_status, name="Compare keyword"),
    path('url_compare_run_time/<int:pk>/', views.url_compare_data_run_time, name="Compare keyword"),
    path('ob_br_compare/<int:pk>/', views.ob_br_compare, name="Compare keyword"),

    path('url_compare_competitor_title/<int:pk>/', views.url_compare_competitor_title, name="Compare keyword"),
    path('url_compare_competitorr_responsive/<int:pk>/', views.url_compare_competitor_responsive, name="Compare keyword"),
    path('url_compare_competitor_sitemap/<int:pk>/', views.url_compare_competitor_sitemap, name="Compare keyword"),
    path('url_compare_competitor_ssl_status/<int:pk>/', views.url_compare_competitor_ssl_status, name="Compare keyword"),
    path('url_compare_competitor_run_time/<int:pk>/', views.url_compare_competitor_run_time, name="Compare keyword"),
    path('ob_br_compare_competitor/<int:pk>/', views.ob_br_compare_competitor, name="Compare keyword"),

    path('top_2_competitors/<int:pk>/', views.top_2_competitors, name="Competitors"),
    path('get_rank/<int:pk>/', views.get_keyword_rank, name="Ranking"),

    path('campaign/<int:pk>/', views.campaign_info_by_id, name='campaign-user-id'),
    path('campaign/', views.CampaignInfoView, name='campaign'),
    path('campaign_user/', views.CampaignInfoByUser, name='campaign'),

    path('keyword/<int:pk>/', views.Keyword_info_by_id, name='Keywords'),
    path('keyword/', views.KeywordsInfoView, name='Keywords'),
    path('keyword_campaign/', views.KeywordsInfoByCampaign, name='Keywords'),

    path('keyword_dash/', views.DashboardInfoView, name='Dashboard'),

    path('keyword_compare/', views.get_seo_data, name='compare'),

    path('subscribe/', views.SubscribersInfoView, name='subscribe'),
    path('subscribe/<int:pk>/', views.Subscriber_info_by_id, name='subscribe'),

    path('test/', views.test, name='test'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)