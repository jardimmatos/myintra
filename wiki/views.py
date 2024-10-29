from . import models
from django.db.models import Q
from . import serializers as app_serializers
from rest_framework import mixins, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import Group, Permission
from base.permissions_mixins import IsAdminUser, IsSuperUser, PermsApi
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Count

class CategoriaSistemaViewSet(viewsets.ModelViewSet):
    queryset = models.CategoriaSistema.objects.all()
    serializer_class = app_serializers.CategoriaSistemaSerializer
    permission_classes = [ permissions.IsAuthenticated ]
    
    def get_queryset(self):
        return self.queryset

    def list(self, request):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        result_set = serializer.data
        return Response(result_set)


class WikiViewSet(viewsets.ModelViewSet):
    queryset = models.Wiki.objects.all()
    serializer_class = app_serializers.WikiSerializer
    permission_classes = [ permissions.IsAuthenticated ]

    def get_queryset(self):
        return self.queryset

    #Adiconar  parametros de url na documentação swagger
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('categoria', openapi.IN_QUERY, description='ID da categoria', type=openapi.TYPE_STRING),
        openapi.Parameter('q', openapi.IN_QUERY, description='Filtrar palavra em títulos e corpo das documentações', type=openapi.TYPE_STRING),
    ])
    def list(self, request):
        qs = self.get_queryset()
        if not request.user.is_superuser:
            # docs que eu criei (privados ou não), inclusive Docs de outros setores (aos quais eu não pertenco)
            qs1 = qs.filter(created_by=request.user)

            # Docs vinculados a min
            qs2 = qs.filter(membros__in=[request.user], ativo=True)

            # Publicados e não vinculados a ninguém ( = todos )
            qs3 = qs.annotate(num_membros=Count('membros')).filter(num_membros__lte=0, ativo=True)

            qs = qs.filter(
                Q(id__in=qs1.values_list('id', flat=True)) |
                Q(id__in=qs2.values_list('id', flat=True)) |
                Q(id__in=qs3.values_list('id', flat=True))
            )
        query = request.query_params.get('q',None)
        if query:
            qs = qs.filter(Q(titulo__icontains=query) | Q(html__icontains=query))

        categoria = request.query_params.get('categoria', None)
        if categoria:
            qs = qs.filter(sistema__id=categoria)

        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        result_set = serializer.data
        return Response(result_set)
