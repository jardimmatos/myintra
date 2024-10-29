from cofre.models import Cofre, Setor, Tipo
from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from datetime import datetime
from base.utils import criptografar, descriptografar
from django import forms


@admin.register(Tipo)
class TipoAdmin(admin.ModelAdmin):
    list_display = ('id','descricao', 'created_by','updated_by')
    list_display_links = ('id','descricao', )
    readonly_fields = ('created_by','updated_by')
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
            obj.updated_at = datetime.now
        else:
            obj.created_by = request.user
            obj.created_at = datetime.now

        super(TipoAdmin, self).save_model(request, obj, form, change)

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('id','descricao', 'created_by','updated_by')
    list_display_links = ('id','descricao', )
    readonly_fields = ('created_by','updated_by')
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
            obj.updated_at = datetime.now
        else:
            obj.created_by = request.user
            obj.created_at = datetime.now

        super(SetorAdmin, self).save_model(request, obj, form, change)

@admin.register(Cofre)
class CofreAdmin(ImportExportActionModelAdmin):
    # change_form_template = 'cofre/cofre_change_form.html'
    list_display = ('exibir','descricao','usuario','tipo','setor', 'senha_descriptografada')
    list_display_links = ('descricao',)
    search_fields = ('id','descricao','usuario')
    readonly_fields = ('updated_at','created_at','created_by','updated_by','senha_descriptografada')

    fieldsets = (
        ('Identificação', {
            'fields': ('descricao',)
        }),
        ('Local', {
            'classes': ('',),
            'fields': (('hostname','ip'),'url', 'obs'),
        }),
        ('Credenciais', {
            'classes': ('',),
            'fields': (('usuario','senha_descriptografada'),'senha',),
        }),
        ('Classificação', {
            'classes': ('',),
            'fields': (('tipo','setor'),),
        }),
        ('Timestamp', {
            'classes': ('',),
            'fields': ('exibir',('created_at','created_by'),('updated_at','updated_by')),
        }),
    )

    def senha_descriptografada(self, obj):
        from django.utils.safestring import mark_safe
        try: senha = descriptografar(str(obj.senha))
        except: senha = obj.senha
        
        return mark_safe(f"""
            <a id="id_copy_{obj.id}" href="#id_copy_{obj.id}" onclick="navigator.clipboard.writeText(\'{senha}\')" class="addlin">Copiar Senha</a>
        """
        )
        
    senha_descriptografada.short_description='Senha descriptografada'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(CofreAdmin, self).get_form(request, obj,**kwargs)
        if obj:
            form.base_fields["senha"] = forms.CharField(label="Senha", required=True, widget=forms.PasswordInput(attrs={"value": obj.senha}))
        
        return form
    
    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
            obj.updated_at = datetime.now
        else:
            obj.created_by = request.user
            obj.created_at = datetime.now

        # Se o campo de senha for alterado, criptografar
        if 'senha' in form.changed_data:
            obj.senha = criptografar(str(obj.senha))


        super(CofreAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        is_master = request.user.user_permissions.filter(codename='cofre_master').exists()
        is_infra = request.user.user_permissions.filter(codename='cofre_infraestrutura').exists()
        is_dev = request.user.user_permissions.filter(codename='cofre_desenvolvimento').exists()
        q = Cofre.objects.all()
        if is_master:
            return q
        elif is_infra:
            return q.filter(setor__descricao='Infraestrutura', exibir=True)
        elif is_dev:
            return q.filter(setor__descricao='Desenvolvimento', exibir=True)
        else:
            return q.filter(id__isnull=True)


