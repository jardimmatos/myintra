from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('local-uso', views.LocalUsoViewSet, basename='local-uso')
router.register('equipamentos', views.EquipamentoViewSet, basename='equipamentos')
router.register('status-dispositivos', views.StatusDispositivoViewSet, basename='status-dispositivos')
router.register('log-dispositivos', views.LogDispositivoViewSet, basename='log-dispositivos')
router.register('dispositivos', views.DispositivoViewSet, basename='dispositivos')
router.register('log-circulacao', views.LogCirculacaoViewSet, basename='log-circulacao')
router.register('circulacao', views.CirculacaoViewSet, basename='circulacao')
router.register('item-circulacao', views.ItemCirculacaoViewSet, basename='item-circulacao')

urlpatterns = router.urls
