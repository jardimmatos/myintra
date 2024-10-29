from django.urls import include, path

from . import views
app_name = 'atendimento'

urlpatterns = [
    path('api/v1/', include('atendimento.api_urls')),
    path('acompanhamento/<int:pk>/<str:senha>/', views.Acompanhamento.as_view(), name="acompanhamento"),
    path('painel/', views.Painel.as_view(), name="painel"),
    # path('acompanhamento/<int:id>/<str:senha>/',views.atendimento_acompanhamento,name='detail'),
]