from django.urls import include, path

from . import views
app_name = 'base'

urlpatterns = [
    
    path('', views.Index.as_view(), name="index"),

    path('base/api/v1/', include('base.api_urls')),
    path('auth/api/v1/', include('base.jwt_urls')),
]