from django.db import models
from .enums import StatusItemCirculacao, StatusCirculacao, StatusDispositivo

"""
class DispositivoAvariaManager(models.Manager):

    def get_queryset(self):
        return super(DispositivoAvariaManager, self).get_queryset().filter(situacao=StatusDispositivo.AVARIADO.name)


class DispositivoExtravioManager(models.Manager):

    def get_queryset(self):
        return super(DispositivoExtravioManager, self).get_queryset().filter(situacao=StatusDispositivo.EXTRAVIO.name)


class DispositivoDisponivelManager(models.Manager):

    def get_queryset(self):
        return super(DispositivoDisponivelManager, self)\
            .get_queryset().filter(situacao=StatusDispositivo.DISPONIVEL.name)


class DispositivoManutencaoManager(models.Manager):

    def get_queryset(self):
        return super(DispositivoManutencaoManager, self)\
            .get_queryset().filter(situacao=StatusDispositivo.MANUTENCAO.name)

class EntregaAbertoManager(models.Manager):
    def get_queryset(self):
        return super(EntregaAbertoManager, self)\
            .get_queryset().filter(situacao=StatusEmprestimo.ABERTO.name)


class EntregaFinalizadoManager(models.Manager):
    def get_queryset(self):
        return super(EntregaFinalizadoManager, self)\
            .get_queryset().filter(situacao=StatusEmprestimo.FINALIZADO.name)


class EntregaCanceladoManager(models.Manager):
    def get_queryset(self):
        return super(EntregaCanceladoManager, self)\
            .get_queryset().filter(situacao=StatusEmprestimo.CANCELADO.name)


class EntregaItemDisponivelManager(models.Manager):
    def get_queryset(self):
        return super(EntregaItemDisponivelManager, self)\
            .get_queryset().filter(situacao=StatusItemCirculacao.DISPONIVEL.name)


class EntregaItemEmprestadoManager(models.Manager):
    def get_queryset(self):
        return super(EntregaItemEmprestadoManager, self)\
            .get_queryset().filter(situacao=StatusItemCirculacao.EMPRESTADO.name)


class EntregaItemAvariaManager(models.Manager):
    def get_queryset(self):
        return super(EntregaItemAvariaManager, self)\
            .get_queryset().filter(situacao=StatusItemCirculacao.DEVOLVIDO_AVARIA.name)
"""

# class ItemCirculacaoManager(models.Manager):
#     def create(self, **kwargs):
        
#         return super().create(**kwargs)



