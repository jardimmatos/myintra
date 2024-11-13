from django.contrib import admin
from . import models
from import_export import (admin as import_export_admin,
                           fields as import_export_fields, resources)
from django.contrib.admin.models import LogEntry

admin.site.site_header = 'My Intranet'
admin.site.index_title = 'Configurações'
admin.site.site_title = 'Gestão do Sistema'
admin.site.login_template = 'admin/login.html'


class AbstractAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    show_full_result_count = True
    list_per_page = 50
    save_as = True

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(models.TeamsChannel)
class TeamsChannels(AbstractAdmin):
    list_display = ('titulo', 'webhook', 'ativo')


class ResourceMonitorServicos(resources.ModelResource):
    servico = import_export_fields.Field(attribute='servico',
                                         column_name='Serviço')
    url = import_export_fields.Field(attribute='url',
                                     column_name='URL')
    referencia = import_export_fields.Field(attribute='referencia',
                                            column_name='Referência')
    ativo = import_export_fields.Field(attribute='ativo',
                                       column_name='Ativo')

    class Meta:
        model = models.MonitorServico
        export_order = ('servico', 'url', 'referencia', 'ativo')
        fields = ('id', 'servico', 'url', 'referencia', 'ativo')


@admin.register(models.MonitorServico)
class MonitorServicoAdmin(import_export_admin.ImportExportModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')
    list_display = ('servico', 'url', 'referencia', 'ativo')
    resource_class = ResourceMonitorServicos
    show_full_result_count = True
    list_per_page = 50
    save_as = True


@admin.register(models.GlobalSetting)
class GlobalSettingAdmin(AbstractAdmin):
    list_display = ('description', )
    readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')
    fieldsets = (
        ('Configurações Globais', {
            'fields': (
                ('description', ),
            ),
        }),
        ('Registro de dado', {
            'fields': (
                ('created_by', 'created_at'),
                ('updated_by', 'updated_at')
            ),
        }),
    )


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_repr',
                    'action_flag', 'change_message', 'tipo')
    list_filter = ('action_time', 'content_type', 'user')
    search_fields = ('object_repr', 'change_message')
    date_hierarchy = 'action_time'
    readonly_fields = ('user', 'content_type', 'object_id', 'object_repr',
                       'action_flag', 'change_message', 'action_time', 'tipo')

    actions = None
    limit = 100  # altera a quantidade de logs recentes exibidos
    search_fields = ('object_repr',)

    def tipo(self, obj):
        if obj.is_addition():
            return u"Adicionado"
        elif obj.is_change():
            return u"Modificado"
        elif obj.is_deletion():
            return u"Deletado"


@admin.register(models.LogSistema)
class LogSistemaAdmin(admin.ModelAdmin):
    list_display = ('path', 'log', 'created_at')
    list_filter = ('path',)


@admin.register(models.SystemParams)
class SysteParamAdmin(admin.ModelAdmin):
    list_display = ('chave', 'valor')
    readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')
    list_display = ('chave', 'valor')
    save_as = True


admin.site.register(LogEntry, LogEntryAdmin)
