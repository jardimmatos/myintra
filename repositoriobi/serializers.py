from django.utils.translation import gettext as _
from rest_framework import serializers
from . import models
from datetime import datetime
from users.serializers import UserSimpleSerializer


class CategoriaSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Categoria
        fields = ('id','nome', 'descricao', 'pai')


class CategoriaSerializer(serializers.ModelSerializer):
    filhos = serializers.SerializerMethodField()
    repos = serializers.SerializerMethodField()
    
    def get_filhos(self, obj):
        categ_filhos = obj.categoria_set.all()
        serializer = CategoriaFullSerializer(instance=categ_filhos, many=True)
        return serializer.data
    
    def get_repos(self, obj):
        repos = obj.repo_set.all()
        serializer = RepoFullSerializer(instance=repos, many=True)
        return serializer.data

    class Meta:
        model = models.Categoria
        fields = '__all__'
        read_only_fields = ['created_by','updated_by', 'filhos', 'repos']

    def validate(self, data):
        #if not data.get('first_name'):
        #    raise serializers.ValidationError(_("Primeiro nome não informado"))
        return data

    def create(self, validated_data):
        if not validated_data.get('nome'):
            raise serializers.ValidationError(_("Nome da categoria não informada"))
        
        validated_data['created_by'] = self.context.get('request').user
        validated_data['created_at'] = datetime.now()
        categoria = self.Meta.model(**validated_data)
        categoria.save()

        return categoria

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context.get('request').user or instance.updated_by
        validated_data['updated_at'] = datetime.now()
        
        self.Meta.model.objects.filter(pk=instance.pk).update(**validated_data)
        instance = self.Meta.model.objects.get(pk=instance.pk)
        return instance


class CategoriaFullSerializer(CategoriaSerializer):
    created_by = UserSimpleSerializer(many=False, read_only=True)
    updated_by = UserSimpleSerializer(many=False, read_only=True)


class RepoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Repo
        fields = ('id','descricao','categoria','membros')

        
class RepoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Repo
        fields = '__all__'
        read_only_fields = ['created_by','updated_by']

    def create(self, validated_data):
        if not validated_data.get('descricao'):
            raise serializers.ValidationError(_("Descrição não informada"))
        
        if not validated_data.get('categoria'):
            raise serializers.ValidationError(_("Categoria do repositório não informada"))
        
        validated_data['created_by'] = self.context.get('request').user
        validated_data['created_at'] = datetime.now()
        repo = self.Meta.model(**validated_data)
        repo.save()

        return repo

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context.get('request').user or instance.updated_by
        validated_data['updated_at'] = datetime.now()
        
        self.Meta.model.objects.filter(pk=instance.pk).update(**validated_data)
        instance = self.Meta.model.objects.get(pk=instance.pk)
        return instance


class RepoFullSerializer(RepoSerializer):
    categoria = CategoriaSimpleSerializer(many=False, read_only=True)
    membros = UserSimpleSerializer(many=True, read_only=True)


class CategoriaPaisFilhosSerializer(serializers.ModelSerializer):
    filhos = serializers.SerializerMethodField()
    repos = serializers.SerializerMethodField()
    
    def get_filhos(self, obj):
        categ_filhos = obj.categoria_set.all()
        serializer = CategoriaFullSerializer(instance=categ_filhos, many=True)
        return serializer.data
    
    def get_repos(self, obj):
        repos = obj.repo_set.all()
        serializer = RepoFullSerializer(instance=repos, many=True)
        return serializer.data

    class Meta:
        model = models.Categoria
        fields = '__all__'
        read_only_fields = ['created_by','updated_by', 'filhos', 'repos']