from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('wiki', views.WikiViewSet, basename='wiki')
router.register('categoria-sistema', views.CategoriaSistemaViewSet, basename='categoria-sistema')

urlpatterns = router.urls
