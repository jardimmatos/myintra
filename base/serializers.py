from rest_framework import serializers
from . import models


class MonitorServicoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MonitorServico
        exclude = ('created_at', 'updated_at', 'created_by', 'updated_by',)


class TeamsChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TeamsChannel
        exclude = ('created_at', 'updated_at', 'created_by', 'updated_by')
