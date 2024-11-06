from django.contrib import admin
from . import models
from django.db.models import Q
from datetime import datetime
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@admin.register(models.Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    save_as = True
    readonly_fields = ('created_by', 'created_at', 'updated_at', 'updated_by','text','html')
    list_display = ('titulo', 'text', 'inicio', 'fim')
    actions = ['refresh_notifications']

    def refresh_notifications(modeladmin, request, queryset):
        modeladmin.call_ws(tag='CHANGED', notify=False)
    refresh_notifications.short_description = "Atualizar Notificações"

    def call_ws(self, msg='', tag='CHANGED', notify=True):
        # usado apenas para disparar um CHANGED type para o channel
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'room_channel_notifications',
            {
                'type': 'send_message',
                'message': str(msg),
                "event": str(tag),
                "notify": notify
            }
        )

    def delete_model(self, request, obj) -> None:
        return super().delete_model(request, obj)
    
    def delete_queryset(self, request, queryset):
        return super().delete_queryset(request, queryset)

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            obj = form.save(commit=True)
        super().save_model(request, obj, form, change)
        if obj:
            exists = models.Notificacao.objects.filter(
                # Notificações com data de inicio a partir de HOJE
                Q(inicio__lte=datetime.now()), 
                # Notificações com data de fim acima de  HOJE
                Q(Q(fim__gte=datetime.now()) | Q(fim__isnull=True)),
                Q( id=obj.id )
            ).exists()
            if exists:
                if change:
                    self.call_ws(f'A notificação <strong>{obj.titulo}</strong> foi atualizada',
                                'CHANGED', notify=True)
                else:
                    self.call_ws(obj.titulo, 'CREATED', notify=True)

        
    
    


