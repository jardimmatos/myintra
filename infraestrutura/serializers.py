from rest_framework import serializers, validators
from . import models
from datetime import datetime
from django.db import transaction
from users import serializers as user_serializers

class LocalUsoSerializer(serializers.ModelSerializer):
    descricao = serializers.CharField(validators=[
            validators.UniqueValidator(
                message="Já existe um Local de Uso com a descrição informada!",
                queryset=models.LocalUso.objects.all(),
                lookup='exact'
            )
        ])

    class Meta:
        model = models.LocalUso
        exclude = ('created_at','updated_at','created_by', 'updated_by',)
    
    def create(self, validated_data):
        with transaction.atomic():
            request = self.context.get('request')
            validated_data['created_by'] = request.user
            validated_data['created_at'] = datetime.now()
            
            obj = self.Meta.model(**validated_data)
            obj.save()
            
        return obj

    def update(self, instance, validated_data):
        with transaction.atomic():
            request = self.context.get('request')
            validated_data['updated_by'] = request.user or instance.updated_by
            validated_data['updated_at'] = datetime.now()
            
            self.Meta.model.objects.filter(pk=instance.pk).update(**validated_data)
            instance = self.Meta.model.objects.get(pk=instance.pk)
            
            return instance


class EquipamentoSerializer(serializers.ModelSerializer):
    descricao = serializers.CharField(validators=[
            validators.UniqueValidator(
                message="Já existe um Equipamento com a descrição informada!",
                queryset=models.Equipamento.objects.all(),
                lookup='exact'
            ),
        ])

    class Meta:
        model = models.Equipamento
        exclude = ('created_at','updated_at','created_by', 'updated_by',)
    
    def create(self, validated_data):
        with transaction.atomic():
            request = self.context.get('request')
            validated_data['created_by'] = request.user
            validated_data['created_at'] = datetime.now()
            
            obj = self.Meta.model(**validated_data)
            obj.save()
            
        return obj

    def update(self, instance, validated_data):
        with transaction.atomic():
            request = self.context.get('request')
            validated_data['updated_by'] = request.user or instance.updated_by
            validated_data['updated_at'] = datetime.now()
            
            self.Meta.model.objects.filter(pk=instance.pk).update(**validated_data)
            instance = self.Meta.model.objects.get(pk=instance.pk)
            
            return instance


class StatusDispositivoSerializer(serializers.ModelSerializer):
    descricao = serializers.CharField(validators=[
            validators.UniqueValidator(
                message="Já existe um Equipamento com a descrição informada!",
                queryset=models.StatusDispositivo.objects.all(),
                lookup='exact'
            ),
        ])
    created_by = user_serializers.UserSimpleSerializer(many=False, read_only=True)
    updated_by = user_serializers.UserSimpleSerializer(many=False, read_only=True)

    class Meta:
        model = models.StatusDispositivo
        fields = '__all__'
        read_only_fields = ('created_at','updated_at','created_by', 'updated_by',)
    
    def create(self, validated_data):
        with transaction.atomic():
            request = self.context.get('request')
            validated_data['created_by'] = request.user
            validated_data['created_at'] = datetime.now()
            
            obj = self.Meta.model(**validated_data)
            obj.save()
            
        return obj

    def update(self, instance, validated_data):
        with transaction.atomic():
            request = self.context.get('request')
            validated_data['updated_by'] = request.user or instance.updated_by
            validated_data['updated_at'] = datetime.now()
            
            self.Meta.model.objects.filter(pk=instance.pk).update(**validated_data)
            instance = self.Meta.model.objects.get(pk=instance.pk)
            
            return instance


class DispositivoSerializer(serializers.ModelSerializer):
    identificador = serializers.CharField(validators=[
            validators.UniqueValidator(
                message="Já existe um Dispositivo com o identificador informado!",
                queryset=models.Dispositivo.objects.all(),
                lookup='exact'
            )
        ])
    equipamento_object = EquipamentoSerializer(many=False, read_only=True)
    situacao_object = serializers.SerializerMethodField()
    status_inventario_object = StatusDispositivoSerializer(many=False, read_only=True)
    created_by = user_serializers.UserSimpleSerializer(many=False, read_only=True)
    updated_by = user_serializers.UserSimpleSerializer(many=False, read_only=True)

    def get_situacao_object(self, obj):
        return obj.situacao_object()

    class Meta:
        model = models.Dispositivo
        fields = '__all__'
        read_only_fields = ('created_at','updated_at','created_by', 'updated_by',)

    def validate(self, data):
        return data

    def create(self, validated_data):
        if not validated_data.get('identificador'):
           raise serializers.ValidationError({'identificador': "Necessário informar um código identificador único"})
        
        if not validated_data.get('equipamento'):
           raise serializers.ValidationError({'equipamento': "Necessário vincular um equipamento"})
        
        with transaction.atomic():
            request = self.context.get('request')
            validated_data['created_by'] = request.user
            validated_data['created_at'] = datetime.now()
            
            obj = self.Meta.model(**validated_data)
            obj.save()
            
        return obj

    def update(self, instance, validated_data):
        with transaction.atomic():
            request = self.context.get('request')
            validated_data['updated_by'] = request.user or instance.updated_by
            validated_data['updated_at'] = datetime.now()
            
            self.Meta.model.objects.filter(pk=instance.pk).update(**validated_data)
            instance = self.Meta.model.objects.get(pk=instance.pk)
            instance.clean()
            
            return instance


class ItemCirculacaoSerializer(serializers.ModelSerializer):
    dispositivo_object = DispositivoSerializer(many=False, read_only=True)
    situacao_object = serializers.SerializerMethodField()
    created_by = user_serializers.UserSimpleSerializer(many=False, read_only=True)
    recebedor = user_serializers.UserSimpleSerializer(many=False, read_only=True)
    
    def get_situacao_object(self, obj):
        try:
            return obj.situacao_object()
        except: return ''

    class Meta:
        model = models.ItemCirculacao
        exclude = ('updated_at','updated_by',)
        # campos de fluxos
        read_only_fields = ('situacao', 
                            'recebedor',
                            'devolvido_em',
                            'created_at',
                            'created_by',
                            )
    
    def update(self, instance, validated_data):
        if 'circulacao' in validated_data:
            # Remover o índice de circulacao para evitar que um item circulacao seja alterado de uma circulacao diretamente, fugindo do fluxo
            del validated_data['circulacao']
        if 'dispositivo' in validated_data:
            # Remover o índice de dispositivo para evitar que um item circulacao seja alterado de uma circulacao diretamente, fugindo do fluxo
            del validated_data['dispositivo']
        with transaction.atomic():
            request = self.context.get('request')
            validated_data['updated_by'] = request.user or instance.updated_by
            validated_data['updated_at'] = datetime.now()
            
            self.Meta.model.objects.filter(pk=instance.pk).update(**validated_data)
            instance = self.Meta.model.objects.get(pk=instance.pk)
            return instance


class CirculacaoSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Circulacao
        fields = ('dict_read_only',)
        read_only_fields = ('dict_read_only',)

class CirculacaoSerializer(serializers.ModelSerializer):
    local_object = LocalUsoSerializer(many=False, read_only=True)
    item_objects = ItemCirculacaoSerializer(many=True, read_only=True)
    situacao_object = serializers.SerializerMethodField()
    created_by = user_serializers.UserSimpleSerializer(many=False, read_only=True)
    updated_by = user_serializers.UserSimpleSerializer(many=False, read_only=True)
    baixado_por = user_serializers.UserSimpleSerializer(many=False, read_only=True)

    def get_situacao_object(self, obj):
        try:
            return obj.situacao_object()
        except: return ''

    class Meta:
        model = models.Circulacao
        fields = '__all__'
        read_only_fields = ('item_objects','local_object',
                            # campos de fluxos, no readonly eles não retornam no serializer da requisição
                            'situacao',
                            'baixado_por',
                            'motivo_cancelamento',
                            'data_baixa',
                            'created_by',
                            'created_at',
                            'updated_at',
                            'updated_by',
                            )
    
    def update(self, instance, validated_data):
        with transaction.atomic():
            request = self.context.get('request')
            validated_data['updated_by'] = request.user or instance.updated_by
            validated_data['updated_at'] = datetime.now()
            
            self.Meta.model.objects.filter(pk=instance.pk).update(**validated_data)
            instance = self.Meta.model.objects.get(pk=instance.pk)
            instance.clean()

            return instance


class LogDispositivoSerializer(serializers.ModelSerializer):
    situacao_object = serializers.SerializerMethodField()
    circulacao_object = CirculacaoSerializer(many=False, read_only=True)
    created_by = user_serializers.UserSimpleSerializer(many=False, read_only=True)

    def get_situacao_object(self, obj):
        try:
            return obj.situacao_object()
        except:
            return ''

    class Meta:
        model = models.LogDispositivo
        fields = '__all__'


class LogCirculacaoSerializer(serializers.ModelSerializer):
    situacao_object = serializers.SerializerMethodField()
    created_by = user_serializers.UserSimpleSerializer(many=False, read_only=True)
    # circulacao_object = CirculacaoSerializer(many=False, read_only=True)

    def get_situacao_object(self, obj):
        try:
            return obj.situacao_object()
        except:
            return ''

    class Meta:
        model = models.LogCirculacao
        fields = '__all__'