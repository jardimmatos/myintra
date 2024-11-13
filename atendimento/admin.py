from django.contrib import admin
from . import models
from django.utils.html import format_html


class AbstractAtendimentoAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(models.Unidade)
class UnidadeAdmin(AbstractAtendimentoAdmin):
    search_fields = ('nome',)


@admin.register(models.Local)
class LocalAdmin(AbstractAtendimentoAdmin):
    autocomplete_fields = ('unidade',)
    search_fields = ('nome',)
    save_as = True


@admin.register(models.Prioridade)
class PrioridadeAdmin(AbstractAtendimentoAdmin):
    autocomplete_fields = ('unidade',)
    search_fields = ('nome',)
    save_as = True


@admin.register(models.Departamento)
class DepartamentoAdmin(AbstractAtendimentoAdmin):
    autocomplete_fields = ('unidade',)
    search_fields = ('nome',)
    save_as = True


@admin.register(models.Servico)
class ServicoAdmin(AbstractAtendimentoAdmin):
    list_select_related = ('unidade', 'departamento')
    list_display = ('id', 'unidade', 'nome', 'descricao', 'departamento',
                    'sigla', 'ativo')
    autocomplete_fields = ('unidade',)
    list_editable = ('nome', 'departamento', 'sigla', 'ativo')
    search_fields = ('nome',)
    save_as = True


@admin.register(models.Cliente)
class ClienteAdmin(AbstractAtendimentoAdmin):
    list_display = ('nome', 'matricula', 'email', 'celular')


@admin.register(models.Perfil)
class PerfilAdmin(AbstractAtendimentoAdmin):
    autocomplete_fields = ('unidade',)
    search_fields = ('nome',)
    save_as = True


@admin.register(models.Atendente)
class AtendenteAdmin(AbstractAtendimentoAdmin):
    list_select_related = ('unidade', 'usuario', 'perfil', 'local',
                           'prioridade')
    list_prefetch_related = ('servicos',)
    list_display = ('usuario', 'to_label_unidade', 'to_label_local',
                    'numero_local', 'to_label_perfil')
    autocomplete_fields = ('usuario', 'local', 'prioridade', 'perfil')
    filter_horizontal = ('servicos',)
    search_fields = ('usuario__username',)
    save_as = True
    ordering = ('usuario__first_name',)
    list_filter = ('ativo', )


@admin.register(models.Atendimento)
class AtendimentoAdmin(AbstractAtendimentoAdmin):
    list_select_related = ('unidade', 'cliente', 'prioridade', 'servico',
                           'local', 'atendente')
    list_per_page = 50
    list_display = (
        'id', 'unidade', 'status_atendimento', 'historico', 'cliente',
        'sigla_senha',
        'to_label_prioridade', 'to_label_servico', 'to_label_local',
        'atendente',
        'data_chegada', 'data_chamada', 'data_inicio', 'data_fim',
        'tempo_espera', 'tempo_deslocamento', 'tempo_atendimento',
        'tempo_permanencia'
        )
    readonly_fields = (
                    'unidade', 'servico_original', 'servico', 'cliente',
                    'prioridade', 'senha',
                    'atendente_tri', 'redirecionado_por', 'atendente', 'local',
                    'data_chegada',
                    'data_chamada', 'data_inicio', 'data_fim',
                    'tempo_espera', 'tempo_deslocamento', 'tempo_atendimento',
                    'tempo_permanencia',
                    'status_atendimento', 'sigla_senha', 'historico',
                    'avaliacao', 'comentarios',
                    'created_at', 'updated_at', 'created_by', 'updated_by',
                    )
    search_fields = ('sigla_senha', 'cliente__matricula', 'cliente__nome',
                     'atendente__usuario__username')

    # Incluir atendente, encarece as consultas de filtros
    list_filter = ('unidade', 'historico', 'prioridade', 'status_atendimento',
                   'servico',)
    date_hierarchy = 'data_chegada'

    def comentarios(self, obj):
        comentarios = "<br>".join([
            '<span>Em {}, {} observou: {}</span>'.format(
                u.get_created_at,
                u.created_by.first_name,
                u.comentario
            ) for u in obj.atendimentocomentario_set.all()])
        return format_html(comentarios)
    comentarios.short_description = 'Comentários deste atendimento'


@admin.register(models.PainelSenha)
class PainelSenhaAdmin(AbstractAtendimentoAdmin):
    list_display = ('id', 'ref_atendimento', 'sigla_senha', 'atendimento',
                    'created_at')
    # readonly_fields = ('created_at', 'updated_at', 'created_by',
    # 'updated_by')
