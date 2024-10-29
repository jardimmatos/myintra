from rest_framework import viewsets, serializers as drf_serializers
from . import models, serializers as app_serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from . import enums
from datetime import datetime, timedelta


class LogDispositivoViewSet(viewsets.ModelViewSet):
    queryset = models.LogDispositivo.objects.all()
    serializer_class = app_serializers.LogDispositivoSerializer
    http_method_names = ['get', 'delete']

    def list(self, request):
        dispositivo_id = request.query_params.get('dispositivo', None)

        if (dispositivo_id):
            self.queryset = self.queryset.filter(dispositivo__id=dispositivo_id)
        page = self.paginate_queryset(self.queryset)
        serializer = self.get_serializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        result_set = serializer.data
        return Response(result_set)

    @action(detail=False, methods=['delete'])
    def delete_logs(self, request):
        dispositivo = request.query_params.get('dispositivo', None)
        if not dispositivo:
            raise drf_serializers.ValidationError({'dispositivo': 'Nenhum dispositivo informado para a remoção de logs'})
        
        self.queryset = self.queryset.filter(dispositivo__id=dispositivo).delete()
        return Response()

    
class LogCirculacaoViewSet(viewsets.ModelViewSet):
    queryset = models.LogCirculacao.objects.all()
    serializer_class = app_serializers.LogCirculacaoSerializer
    http_method_names = ['get','delete']

    def list(self, request):
        circulacao_id = request.query_params.get('circulacao', None)

        if (circulacao_id):
            self.queryset = self.queryset.filter(circulacao__id=circulacao_id)
        page = self.paginate_queryset(self.queryset)
        serializer = self.get_serializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        result_set = serializer.data
        return Response(result_set)
    
    
    @action(detail=False, methods=['delete'])
    def delete_logs(self, request):
        circulacao = request.query_params.get('circulacao', None)
        if not circulacao:
            raise drf_serializers.ValidationError({'circulacao': 'Nenhuma circulação informada para a remoção de logs'})
        
        self.queryset = self.queryset.filter(circulacao__id=circulacao).delete()
        return Response()


class LocalUsoViewSet(viewsets.ModelViewSet):
    queryset = models.LocalUso.objects.all()
    serializer_class = app_serializers.LocalUsoSerializer
    http_method_names = ['get', 'post', 'patch']


class EquipamentoViewSet(viewsets.ModelViewSet):
    queryset = models.Equipamento.objects.all()
    serializer_class = app_serializers.EquipamentoSerializer
    http_method_names = ['get', 'post', 'patch']


class StatusDispositivoViewSet(viewsets.ModelViewSet):
    queryset = models.StatusDispositivo.objects.all()
    serializer_class = app_serializers.StatusDispositivoSerializer
    http_method_names = ['get', 'post', 'patch']


class DispositivoViewSet(viewsets.ModelViewSet):
    queryset = models.Dispositivo.objects.all()
    serializer_class = app_serializers.DispositivoSerializer
    http_method_names = ['get', 'post', 'patch']

    @action(detail=True, methods=['post'])
    def set_manutencao(self, request, pk=None):
        obs = request.data.get('obs', '')
        obj = self.get_object()
        try:
            obj.set_dispositivo_manutencao(obs, request.user)
        except Exception as ex:
            print(ex)
            raise drf_serializers.ValidationError(ex.message_dict)
        
        serializer = self.get_serializer(obj, many=False)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def set_extravio(self, request, pk=None):
        obs = request.data.get('obs', '')
        obj = self.get_object()
        try:
            obj.set_dispositivo_extravio(obs, request.user)
        except Exception as ex:
            raise drf_serializers.ValidationError(ex.message_dict)
        serializer = self.get_serializer(obj, many=False)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def set_disponivel(self, request, pk=None):
        obs = request.data.get('obs', '')
        obj = self.get_object()
        try:
            obj.set_dispositivo_disponivel(obs, request.user)
        except Exception as ex:
            raise drf_serializers.ValidationError(ex.message_dict)
        serializer = self.get_serializer(obj, many=False)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def set_circulacao(self, request, pk=None):
        obs = request.data.get('obs', '')
        obj = self.get_object()
        try:
            obj.set_dispositivo_circulacao(obs, request.user)
        except Exception as ex:
            raise drf_serializers.ValidationError(ex.message_dict)
        serializer = self.get_serializer(obj, many=False)
        return Response(serializer.data)
        
    @action(detail=True, methods=['post'])
    def set_avaria(self, request, pk=None):
        obs = request.data.get('obs', '')
        obj = self.get_object()
        try:
            obj.set_dispositivo_avaria(obs, request.user)
        except Exception as ex:
            raise drf_serializers.ValidationError(ex.message_dict)
        serializer = self.get_serializer(obj, many=False)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_enum_situacao(self, request):
        enums_situacao = [ e.alias for e in enums.StatusDispositivo ]
        return Response(enums_situacao)


class ItemCirculacaoViewSet(viewsets.ModelViewSet):
    queryset = models.ItemCirculacao.objects.all()
    serializer_class = app_serializers.ItemCirculacaoSerializer
    http_method_names = ['get', 'post', 'patch']

    def perform_create(self, serializer):
        with transaction.atomic():
            options = serializer.validated_data
            options['created_by'] = self.request.user
            try:
                # Verifica se existe a circulacao ABERTO, para poder incluir um item
                models.Circulacao.objects.get(situacao=enums.StatusCirculacao.ABERTO.name, id=serializer.data.get('circulacao'))
            except models.Circulacao.DoesNotExist as ne:
                raise drf_serializers.ValidationError({'circulacao': 'Circulação não está aberta para inclusão de mais itens!'})
            try:
                models.ItemCirculacao.create(**options)
            except Exception as ex:
                raise drf_serializers.ValidationError(ex.message_dict)
    
    @action(detail=False, methods=['post'])
    def set_receber(self, request,):
        """ Requer parâmetros ```obs, usuario, devolvido_em``` """
        ids = request.data.get('ids', [])
        obs = request.data.get('obs', '')
        devolvido_em = request.data.get('devolvido_em', None)
        qs = self.queryset.filter(id__in=ids)
        for obj in qs:
            try:
                obj.set_item_circulacao_receber(obs, request.user, devolvido_em)
            except Exception as ex:
                raise drf_serializers.ValidationError(ex.message_dict)
            # if 'error_dict' in ex:
            #     raise drf_serializers.ValidationError(ex.message_dict)
            # raise drf_serializers.ValidationError(ex.message)
            
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def set_estornar(self, request):
        """ Requer parâmetros ```obs, usuario``` """
        ids = request.data.get('ids', [])
        obs = request.data.get('obs', 'Item estornado para circulacao')
        qs = self.queryset.filter(id__in=ids)
        for obj in qs:
            try:
                obj.set_item_circulacao_estornar(obs, request.user)
            except Exception as ex:
                raise drf_serializers.ValidationError(ex.message_dict)
        
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def set_cancelar(self, request):
        """ Requer parâmetros ```obs, usuario``` """
        obs = request.data.get('obs', '')
        ids = request.data.get('ids', [])
        # obj = self.get_object()
        qs = self.queryset.filter(id__in=ids)
        for obj in qs:
            try:
                obj.set_item_circulacao_cancelar(obs, request.user)
            except Exception as ex:
                raise drf_serializers.ValidationError(ex.message_dict)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def set_avaria(self, request):
        """ Requer parâmetros ```obs, usuario, devolvido_em``` """
        obs = request.data.get('obs', '')
        ids = request.data.get('ids', [])
        devolvido_em = request.data.get('devolvido_em', None)

        qs = self.queryset.filter(id__in=ids)
        for obj in qs:
            try:
                obj.set_item_circulacao_avaria(obs, request.user, devolvido_em)
            except Exception as ex:
                raise drf_serializers.ValidationError(ex.message_dict)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def set_extravio(self, request):
        """ Requer parâmetros ```obs, usuario, devolvido_em``` """
        ids = request.data.get('ids', [])
        qs = self.queryset.filter(id__in=ids)
        obs = request.data.get('obs', '')
        devolvido_em = request.data.get('devolvido_em', None)
        for obj in qs:
            try:
                obj.set_item_circulacao_extravio(obs, request.user, devolvido_em)
            except Exception as ex:
                raise drf_serializers.ValidationError(ex.message_dict)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def get_enum_situacao(self, request):
        enums_situacao = [ e.alias for e in enums.StatusItemCirculacao ]
        return Response(enums_situacao)


class CirculacaoViewSet(viewsets.ModelViewSet):
    queryset = models.Circulacao.objects.all()
    serializer_class = app_serializers.CirculacaoSerializer
    http_method_names = ['get', 'post', 'patch']

    def list(self, request):
        local = request.query_params.getlist('local[]')
        situacao = request.query_params.getlist('situacao[]')
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        # Filtrar locais
        if len(local):
            self.queryset = self.queryset.filter(local__in=local)

        # Filtrar por situacao
        if len(situacao):
            self.queryset = self.queryset.filter(situacao__in=situacao)
        # Filtrar ultimos 15 dias
        if data_inicio or data_fim:
            if data_inicio:
                dt = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                self.queryset = self.queryset.filter(created_at__date__gte=dt)

            if data_fim:
                dt = datetime.strptime(data_fim, '%Y-%m-%d').date()
                self.queryset = self.queryset.filter(created_at__date__lte=dt)
        else:
            # Se não houver nem data inico e nem fim, então limitar a 7 dias
            now = datetime.today() - timedelta(days=7)
            self.queryset = self.queryset.filter(created_at__date__gte=now)

        serializer = app_serializers.CirculacaoSimpleSerializer(self.queryset, many=True)
        # ao utilizar o serializer abaixo, remover o .map() no js no store GetRecursosCirculacao
        # serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        options = serializer.validated_data
        options['created_by'] = self.request.user
        # incluído no options pois a key "itens_dispositivos" não faz parte de uma prop da classe Circulacao, portanto, 
        # a inclusão manual em options para a lógica de criacao e relacionamento dos itens
        options['itens_dispositivos'] = self.request.data.get('itens_dispositivos', [])
        try:
            models.Circulacao.create(**options)
        except Exception as ex:
            print(ex)
            raise drf_serializers.ValidationError(ex.message_dict)

    @action(detail=True, methods=['post'])
    def set_cancelar(self, request, pk=None):
        """ parâmetros da view, motivo_cancelamento, baixado_por """
        motivo = request.data.get('motivo_cancelamento', '')
        baixado_por = self.request.user
        obj = self.get_object()
        obj.updated_by = baixado_por
        try:
            # TODO: Adicionar na models validação de que só pode realizar cancelamento se todos os itens estiverem como EM_CIRCULACAO, 
            # ou seja, sem que qualquer outra baixa tenha sido realizada
            obj.set_circulacao_cancelar(motivo, baixado_por)
        except Exception as ex:
            raise drf_serializers.ValidationError(ex.message_dict)
        serializer = self.get_serializer(obj, many=False)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def set_receber(self, request, pk=None):
        """ parâmetros da view, obs, data_baixa """
        obs = request.data.get('obs', '')
        devolvido_em = request.data.get('data_baixa', None)
        baixado_por = self.request.user
        obj = self.get_object()
        obj.updated_by = baixado_por
        try:
            obj.set_circulacao_baixar(obs, baixado_por, devolvido_em)
        except Exception as ex:
            print(ex)
            raise drf_serializers.ValidationError(ex.message_dict)
        serializer = self.get_serializer(obj, many=False)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def set_transferir(self, request, pk=None):
        """ parâmetros da view, responsavel, email, previsao_devolucao, transferidor, local """
        responsavel = request.data.get('responsavel', None)
        local = request.data.get('local', None)
        email = request.data.get('email', None)
        previsao_devolucao = request.data.get('previsao_devolucao', '')
        transferidor = self.request.user
        obj = self.get_object()
        obj.updated_by = transferidor
        try:
            obj.set_circulacao_transferir(responsavel, email, previsao_devolucao, transferidor, local)
        except Exception as ex:
            raise drf_serializers.ValidationError(ex.message_dict)
        serializer = self.get_serializer(obj, many=False)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_enum_situacao(self, request):
        enums_situacao = [ e.alias for e in enums.StatusCirculacao ]
        return Response(enums_situacao)

    @action(detail=False, methods=["get"])
    def pesquisar_pessoas(self, request):
        """ comumente utilizado em infraestrutura Circulacao (responsáveis) """
        # implementar usuário ou integrações externas
        pessoa = {}
        return Response(pessoa, status=404)
