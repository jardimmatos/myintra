from django.contrib import admin, messages
from . import models
from base.admin import AbstractAdmin 
from datetime import datetime

@admin.register(models.LocalUso)
class LocalUsoAdmin(AbstractAdmin):
    search_fields = ('descricao',)


@admin.register(models.Equipamento)
class EquipamentoAdmin(AbstractAdmin):
    search_fields = ('descricao',)


@admin.register(models.Dispositivo)
class DispositivoAdmin(AbstractAdmin):
    list_display = ('id','identificador','equipamento', 'situacao','obs')
    search_fields = ('identificador','equipamento__descricao', 'obs')
    autocomplete_fields = ('equipamento',)
    list_filter = ('equipamento', 'situacao')


@admin.register(models.LogDispositivo)
class LogDispositivoAdmin(AbstractAdmin):
    list_display = ('dispositivo','local','responsavel','situacao','obs','created_at','created_by', 'circulacao_id')
    list_filter = ('dispositivo__equipamento','dispositivo','situacao')
    search_fields = ('dispositivo__identificador','dispositivo__equipamento__descricao')


@admin.register(models.ItemCirculacao)
class ItemCirculacaoAdmin(AbstractAdmin):
    list_display = ('id','dispositivo','circulacao','situacao','circulacao_id')
    list_filter = ('situacao',)
    actions = ('receber','estornar','cancelar', 'avaria', 'extravio')

    def estornar(modeladmin, request, queryset):
        for obj in queryset:
            try:
                obj.set_item_circulacao_estornar('Item Estornado via admin', request.user)
            except Exception as ex:
                messages.add_message(request, messages.ERROR, str(ex))
    estornar.short_description = "Estornar"

    def receber(modeladmin, request, queryset):
        for obj in queryset:
            try:
                obj.set_item_circulacao_receber('Item Baixado via admin', request.user, datetime.now())
            except Exception as ex:
                messages.add_message(request, messages.ERROR, str(ex))
    receber.short_description = "Receber"

    def cancelar(modeladmin, request, queryset):
        for obj in queryset:
            try:
                obj.set_item_circulacao_cancelar('Item Cancelado e registrado via admin', request.user)
            except Exception as ex:
                messages.add_message(request, messages.ERROR, str(ex))
    cancelar.short_description = "Cancelar"

    def avaria(modeladmin, request, queryset):
        for obj in queryset:
            try:
                obj.set_item_circulacao_avaria('Item Avariado e registrada via admin', request.user, datetime.now())
            except Exception as ex:
                messages.add_message(request, messages.ERROR, str(ex))
    avaria.short_description = "Avaria"

    def extravio(modeladmin, request, queryset):
        for obj in queryset:
            try:
                obj.set_item_circulacao_extravio('Item Extraviado e registrado via admin', request.user, datetime.now())
            except Exception as ex:
                messages.add_message(request, messages.ERROR, str(ex))
    extravio.short_description = "Extravio"


@admin.register(models.Circulacao)
class CirculacaoAdmin(AbstractAdmin):
    list_display = ('id','count_itens','local','responsavel', 'email', 'previsao_devolucao', 'data_baixa','situacao','created_by','obs','created_at')
    list_filter = ('situacao', 'responsavel')
    autocomplete_fields = ('local','baixado_por')
    actions = ('baixar','cancelar')

    def baixar(modeladmin, request, queryset):
        for obj in queryset:
            try:
                obj.set_circulacao_baixar('Baixado via admin', request.user, datetime.now())
            except Exception as ex:
                messages.add_message(request, messages.ERROR, str(ex))
    baixar.short_description = "Baixar Circulação (Receber tudo)"

    def cancelar(modeladmin, request, queryset):
        for obj in queryset:
            try:
                obj.set_circulacao_cancelar('Cancelado via admin', request.user)
            except Exception as ex:
                messages.add_message(request, messages.ERROR, str(ex))
    cancelar.short_description = "Cancelar Circulação"

    

@admin.register(models.LogCirculacao)
class LogCirculacaoAdmin(AbstractAdmin):
    list_display = ('circulacao_id','circulacao', 'situacao', 'obs', 'created_at')


@admin.register(models.StatusDispositivo)
class StatusDispositivoAdmin(AbstractAdmin):
    list_display = ('id','descricao', 'color', 'permite_circular', 'created_at')


