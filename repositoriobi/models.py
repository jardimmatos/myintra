from django.db import models
from base.models import TimeStampedModel
from users.models import User
from django.core.exceptions import ValidationError

class Categoria(TimeStampedModel):
    nome = models.CharField(max_length=255, null=True, blank=False, unique=True)
    descricao = models.CharField(max_length=255, null=True, blank=True, verbose_name="Descrição")
    pai = models.ForeignKey("Categoria", on_delete=models.PROTECT, verbose_name="Categoria Pai", null=True, blank=True)

    def __str__(self):
        return f'{self.nome}'
    
    def clean(self):
        if self.id and self.pai:
            if self.id == self.pai.id:
                raise ValidationError(f"Não é possível associar a categoria \"{self.nome}\" a ela mesma!")

    @property
    def _itens(self):
        return self.repo_set.count()


class Repo(TimeStampedModel):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, null=True, blank=False)
    descricao = models.CharField(max_length=255, null=True, blank=False, verbose_name="Descrição")
    link_bi = models.URLField(null=True, blank=False, verbose_name='Link do BI')
    membros = models.ManyToManyField(User, blank=True)

    def __str__(self):
        str_ = []
        if self.categoria:
            str_ += [self.categoria.nome]
        str_ += [self.descricao]

        return ' - '.join(str_)

    @property
    def _membros(self):
        return self.membros.count()


    class Meta:
        verbose_name = 'Repositório Dados'
        verbose_name_plural = 'Repositórios Dados'
