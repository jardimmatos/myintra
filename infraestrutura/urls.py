from django.urls import include, path
app_name = 'infraestrutura'

urlpatterns = [
    path('api/v1/', include('infraestrutura.api_urls')),
]