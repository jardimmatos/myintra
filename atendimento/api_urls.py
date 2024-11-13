from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('atendimento', views.AtendimentoViewSet,
                basename='atendimento')

urlpatterns = router.urls
