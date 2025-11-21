from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('sso-login/', views.sso_login, name='sso_login'),
    path('sso-callback/', views.sso_callback, name='sso_callback'),
    path('sync-user/', views.sync_user, name='sync_user'),
    path('validate-token/', views.validate_token, name='validate_token'),
]