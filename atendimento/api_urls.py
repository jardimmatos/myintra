from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('atendimento', views.AtendimentoViewSet, basename='atendimento')
# router.register('painel', views.MonitorViewSet, basename='painel')

urlpatterns = router.urls
