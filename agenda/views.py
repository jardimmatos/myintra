from datetime import datetime, timedelta
from base.enums import ActionEnum, AppEnum, LogTypeEnum
from .enums import StatusReservaEnum
from django.db.models import Q
from django.db.models import ProtectedError
from django.utils.translation import gettext as _
from . import models
from . import serializers as app_serializers
from rest_framework import viewsets, status, serializers as drf_serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from users.serializers import UserSimpleSerializer
from .tasks import agenda_registra_log, agenda_notificar_email
from .mail_templates import template_aprovacao_reserva, template_cancelamento_reserva
from base.teams import TeamsTemplates
from base.tasks import task_send_teams_channel
from base.utils import call_ws, register_gateway


class FinalidadeViewSet(viewsets.ModelViewSet):
    """ Viewset para Finalidades de Reserva """
    queryset = models.Finalidade.objects.all()
    serializer_class = app_serializers.FinalidadeSerializer
    
    def list(self, request):
        """ Rota padrão para listagem de objetos Finalidade"""
        page = self.paginate_queryset(self.queryset)
        serializer = self.get_serializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        result_set = serializer.data
        return Response(result_set)


class TipoEspacoViewSet(viewsets.ModelViewSet):
    """ Viewset para os Tipos de Espaços """
    queryset = models.TipoEspaco.objects.all()
    serializer_class = app_serializers.TipoEspacoSerializer
    
    def list(self, request):
        """ Rota padrão para listagem de objetos Tipos de Espaços"""
        page = self.paginate_queryset(self.queryset)
        serializer = self.get_serializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        result_set = serializer.data
        return Response(result_set)
    
    def perform_destroy(self, instance):
        """ Rota padrão para exclusão de Tipos de Espaços"""
        try:
            instance.delete()
        except ProtectedError:
            raise drf_serializers.ValidationError(
                _('Este tipo de Espaço não pode ser removido, há salas relacionadas')
            )


class EspacoViewSet(viewsets.ModelViewSet):
    """ Viewset para os Espaços """
    queryset = models.Espaco.objects.all()
    serializer_class = app_serializers.EspacoSerializer
    
    def list(self, request):
        """ Rota padrão para listagem de objetos Espaços"""
        self.queryset = self.queryset.all()
        page = self.paginate_queryset(self.queryset)
        serializer = self.get_serializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        result_set = serializer.data
        return Response(result_set)
    
    def perform_destroy(self, instance):
        """ Rota padrão para exclusão de Tipos de Espaços"""
        try:
            instance.delete()
        except ProtectedError:
            raise drf_serializers.ValidationError(_('Este Espaço não pode ser removido, há reservas relacionadas'))


class GestorViewSet(viewsets.ModelViewSet):
    """ Viewset para os Gestores de Espaços """
    queryset = models.User.objects.all()
    serializer_class = UserSimpleSerializer
    
    def list(self, request):
        """ Rota padrão para listagem de objetos Gestor"""
        search = request.query_params.get('q', None)

        if search:
            # pesquisar pela parte de username, pelo e-mail ou pelo primeiro nome    
            self.queryset = self.queryset.filter(
                Q(username__icontains=search) | 
                Q(email__icontains=search) | 
                Q(first_name__icontains=search)
            )
        page = self.paginate_queryset(self.queryset)
        serializer = self.get_serializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        result_set = serializer.data
        return Response(result_set)


class RegraViewSet(viewsets.ModelViewSet):
    """ Viewset para as restrições no Espaço/Reserva """
    queryset = models.Regra.objects.all()
    serializer_class = app_serializers.RegraSerializer

    @action(detail=False, methods=['get'])
    def weekdays(self, request, pk=None):
        """ Listagem de dias da semana """
        regra = models.Regra()
        serializer = app_serializers.RegraWeekdayEnumSerializer(regra)
        return Response(serializer.data)
    
    def list(self, request):
        """ Listagem padrão de Regras """
        page = self.paginate_queryset(self.queryset)
        serializer = self.get_serializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        result_set = serializer.data
        return Response(result_set)
    
    def perform_destroy(self, instance):
        """ Listagem padrão de exclusão """
        count = instance.espaco_set.count()
        if count > 0:
            raise drf_serializers.ValidationError(_('Não é possível remover esta restrição, ainda há espaços utilizando-a!'))
        else:
            try:
                instance.delete()
            except ProtectedError:
                raise drf_serializers.ValidationError(_('Há espaços relacionados'))


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = models.Reserva.objects.all().order_by('start')
    serializer_class = app_serializers.ReservaSerializer
    page_size = 20
    
    @action(detail=True)
    def details(self, request, pk=None):
        """ Método para carregar os detalhes de uma reserva """
        obj = self.get_object()
        register_gateway(request, f"Obtendo detalhes de reserva no AgendaLabs: {str(obj.__dict__)}", 'AgendaLabs')
        serializer = app_serializers.ReservaDetalheSerializer(obj)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def set_opened(self, request, pk=None):
        """ Método para definir status como OPENED """
        obj = self.get_object()
        if request.user.has_perms(['agenda.can_aprovar_reserva']) or \
            obj.created_by in obj.espaco.admins.all():
            # libera Aprovação para usuários com permissão de aprovação
            # e usuários que fazem parte do grupo de admins de um espaco
            pass
        else:
            raise drf_serializers.ValidationError(f'Usuário não tem permissão para aprovar reservas!')

        if obj.status_reserva == StatusReservaEnum.PENDING.name:
            obj.status_reserva = StatusReservaEnum.OPENED.name
            obj.save()
            
            by = self.request.user
            # print('register log UPDATE VIEW')
            log = '{0} aprovou uma reserva para {1} no espaço {2} do dia {3}'.format(
                    by.get_full_name(),
                    obj.responsavel,
                    obj.espaco.descricao,
                    obj.date_start_end
                )
            msg = '{0} aprovou uma reserva para o espaço {1} do dia {2}'.format(
                    by.get_full_name(),
                    obj.espaco.descricao,
                    obj.date_start_end
                )
            register_gateway(request, msg, 'AgendaLabs')
            call_ws('room_channel_reservas', msg, 'RESERVA-APPROVED', notify=True)
            agenda_registra_log.delay({
                'log':          log, 
                'log_action':   ActionEnum.UPDATE.name, 
                'log_at':       f'{datetime.now()}', 
                'log_type':     LogTypeEnum.VIEW.name,
                'log_app':      AppEnum.AGENDALABS.name,
                'log_model':    'Reserva', 
                'log_reserva':  obj.id.hex
            })

            # TASK NOTIFICAÇÃO - TEAMS
            channels = obj.espaco.teams.filter(ativo=True)
            for channel in channels:
                options = {
                    'template': TeamsTemplates.TEMPLATE_FACTS, 
                    'channel': channel.webhook, 
                    'color': obj.status_color_hexadecimal.replace('#', ''), 
                    'title': 'Reserva APROVADA', 
                    'subtitle': obj.titulo, 
                    'messages': [
                        [ 'Espaço', obj.espaco.__str__()], 
                        [f'Responsável', obj.responsavel],
                        ['Data/hora', obj.date_start_end],
                        ['Finalidade', obj.finalidade.descricao],
                        ['Situação', obj.get_status()],
                        ['Observações', obj.observacao],
                        ['Detalhe', log],
                        ['Identificador', obj.id.hex],
                    ]
                }
                
                task_send_teams_channel.delay(options)

            if obj.espaco.enviar_notificacao:
                params = template_aprovacao_reserva(obj)
                agenda_notificar_email.delay(params)

        elif obj.status_reserva == StatusReservaEnum.CANCELLED.name:
            raise drf_serializers.ValidationError(
                f'Status atual da reserva é: {StatusReservaEnum.CANCELLED.value}!')
        elif obj.status_reserva == StatusReservaEnum.OPENED.name:
            raise drf_serializers.ValidationError(
                f'Status da reserva já é {StatusReservaEnum.OPENED.value}!')
        else:
            raise drf_serializers.ValidationError(
                _('Status da reserva não é pendente!'))
        serializer = app_serializers.ReservaSerializer(obj)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def set_cancelled(self, request, pk=None):
        """ Método para definir um status como cancelado"""
        obj = self.get_object()
        if request.user.has_perms(['agenda.can_cancelar_reserva']) or \
            obj.created_by in obj.espaco.admins.all() or \
            obj.created_by == request.user:
            # Usuário pode cancelar se tiver permissão, 
            # usuário sendo o próprio requerente da reserva 
            # usuário que faz parte do grupo de admins do espaço
            pass
        else:
            raise drf_serializers.ValidationError(
                f'Usuário não tem permissão para cancelar reservas!')

        if obj.status_reserva in [StatusReservaEnum.PENDING.name, StatusReservaEnum.OPENED.name ]:
            obj.status_reserva = StatusReservaEnum.CANCELLED.name
            obj.status_descricao = request.data.get('status_descricao', None)
            obj.save()

            by = self.request.user
            log = '{0} cancelou uma reserva para {1} no espaço {2} do dia {3}'.format(
                    by.get_full_name(),
                    obj.responsavel,
                    obj.espaco.descricao,
                    obj.date_start_end
                )
            msg = '{0} cancelou uma reserva para o espaço {1} do dia {2}'.format(
                    by.get_full_name(),
                    obj.espaco.descricao,
                    obj.date_start_end
                )
            register_gateway(request, msg, 'AgendaLabs')
            call_ws('room_channel_reservas', msg, 'RESERVA-CANCELLED', notify=True)
            agenda_registra_log.delay({
                'log':          log, 
                'log_action':   ActionEnum.UPDATE.name, 
                'log_at':       f'{datetime.now()}', 
                'log_type':     LogTypeEnum.VIEW.name,
                'log_app':      AppEnum.AGENDALABS.name,
                'log_model':    'Reserva', 
                'log_reserva':  obj.id.hex
            })

            if obj.espaco.enviar_notificacao:
                params = template_cancelamento_reserva(obj)
                agenda_notificar_email.delay(params)
            
            # TASK NOTIFICAÇÃO - TEAMS
            channels = obj.espaco.teams.filter(ativo=True)
            for channel in channels:
                options = {
                    'template': TeamsTemplates.TEMPLATE_FACTS, 
                    'channel': channel.webhook, 
                    'color': obj.status_color_hexadecimal.replace('#', ''), 
                    'title': 'Reserva CANCELADA', 
                    'subtitle': obj.titulo, 
                    'messages': [
                        [ 'Espaço', obj.espaco.__str__()], 
                        [f'Responsável', obj.responsavel],
                        ['Data/hora', obj.date_start_end],
                        ['Finalidade', obj.finalidade.descricao],
                        ['Situação', obj.get_status()],
                        ['Motivo', obj.status_descricao ],
                        ['Observações', obj.observacao],
                        ['Detalhe', log],
                        ['Identificador', obj.id.hex],
                    ]
                }
                task_send_teams_channel.delay(options)

        elif obj.status_reserva == StatusReservaEnum.CANCELLED.name:
            raise drf_serializers.ValidationError(
                f'Status atual da reserva já é: {StatusReservaEnum.CANCELLED.value}!')
        else:
            raise drf_serializers.ValidationError(
                f'Status da reserva não é pendente ({StatusReservaEnum[obj.status_reserva].value})!')

        serializer = app_serializers.ReservaSerializer(obj)
        return Response(serializer.data)

    def list(self, request):
        """ Método padrão para listagem de configs """
        config = models.Configuracao.objects.first()
        retroativos = 0
        if config:
            if config.dias_retroativos:
                retroativos = config.dias_retroativos
        
        # Parametrizando exibição de dias anteriores dias
        self.queryset = self.queryset \
            .exclude(date__lt=datetime.now() - timedelta(days=retroativos)) \
            .order_by('date')

        # parametro para filtro de status
        status_reserva = request.query_params.getlist('status_reserva[]', [])
        if status_reserva:
            self.queryset = self.queryset.filter(status_reserva__in=status_reserva)

        # parametro para filtro de data inicio
        date_start = request.query_params.get('date_start', None)
        if date_start:
            self.queryset = self.queryset.filter(date__gte=date_start)

        # parametro para filtro de data fim
        date_end = request.query_params.get('date_end', None)
        if date_end:
            self.queryset = self.queryset.filter(date__lte=date_end)

        # parametro para filtro de espaço (para componente de tela de relatórios no front)
        espaco_id = request.query_params.getlist('espaco_id[]', [])
        if espaco_id:
            self.queryset = self.queryset.filter(espaco__id__in=espaco_id)
        
        page = self.paginate_queryset(self.queryset)
        serializer = self.get_serializer(page, many=True)

        if page is not None:
            return self.get_paginated_response(serializer.data)
        result_set = serializer.data

        return Response(result_set)


class LogAgendaViewSet(viewsets.ModelViewSet):
    queryset = models.LogAgenda.objects.filter(log_type=LogTypeEnum.VIEW.name).order_by('-log_at')
    serializer_class = app_serializers.LogAgendaSerializer
    page_size = 20
    
    def list(self, request):
        """ Método para listagem de Logs """
        page = self.paginate_queryset(self.queryset)
        serializer = self.get_serializer(page, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        result_set = serializer.data
        return Response(result_set)
