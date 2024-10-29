from rest_framework import serializers
from . import models
from users.serializers import UserSimpleSerializer


class UnidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Unidade
        exclude = ('created_at','updated_at', 'created_by', 'updated_by')


class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Local
        exclude = ('created_at','updated_at', 'created_by', 'updated_by')


class PrioridadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Prioridade
        exclude = ('created_at','updated_at', 'created_by', 'updated_by')


class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Departamento
        exclude = ('created_at','updated_at', 'created_by', 'updated_by')


class ServicoSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Servico
        fields = ('id', 'nome')

class ServicoSerializer(serializers.ModelSerializer):
    departamento_object = DepartamentoSerializer()

    class Meta:
        model = models.Servico
        exclude = ('created_at','updated_at', 'created_by', 'updated_by')


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cliente
        exclude = ('created_at','updated_at', 'created_by', 'updated_by')


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Perfil
        exclude = ('created_at','updated_at', 'created_by', 'updated_by')


class AtendenteSerializer(serializers.ModelSerializer):
    unidade_object = UnidadeSerializer()
    usuario_object = UserSimpleSerializer()
    local_object = LocalSerializer()
    prioridade_object = PrioridadeSerializer()
    perfil_object = PerfilSerializer()

    class Meta:
        model = models.Atendente
        exclude = ('created_at','updated_at', 'created_by', 'updated_by')
        read_only_fields = ('usuario_object', 'local_object', 'prioridade_object', 'unidade_object')


class AtendimentoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Atendimento
        exclude = ('created_at','updated_at', 'created_by', 'updated_by')


class AtendimentoFullSerializer(serializers.ModelSerializer):
    servico_object = ServicoSerializer()
    unidade_object = UnidadeSerializer()
    prioridade_object = PrioridadeSerializer()
    cliente_object = ClienteSerializer()
    local_object = LocalSerializer()
    sigla_senha = serializers.SerializerMethodField()

    def get_sigla_senha(self, obj):
        return obj.sigla_senha

    class Meta:
        model = models.Atendimento
        exclude = ('created_at','updated_at', 'created_by', 'updated_by')

class AtendimentoComentarioSerializer(serializers.ModelSerializer):
    created_by_object = UserSimpleSerializer()
    updated_by_object = UserSimpleSerializer()
    get_created_at = serializers.CharField()
    get_updated_at = serializers.CharField()

    class Meta:
        model = models.AtendimentoComentario
        exclude = ('created_at', 'updated_at')


class PainelSenhaSerializer(serializers.ModelSerializer):
    atendimento_object = AtendimentoFullSerializer()
    class Meta:
        model = models.PainelSenha
        exclude = ('created_at','updated_at', 'created_by', 'updated_by')
