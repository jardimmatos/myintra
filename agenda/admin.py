from django.contrib import admin
import datetime
from .enums import StatusReservaEnum
from . import models
from base.admin import AbstractAdmin 


@admin.register(models.Configuracao)
class ConfiguracaoAdmin(AbstractAdmin):
    search_fields = ('descricao',)


@admin.register(models.Finalidade)
class FinalidadeAdmin(AbstractAdmin):
    search_fields = ('descricao',)


@admin.register(models.TipoEspaco)
class TipoEspacoAdmin(AbstractAdmin):
    search_fields = ('descricao',)


@admin.register(models.Espaco)
class EspacoAdmin(AbstractAdmin):
    list_display = (
        'alias', 'descricao', 'tipo_espaco', 'permite_criar_sabados', 'permite_criar_domingos',
        'ativo', 'requer_aprovacao', 'count_admins'
    )
    search_fields = ('descricao',)
    list_editable = (
        'descricao', 'tipo_espaco','permite_criar_sabados', 'permite_criar_domingos',
        'ativo', 'requer_aprovacao'
    )
    filter_horizontal = ('regras','gestores', 'admins', 'teams')
    autocomplete_fields = ('tipo_espaco',)


@admin.register(models.Regra)
class RegraAdmin(AbstractAdmin):
    list_display = ('week_day', 'start_time', 'end_time')


@admin.register(models.Reserva)
class ReservaAdmin(AbstractAdmin):
    list_display = ('espaco', 'date', 'start', 'end', 'get_status_html', 'status_andamento', 'created_at')
    list_filter= ('espaco','status_reserva', 'finalidade', 'created_by')
    filter_horizontal=('arquivos',)
    autocomplete_fields = ('espaco','finalidade', )
    date_hierarchy= 'date'
    list_per_page = 50
    show_full_result_count = True
    actions = ['set_cancelled', 'set_opened']
    search_fields = ('titulo', 'responsavel')

    def get_queryset(self, request):
        #inscricoes serão exibidas no admin somente se inscrito estiver legal
        queryset = models.Reserva.objects.all().order_by('date', 'start')
        if request.user.is_superuser:
            return queryset.all()
        else:
            return queryset.filter(status_reserva=StatusReservaEnum.OPENED.name,
                        date__gte=datetime.datetime.now().date())
    
    def set_cancelled(modeladmin, request, queryset):
        for obj in queryset:
            if obj.status_reserva != StatusReservaEnum.CANCELLED.name:
                obj.status_reserva = StatusReservaEnum.CANCELLED.name
                obj.save()

    set_cancelled.short_description = "Cancelar Reserva"
    set_cancelled.allowed_permissions = ('change_reserva',)
    
    def set_opened(modeladmin, request, queryset):
        for obj in queryset:
            if obj.status_reserva != StatusReservaEnum.CANCELLED.name:
                obj.status_reserva = StatusReservaEnum.OPENED.name
                obj.save()

    set_opened.short_description = "Autorizar Reserva"
    set_opened.allowed_permissions = ('change_reserva',)
    
    def has_change_reserva_permission(self, request):
        return request.user.has_perm('agenda.change_reserva')


@admin.register(models.LogAgenda)
class LogAgendaAdmin(admin.ModelAdmin):
    list_display = ('log_app','log_type','log_action','log_at', 'log')
    list_filter = ('log_app','log_type','log_action')
    search_fields = ('log',)
