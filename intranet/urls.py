from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from base.permissions_mixins import IsSuperUser

schema_view = get_schema_view(
    openapi.Info(
        title="Intranet API",
        default_version='v1',
        description="Intranet Full Documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="jr.jardimmatos@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    # permission_classes=[permissions.IsAuthenticated],
    permission_classes=[IsSuperUser],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('user/', include('users.urls')),
    path('agendalabs/', include('agenda.urls')),
    path('notificacao/', include('notifications.urls')),
    path('wiki/', include('wiki.urls')),
    path('repositoriobi/', include('repositoriobi.urls')),
    path('infraestrutura/', include('infraestrutura.urls')),
    path('atendimento/', include('atendimento.urls')),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
]

# swagger
urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),  # noqa E501
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # noqa E501
    re_path(r'^developer/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # noqa E501
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
