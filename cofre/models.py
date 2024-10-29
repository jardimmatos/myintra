from base.models import TimeStampedModel
from django.db import models

class Setor(TimeStampedModel):
    descricao = models.CharField(max_length=254, unique=True, verbose_name='Setor', blank=False, null=True)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name='Setor'
        verbose_name_plural='Setores'


class Tipo(TimeStampedModel):
    descricao = models.CharField(max_length=254, unique=True, verbose_name='Tipo',blank=False, null=True)
    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name='Tipo'
        verbose_name_plural='Tipos'

class Cofre(TimeStampedModel):
    descricao = models.CharField(max_length=254, verbose_name='Descrição', blank=False, null=True)
    hostname = models.CharField(max_length=254, verbose_name='Hostname',blank=True, null=True)
    ip = models.CharField(max_length=254, verbose_name='IP',blank=True, null=True)
    url = models.CharField(max_length=254, verbose_name='Url',blank=True, null=True)
    usuario = models.CharField(max_length=254, verbose_name='Usuário',blank=False, null=True)
    senha = models.CharField(max_length=254, verbose_name='Senha',blank=False, null=True, help_text="Altere este campo somente se desejar alterar a senha. O campo é criptografado após salvar.")
    obs = models.TextField(verbose_name='Observações',blank=True, null=True)
    tipo = models.ForeignKey(Tipo, verbose_name='Tipo', related_name='senhas', on_delete=models.PROTECT, blank=False, null=True)
    setor = models.ForeignKey(Setor, verbose_name='Setor', related_name='senhas', on_delete=models.PROTECT, blank=False, null=True)
    exibir = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.descricao} - {self.tipo}'
        

    class Meta:
        verbose_name = 'Registro de Cofre'
        verbose_name_plural = 'Registros de Cofre'
        unique_together = ('descricao', 'usuario','tipo', 'setor')
        permissions = (
            ('cofre_infraestrutura', 'Acessar Cofre Infraestrutura'),
            ('cofre_desenvolvimento', 'Acessar Cofre Desenvolvimento'),
            ('cofre_master', 'Acessar Cofre Integral')
        )