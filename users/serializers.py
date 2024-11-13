from rest_framework import serializers
from . import models
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from datetime import datetime


class ContentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContentType
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'name')


class UserSerializer(serializers.ModelSerializer):
    user_count_bis = serializers.SerializerMethodField()
    is_atendente = serializers.SerializerMethodField()
    get_imagem = serializers.SerializerMethodField()

    def get_user_count_bis(self, obj):
        return obj.user_count_bis

    def get_is_atendente(self, obj):
        return obj.is_atendente

    def get_get_imagem(self, obj):
        return obj.get_imagem

    class Meta:
        model = models.User
        exclude = ('password', 'groups', 'user_permissions', 'token', 'imagem')
        read_only_fields = ('created_by', 'updated_by', 'date_joined',
                            'last_login', 'get_imagem', 'is_atendente')

    def validate(self, data):
        # if not data.get('first_name'):
        #    raise serializers.ValidationError("Primeiro nome não informado")
        return data

    def create(self, validated_data):
        if not validated_data.get('username'):
            raise serializers.ValidationError("Nome de usuário não informado")

        # Registrar stamps
        validated_data['created_by'] = self.context.get('request').user
        validated_data['created_at'] = datetime.now()

        # separar(e remover do dict) username, password e e-mail para
        # parâmetros da função .create_user()
        username = validated_data.pop('username')

        password = '123456'
        email = validated_data.pop('email', None)

        # ignore Staff and Superuser flag, for security
        validated_data['is_superuser'] = False
        validated_data['is_staff'] = False
        validated_data['is_active'] = True

        user = models.User.objects.create_user(
            username, email, password, **validated_data)
        return user

    def update(self, instance, validated_data):
        validated_data['updated_by'] = (
            self.context.get('request').user or instance.updated_by)
        validated_data['updated_at'] = datetime.now()

        # action set_auper exclusiva para esta prop
        validated_data['is_superuser'] = instance.is_superuser

        # action set_admin exclusiva para estas props
        validated_data['is_staff'] = instance.is_staff
        validated_data['is_active'] = instance.is_active

        models.User.objects.filter(pk=instance.pk).update(**validated_data)
        instance = models.User.objects.get(pk=instance.pk)
        return instance


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True, required=True)


class UserAdminSerializer(serializers.Serializer):
    is_staff = serializers.BooleanField(required=False, write_only=True)
    is_active = serializers.BooleanField(required=False, write_only=True)


class UserSuperSerializer(serializers.Serializer):
    is_superuser = serializers.BooleanField()


# Serializa ContentType em Permission
class PermissionContentTypeSerializer(serializers.ModelSerializer):
    content_type = ContentTypeSerializer(many=False, read_only=True)

    class Meta:
        model = Permission
        fields = '__all__'


# Serializa as permissões em Grupo
class GroupPermissionsSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'


# serializa grupos e permissões em usuários
class UserFullSerializer(serializers.ModelSerializer):
    # groups = GroupPermissionsSerializer(many=True, read_only=True)
    get_groups = serializers.SerializerMethodField()
    get_perms = serializers.SerializerMethodField()
    # get_filiais = serializers.SerializerMethodField()
    user_count_bis = serializers.SerializerMethodField()
    is_atendente = serializers.SerializerMethodField()
    # user_is_gestor = serializers.SerializerMethodField()
    # get_imagem = serializers.SerializerMethodField()

    def get_user_count_bis(self, obj):
        return obj.user_count_bis

    def get_is_atendente(self, obj):
        return obj.is_atendente

    def get_get_groups(self, obj):
        return [group.name for group in obj.groups.all()]

    def get_get_perms(self, obj):
        perms = [perm.codename for perm in obj.user_permissions.all()]
        groups = obj.groups.all()
        for g in groups:
            perms += [
                perm.codename
                for perm in g.permissions.exclude(codename__in=perms).all()]
        return perms

    class Meta:
        model = models.User
        exclude = ('password', )
        read_only_fields = ('created_by', 'updated_by', 'perms', 'groups',)


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
