from django.urls import include, path


urlpatterns = [
    path('api/v1/', include('wiki.api_urls'))
]
