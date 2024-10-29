from django.views.generic import DetailView
from . import models
from . import serializers as app_serializers
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from base.permissions_mixins import PermsApi
from base.utils import register_gateway

class RepoView(DetailView):
    template_name = 'repositorio/page.html'
    model = models.Repo
    fields = '__all__'
    lookup_field = 'pk'


class RepoViewSet(viewsets.ModelViewSet):
    queryset = models.Repo.objects.all()
    serializer_class = app_serializers.RepoSerializer
    permission_classes = [ PermsApi ]

    def get_permissions(self):
        if self.action in ['user']:
            self.permission_classes = [ permissions.IsAuthenticated ]

        return super().get_permissions()

    @action(detail=True)
    def full(self, request, pk=None):
        obj = self.get_object()
        serializer = app_serializers.RepoFullSerializer(obj)
        return Response(serializer.data)
    
    @action(detail=False)
    def user(self, request):
        user = request.user
        repos_usuario = user.repo_set.all()
        result=[]
        for cat in models.Categoria.objects.filter(id__in=repos_usuario.values_list('categoria__id')):
            serial_cat = app_serializers.CategoriaFullSerializer(cat, many=False)
            categoria = serial_cat.data
            
            repos = repos_usuario.filter(categoria=cat)
            serial_repos = app_serializers.RepoFullSerializer(repos, many=True)
            categoria['repos'] = serial_repos.data
            result.append(categoria)
            
        return Response(result)

    def list(self, request):
        register_gateway(request, f"Carregando BI`s", 'Repositório BI')
        page = self.paginate_queryset(self.queryset)
        serializer = self.get_serializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = models.Categoria.objects.all()
    serializer_class = app_serializers.CategoriaSerializer
    permission_classes = [ PermsApi ]

    def get_permissions(self):
        if self.action in ['categorias_pais_filhos']:
            self.permission_classes = [ permissions.IsAuthenticated ]

        return super().get_permissions()

    @action(detail=True)
    def full(self, request, pk=None):
        obj = self.get_object()
        serializer = app_serializers.CategoriaFullSerializer(obj)
        return Response(serializer.data)

    @action(detail=False)
    def categorias_pais_filhos(self, request):
        self.serializer_class = app_serializers.CategoriaPaisFilhosSerializer
        serializer = self.get_serializer(self.queryset.all(), many=True, read_only=True)
        return Response(serializer.data)

    def list(self, request):
        page = self.paginate_queryset(self.queryset)
        serializer = self.get_serializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        result_set = serializer.data
        return Response(result_set)
