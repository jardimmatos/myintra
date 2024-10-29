from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('finalidades', views.FinalidadeViewSet, basename='finalidades')
router.register('tipo_espaco', views.TipoEspacoViewSet, basename='tipo_espaco')
router.register('espacos', views.EspacoViewSet, basename='espacos')
router.register('gestores', views.GestorViewSet, basename='gestores')
router.register('regras', views.RegraViewSet, basename='regras')
router.register('logs', views.LogAgendaViewSet, basename='logs')
router.register('reservas', views.ReservaViewSet, basename='reservas')

urlpatterns = router.urls
