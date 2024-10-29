from django.urls import include, path

app_name = 'agenda'

urlpatterns = [
    path('api/v1/', include('agenda.api_urls')),
]


