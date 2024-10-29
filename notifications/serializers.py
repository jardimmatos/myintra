from rest_framework import serializers
from django.db import transaction
from . import models
from datetime import datetime
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django_quill.quill import Quill
from base.utils import call_ws

class NotificacaoSerializer(serializers.ModelSerializer):
    mensagem = serializers.CharField()


    class Meta:
        model = models.Notificacao
        fields = '__all__'
        read_only_fields = ['created_by','updated_by','html','plain']
    
    def validate(self, data):
        #if not data.get('first_name'):
        #    raise serializers.ValidationError(_("Primeiro nome não informado"))
        return data

    def try_message_quill(self, msg):
        # Formato aceitável para o campo mensagem(tipo QuillField)
        import re
        pattern = re.compile('<.*?>')
        result = re.sub(pattern, '', msg)
        mensagem = {
            "delta": '{\"ops\": [ {\"insert\": \"' + result + '\"} ] }' ,
            "html": msg
        }
        # Retorna instancia de Quill
        quill = Quill(json.dumps(mensagem))
        return quill
    
    def create(self, validated_data):
        with transaction.atomic():
            if not validated_data.get('inicio', None):
                raise serializers.ValidationError('Data de início não informada')

            # Stamps
            validated_data['created_by'] = self.context.get('request').user
            validated_data['created_at'] = datetime.now()
            #validated_data['mensagem'] = self.try_message_quill( validated_data.get('mensagem') )

            obj = self.Meta.model(**validated_data)
            obj.mensagem = self.try_message_quill( validated_data.get('mensagem') )

            obj.save()

            # if  obj.inicio <= datetime.now() and \
            #     (obj.fim >= datetime.now() or  not obj.fim) and \
            #     obj.id == obj.id:
            now = int(datetime.timestamp(datetime.now()))
            now = datetime.now().strftime('%Y-%m-%d %H:%M')
            now = datetime.strptime(now, '%Y-%m-%d %H:%M')
            try:
                inicio = obj.inicio.strftime('%Y-%m-%d %H:%M')
                inicio = datetime.strptime(inicio, '%Y-%m-%d %H:%M')
                fim = obj.fim.strftime('%Y-%m-%d %H:%M')
                fim = datetime.strptime(fim, '%Y-%m-%d %H:%M')
                if  inicio <= now and \
                    (fim >= now or not fim): 
                    call_ws('room_channel_notifications','Uma notificação [{}] foi criada'.format(validated_data.get('titulo', '...')), 'NOTIFICATION-CREATED', notify=True)
            except:
                pass

            return obj

    def update(self, instance, validated_data):
        with transaction.atomic():
            validated_data['updated_by'] = self.context.get('request').user or instance.updated_by
            validated_data['updated_at'] = datetime.now()
            
            quill = validated_data.pop('mensagem')
            
            instance = super().update(instance, validated_data)
            instance.mensagem = self.try_message_quill(quill)
            instance.save()
            
            now = int(datetime.timestamp(datetime.now()))
            now = datetime.now().strftime('%Y-%m-%d %H:%M')
            now = datetime.strptime(now, '%Y-%m-%d %H:%M')
            try:
                inicio = instance.inicio.strftime('%Y-%m-%d %H:%M')
                inicio = datetime.strptime(inicio, '%Y-%m-%d %H:%M')
                fim = instance.fim.strftime('%Y-%m-%d %H:%M')
                fim = datetime.strptime(fim, '%Y-%m-%d %H:%M')
                if  inicio <= now and \
                    (fim >= now or not fim): 
                    call_ws('room_channel_notifications','Uma notificação foi atualizada',  'NOTIFICATION-CHANGED', notify=True)
            except:
                pass

            return instance