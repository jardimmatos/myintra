import urllib3
import requests
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from users.models import User
from rest_framework_simplejwt import views as drf_views
from .token_pair_serializers import MyTokenObtainPairSerializer
from . import serializers as app_serializers, models
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render, redirect
from rest_framework import viewsets, status, permissions
from base.utils import call_ws, register_gateway
from django.contrib import auth

class Index(TemplateView):
    def get(self, request, *args, **kwargs):
        """ Admin / redireciona para /admin/ """
        return HttpResponseRedirect('/admin/')


class CustomTokenObtainPairView(drf_views.TokenViewBase):
    serializer_class = MyTokenObtainPairSerializer


class MonitorViewSet(viewsets.ModelViewSet):
    """ carrega lista de serviços cadastrados """
    queryset = models.MonitorServico.objects.filter(ativo=True).order_by('referencia')
    serializer_class = app_serializers.MonitorServicoSerializer

    @action(detail=False)
    def monitors(self, request):

        serializer = self.get_serializer(self.get_queryset(), many=True)
        
        # canal para o id do usuário
        room = f'{"room_channel_monitor_"}{request.user.id}'

        for value in serializer.data:

            loading_msg = "Verificando "+value.get('url')+'...'
            call_ws(channel_name=room, tag='MONITOR-LOADING', msg=loading_msg)

            mensagem, online = self.checkServiceRequest(value.get('url')) 
            value['mensagem'] = mensagem
            value['online'] = online
        
        call_ws(channel_name=room, tag='MONITOR-LOADED', msg="Verificação concluída")

        return Response(serializer.data)
    
    def checkServiceRequest(self, url):
        urllib3.disable_warnings()
        online = False
        message = 'Servidor Offline'
        try:
            check = requests.get(url, timeout=5, verify=False)
            if check.status_code == 200:
                message = "Servidor Online"
                online = True
        except:
            message = 'Servidor demorou responder'
            online = False

        return message, online

    def list(self, request):
        page = self.paginate_queryset(self.queryset)
        serializer = self.get_serializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        result_set = serializer.data
        return Response(result_set)


def auth_sso_admin(request):
    if request.method == "GET":
        next = request.GET.get("next","/")
        token = request.GET.get("token", None)
        if not token:
            return redirect(next)
        
        if request.user.is_authenticated:
            return redirect(next)
        try:
            user = User.objects.get(token=token)
        except:
            # Se não encontrar usuário com o token especificado, redirecionar para o next(dependente de login)
            return redirect(next)
        auth.login(request, user)
        
        # Registrar log no gateway
        register_gateway(request, f"Registrando login SSO: {user}", 'SSO')
        
        return redirect(next)

