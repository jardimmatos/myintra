from datetime import datetime
from django.contrib import admin, messages
from django.utils.translation import gettext as _
from django.contrib.auth.admin import UserAdmin
from . import models
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Permission, Group
from base.utils import call_ws, register_gateway
from django.utils.html import format_html


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    readonly_fields = ('name','content_type', 'codename', 'usuarios', 'grupos')
    search_fields = ('name','codename')
    list_filter = ('content_type',)

    def grupos(model, obj):
        grupos = "<br>".join([ f'<a href="/admin/auth/group/{u.id}/change/" target="_blank">{ u.name }</a>' for u in obj.group_set.all()])
        return format_html(grupos)

    def usuarios(model, obj):
        usuarios = "<br>".join([ f'<a href="/admin/users/user/{u.id}/change/" target="_blank">{ u.get_full_name() }</a>' for u in obj.user_set.all()])
        return format_html(usuarios)


@admin.register(models.User)
class UserAdmin(UserAdmin):
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    list_prefetch_related = ('user_permissions',)
    list_display = ('username', 'email', 'get_full_name','is_active','is_staff', 'is_superuser', )
    list_display_links = ('username',)
    filter_horizontal = ('user_permissions',)
    readonly_fields = ('date_joined','token', 'last_login', 'created_by', 'updated_by','created_at','updated_at', 'is_gestor_espacos', 'is_admin_espacos', 'repositorios_vinculados')
    list_per_page = 10
    show_full_result_count = True
    # autocomplete_fields = ['groups','filiais',]
    autocomplete_fields = ['groups']

    save_as = True
    search_fields = ('username', 'email','first_name', 'last_name')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'first_name', 'last_name','password1', 'password2','is_staff','is_superuser','groups'),
        }),
    )

    fieldsets = (
        (_('Identificação'), {
            'classes': ('',),
            'fields': ( ('first_name','last_name'),),
        }),
        (_('Token do Usuário/API'), {
            'fields': ('token',)
        }),
        (_('Usuário'), {
            'fields': (('username','email'), 'password',)
        }),
        (_('Liberação de Acesso'), {
            'classes': ('',),
            'fields': (('is_active', 'is_staff'), 'is_superuser',),
        }),
        (_('Permissões'), {
            'classes': ('',),
            'fields': ('groups', 'user_permissions'),
        }),
        (_('Registro do dado'), {
            'classes': ('collapse',),
            'fields': ('date_joined', ('created_by', 'created_at'),('updated_by','updated_at')),
        }),
        (_('AgendaLabs'), {
            'classes': ('collapse',),
            'fields': ('is_gestor_espacos','is_admin_espacos'),
        }),
        (_('Repositórios Vinculados'), {
            'classes': ('collapse',),
            'fields': ('repositorios_vinculados',),
        }),
    )

    date_hierarchy = 'last_login'
    ordering = ['-first_name']
    actions = ['activeUser','generateToken', 'revokeToken', 'renew_session', 'teste_gateway']

    def is_gestor_espacos(self, obj):
        espacos = "<br>".join([ f'<a href="/admin/agenda/espaco/{u.id}/change/" target="_blank">{ u.descricao }</a>' for u in obj.gestor_espaco_users.all()])
        return format_html(espacos)
    is_gestor_espacos.short_description = 'Gestor nos espaços'

    def repositorios_vinculados(self, obj):
        repositorios = "<br>".join([ f'<a href="/admin/repositoriobi/repo/{u.id}/change/" target="_blank">{ u.descricao }</a>' for u in obj.repo_set.all()])
        return format_html(repositorios)
    repositorios_vinculados.short_description = 'Repositórios Vinculados'

    def is_admin_espacos(self, obj):
        espacos = "<br>".join([ f'<a href="/admin/agenda/espaco/{u.id}/change/" target="_blank">{ u.descricao }</a>' for u in obj.admin_users.all()])
        return format_html(espacos)
    is_admin_espacos.short_description = 'Admin nos espaços'

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
            obj.updated_at = datetime.now()
        else:
            obj.created_by = request.user
            obj.created_at = datetime.now()

        super(UserAdmin, self).save_model(request, obj, form, change)
    
    # ACTION TO ACTIVE/DEACTIVE USER
    def activeUser(modeladmin, request, queryset):
        for obj in queryset:
            if not obj.is_staff:
                obj.is_active = not obj.is_active
                obj.save()
            else:
                if not obj.is_active:
                    obj.is_active = not obj.is_active
                    obj.save()
                    register_gateway(request, f'Reativando usuário', 'Users')

    activeUser.short_description = _("Ativar/Desativar usuário")
    # TODO: test user not superuser
    activeUser.allowed_permissions = ('change',)
    
    # RENEW SESSION AND USER PERMISSIONS IN FRONTEND
    def renew_session(modeladmin, request, queryset):
        for obj in queryset:
            room = f'{"room_channel_session_user_"}{obj.id}'
            call_ws(channel_name=room, 
                tag='USER-REFRESH', 
                msg="Renovando sessão de usuário"
            )
            register_gateway(request, f'Renovando sessão do usuário', 'Users')
    renew_session.short_description = _("renovar sessão do usuário")
    # TODO: test user not superuser
    renew_session.allowed_permissions = ('change',)

    # Teste Gateway
    def teste_gateway(modeladmin, request, queryset):
        for obj in queryset:
            register_gateway(request, f"Testando Gateway no usuário ws: {obj.username}", 'Users')
    teste_gateway.short_description = _("Testar Gateway")
    

    # TODO: test permission as non-superuser
    def has_active_user_permission(self, request):
        return request.user.has_perm('users.change_user')

    # ACTION TO GENERATE TOKEN
    def generateToken(modeladmin, request, queryset):
        for obj in queryset:
            token = obj.generate_token()
            obj.token = token
            obj.save()
            register_gateway(request, f'Gerando Token para usuário {obj.username}', 'Users')
            messages.success(request, f'Geração de Token finalizada: {token}')

    generateToken.short_description = _("Gerar Token de Usuário")
    generateToken.allowed_permissions = ('generate_token',)
    def has_generate_token_permission(self, request):
        return request.user.has_perm('users.generate_token')

    # ACTION TO REVOKE TOKEN
    def revokeToken(modeladmin, request, queryset):
        for obj in queryset:
            token = None
            obj.token = token
            obj.save()
            register_gateway(request, f'Revogando token do usuário {obj.username}', 'Users')
            messages.success(request, f'Revogação de Token finalizada')

    revokeToken.short_description = _("Revogar Token de Usuário")
    revokeToken.allowed_permissions = ('generate_token',)
    
    # TODO: test permission as non-superuser
    def has_revoke_token_permission(self, request):
        return request.user.has_perm('users.generate_token')

    # def get_search_results(self, request, queryset, search_term):
    #     queryset, use_distinct = super().get_search_results(request, queryset, search_term)
    #     # Limite os resultados a 100 para evitar lentidão
    #     return queryset[:10], use_distinct

@admin.register(models.AccessHistory)
class AccessHistoryAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'origin', 'access_at', 'ip')
    readonly_fields = ('origin','ip', 'access_at', 'user')
    list_filter = ('origin','user')
    date_hierarchy = 'access_at'


@admin.register(models.ApiRequests)
class ApiRequestsAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'view_basename', 'view_action', 'view_method', 'requested_at')
    list_filter = ('user', 'view_basename', 'view_method', 'view_action')
    date_hierarchy = 'requested_at'
    search_fields = ('user__username', 'view_basename', 'view_pk')
    readonly_fields = (
        'user', 
        'token',
        'view_data_post',
        'view_data_get',
        'view_query_params_get',
        'view_basename',
        'view_action',
        'view_pk',
        'view_method',
        'requested_at'
    )


@admin.register(models.LoggedUser)
class LoggedUserAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'logged_at')
    readonly_fields = (
        'user', 
        'logged_at'
    )


class GroupsAdmin(GroupAdmin):
    readonly_fields = ('usuarios',)
    def usuarios(model, obj):
        usuarios = "<br>".join([ f'<a href="/admin/users/user/{u.id}/change/" target="_blank">{ u.get_full_name() }</a>' for u in obj.user_set.all()])
        return format_html(usuarios)

admin.site.unregister(Group)
admin.site.register(Group, GroupsAdmin)