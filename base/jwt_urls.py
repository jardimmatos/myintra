from django.urls import path
from rest_framework_simplejwt import views as drf_views
from . import views

urlpatterns = [
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', views.CustomRefreshTokenObtainPairView.as_view(), name='token_refresh'),
    path('token/refresh/', drf_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', views.CustomTokenVerifyView.as_view(), name='token_verify'),
    path('token/verify/', drf_views.TokenVerifyView.as_view(), name='token_verify'),
    path('auth-sso-admin/', views.auth_sso_admin, name='auth_sso_admin'),
]

