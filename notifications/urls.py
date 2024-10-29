from django.urls import include, path


urlpatterns = [
    path('api/v1/', include('notifications.api_urls'))
]
