from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('bi', views.RepoViewSet, basename='bi')
router.register('categoria', views.CategoriaViewSet, basename='categoria')

urlpatterns = router.urls
