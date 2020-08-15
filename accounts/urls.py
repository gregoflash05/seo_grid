from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings

urlpatterns = [
    path('signup/', views.register, name = "signup"),
    path('', views.homepage, name = "homepage"),
    path('login/', views.login, name = "login"),
    path('logout/', views.logout, name="logout"),
    # path('dashboard/', views.dashboard, name="logout"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name="password_reset_done"),
    path('reset_form/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/reset_form.html"), name="password_reset_confirm"),
    path('reset_password_completed/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_completed.html"), name="password_reset_complete"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)