from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('monitor', views.MonitorViewSet, basename='monitor')

urlpatterns = router.urls
