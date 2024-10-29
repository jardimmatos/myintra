from django.db import models
from base.models import TimeStampedModel
from django_quill.fields import QuillField


class CategoriaSistema(TimeStampedModel):
    nome = models.CharField('Sistema', max_length=100, unique=True, null=True, blank=False)
    
    def __str__(self):
        return f'{self.nome}'


class Wiki(TimeStampedModel):
    titulo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Título")
    sistema = models.ForeignKey(CategoriaSistema, on_delete=models.PROTECT, null=True, blank=False)
    # locais = models.ManyToManyField('users.Local', blank=True)
    membros = models.ManyToManyField('users.user', blank=True)
    text = models.TextField(blank=True, null=True)
    html = models.TextField(blank=True, null=True)
    corpo = QuillField(blank=False, null=True)
    ativo = models.BooleanField(default=True)

    def sistema_object(self):
        return self.sistema

    # def setor_objects(self):
    #     return self.locais.all()
    
    def membros_objects(self):
        return self.membros.all()

    def __str__(self):
        return f'{self.titulo}'
    
    def clean(self):
        self.text = self.corpo.plain
        self.html = self.corpo.html
    
    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Wiki'
        verbose_name_plural = 'Wikis'