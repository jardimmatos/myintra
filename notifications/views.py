from . import models
from django.db.models import Q
from . import serializers as app_serializers
from rest_framework import mixins, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import Group, Permission
from base.permissions_mixins import IsAdminUser, IsSuperUser, PermsApi
import datetime
from base.utils import call_ws, register_gateway

class NotificacaoViewSet(viewsets.ModelViewSet):
    queryset = models.Notificacao.objects.all()
    serializer_class = app_serializers.NotificacaoSerializer
    permission_classes = [ permissions.IsAuthenticated ]
    
    def get_queryset(self):
        self.queryset = self.queryset.filter(
            # Notificações com data de inicio a partir de HOJE
            Q(inicio__lte=datetime.datetime.now()), 
            # Notificações com data de fim nulas ou até HOJE
            Q(
                Q(fim__isnull=True) | 
                Q(fim__gte=datetime.datetime.now())
            ))
        return self.queryset

    def list(self, request):
        register_gateway(request, f"Carregando Notificações da página Inicial", 'Notificações')
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        result_set = serializer.data
        return Response(result_set)
    
    def perform_destroy(self, instance):
        instance.delete()
        call_ws('room_channel_notifications','Notificação removida', 'NOTIFICATION-DELETED', notify=False)
