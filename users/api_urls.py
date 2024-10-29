from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('users', views.UserViewSet, basename='users')
router.register('global', views.UserGlobalViewSet, basename='global')
router.register('groups', views.GroupViewSet, basename='groups')
router.register('permissions', views.PermissionViewSet, basename='permissions')

urlpatterns = router.urls
