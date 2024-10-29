from rest_framework import serializers
from django.db import transaction
from . import models
from datetime import datetime
import json
from django_quill.quill import Quill
from users.serializers import UserSimpleSerializer

class CategoriaSistemaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CategoriaSistema
        fields = ('id','nome',)
        read_only_fields = ['id']
    
    def validate(self, data):
        if not data.get('nome'):
            raise serializers.ValidationError(("Nome da categoria não informado"))

        return data

    def create(self, validated_data):
        # Stamps
        validated_data['created_by'] = self.context.get('request').user
        validated_data['created_at'] = datetime.now()

        obj = self.Meta.model(**validated_data)
        obj.save()

        return obj

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context.get('request').user or instance.updated_by
        validated_data['updated_at'] = datetime.now()

        instance = super().update(instance, validated_data)
        
        return instance


class WikiSerializer(serializers.ModelSerializer):
    corpo = serializers.CharField()
    sistema_object = CategoriaSistemaSerializer(many=False, read_only=True)
    membros_objects = UserSimpleSerializer(many=True, read_only=True)
    criado_por = serializers.SerializerMethodField()

    def get_criado_por(self, obj):
        return obj.created_by.first_name

    class Meta:
        model = models.Wiki
        fields = '__all__'
        read_only_fields = ['created_by','updated_by','html','text', 'membros_objects', 'criado_por', 'sistema_object']
    
    def validate(self, data):
        #if not data.get('first_name'):
        #    raise serializers.ValidationError(("Primeiro nome não informado"))
        return data

    def try_message_quill(self, msg):
        # Formato aceitável para o campo corpo(tipo QuillField)
        import re
        pattern = re.compile('<.*?>')
        result = re.sub(pattern, '', msg)
        corpo = {
            "delta": '{\"ops\": [ {\"insert\": \"' + result + '\"} ] }' ,
            "html": msg
        }
        # Retorna instancia de Quill
        quill = Quill(json.dumps(corpo))
        return quill
    
    def create(self, validated_data):
        with transaction.atomic():
            # Stamps
            validated_data['created_by'] = self.context.get('request').user
            validated_data['created_at'] = datetime.now()
            membros = validated_data.pop('membros', [])
            obj = self.Meta.model(**validated_data)
            obj.corpo = self.try_message_quill( validated_data.get('corpo') )
            obj.save()
            obj.membros.set(membros)
            # obj.save()

            return obj

    def update(self, instance, validated_data):
        with transaction.atomic():
            validated_data['updated_by'] = self.context.get('request').user or instance.updated_by
            validated_data['updated_at'] = datetime.now()
            corpo = validated_data.get('corpo')
            if corpo:
                validated_data['html'] = corpo
                validated_data.pop('corpo')


            instance = super().update(instance, validated_data)
            
            if corpo:
                quill = corpo
                instance.corpo = self.try_message_quill(quill)
                instance.save()

            return instance