from django.contrib import admin
from base.admin import AbstractAdmin
from repositoriobi import models
from django.utils.html import format_html

@admin.register(models.Categoria)
class CategoriaAdmin(AbstractAdmin):
    list_display = ('nome','descricao','pai','_itens')
    list_editable = ('pai','descricao')
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at','filhos',)

    def filhos(model, obj):
        filhos = "<br>".join([ f'<a href="/admin/repositoriobi/categoria/{u.id}/change/" target="_blank">{ u.nome } {u.id}</a>' for u in obj.categoria_set.all()])
        return format_html(filhos)


@admin.register(models.Repo)
class RepoAdmin(AbstractAdmin):
    list_display = ('descricao','categoria','_membros')
    readonly_fields = ('view_repo','created_by', 'updated_by', 'created_at', 'updated_at')
    filter_horizontal = ('membros',)
    search_fields = ('descricao',)
    list_filter= ('categoria','membros')
    list_editable = ('categoria',)

    def view_repo(self, obj):
        from django.utils.safestring import mark_safe
        if obj.link_bi:
            return mark_safe('''
            <iframe src="{0}" width="400px" height="300px" ></iframe>
            '''.format(obj.link_bi))