from django.contrib import admin
from base.admin import AbstractAdmin
from . import models


@admin.register(models.CategoriaSistema)
class CategoriaSistemaAdmin(AbstractAdmin):
    list_display = ('id', 'nome',)


@admin.register(models.Wiki)
class WikiAdmin(AbstractAdmin):
    list_display = ('titulo', 'text', 'sistema', 'ativo')
    search_fields = ('titulo',)
    filter_horizontal = ('membros',)
    readonly_fields = ('text', 'html', 'created_at', 'updated_at',
                       'created_by', 'updated_by')
