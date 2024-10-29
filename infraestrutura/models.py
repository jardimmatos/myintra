from django.db import models, transaction
from base. models import TimeStampedModel
from . import enums
from django.core.exceptions import ValidationError
from datetime import datetime
from django.conf import settings

class LocalUso(TimeStampedModel):
    """ Local onde os dispositivos serão utilizados """
    descricao = models.CharField(max_length=100, unique=True, blank=False,
                                null=True, verbose_name='Descrição')

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Local de Uso'
        verbose_name_plural = 'Locais de Uso'
        ordering = ('descricao',)


class Equipamento(TimeStampedModel):
    """ Classe de Equipamentos (Ex: iPad, Projeto, ...)"""
    descricao = models.CharField(max_length=100, unique=True, blank=False,
                                 null=True, verbose_name='Descrição')

    def __str__(self):
        return self.descricao

class StatusDispositivo(TimeStampedModel):
    descricao = models.CharField(max_length=100, unique=True, blank=False,
                                 null=True, verbose_name='Descrição')
    permite_circular = models.BooleanField(default=True)
    color = models.CharField(max_length=100, blank=True, null=True,
                             verbose_name='Cor', default="#dddd")

    def __str__(self):
        return self.descricao


class Dispositivo(TimeStampedModel):
    """ 
        Equipamentos identificados com seus códigos únicos (identificador), 
        Ex: iPad 102030, iPad 502030, Projetor 105090 ...)
    """
    identificador = models.CharField(max_length=100, unique=True, blank=False,
                                     null=True, verbose_name='Código')
    serie = models.CharField(max_length=150, blank=True, null=True, verbose_name='Nº Série')
    equipamento = models.ForeignKey(Equipamento, on_delete=models.PROTECT, blank=False,
                                    null=True, verbose_name='Equipamento')
    status_inventario = models.ForeignKey(StatusDispositivo, on_delete=models.PROTECT,
                                          blank=True, null=True, verbose_name='Status no Inventário')
    obs_inventario = models.TextField(null=True, blank=True)
    situacao = models.CharField(max_length=50, default=enums.StatusDispositivo.DISPONIVEL.name,
                                choices=[(tag.name, tag.value) for tag in enums.StatusDispositivo], blank=False)
    obs = models.TextField(null=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.identificador, self.equipamento.descricao)

    def situacao_object(self):
        """ Enum de Situação """
        return enums.StatusDispositivo[self.situacao].alias

    def status_inventario_object(self):
        """ Situação do dispositivo no inventário """
        return self.status_inventario

    def valida_disponibilidade(self):
        """ Condição de Enum Disponível """
        situacao = self.situacao in [
            enums.StatusDispositivo.DISPONIVEL.name, 
            enums.StatusDispositivo.AVARIADO.name
        ]
        status_permite_circulacao = self.status_inventario and \
                                    self.status_inventario.permite_circular
        return situacao and status_permite_circulacao

    def equipamento_object(self):
        """ Equipamento do cadastro de Dispositivo """
        return self.equipamento

    def clean(self):
        if self.situacao in [
            enums.StatusDispositivo.EXTRAVIO.name,
            enums.StatusDispositivo.MANUTENCAO.name,
            enums.StatusDispositivo.AVARIADO.name
            ]:
            if not self.obs:
                raise ValidationError({
                    'obs': 'Necessário incluir uma observação para esta situação'})
        if self.situacao == None:
            raise ValidationError({ 'situacao': 'A situação é obrigatória' })

        """ 
            Verificar ao alterar para Disponível se o Dispositivo não está em circulação em 
            um ItemCirculacao 
        """
        try:
            # Obter o item original
            item = Dispositivo.objects.get(id=self.id)
            # comparar a situacao do item original com o item sendo alterado atualmente e checar se a alteração é para Disponível
            if item.situacao != self.situacao and self.situacao == enums.StatusDispositivo.DISPONIVEL.name:
                
                # se houver alteração na situação, verificar se existe itemcirculacao com 
                # situacao EM_CIRCULACAO em um empréstimo (ou seja, verificar se está em circulacao)
                # queryset para obter os itens circulacao
                item_em_circulacao_qs = item.itemcirculacao_set.filter(situacao=enums.StatusItemCirculacao.EM_CIRCULACAO.name)

                item_em_circulacao = item_em_circulacao_qs.exists()
                if item_em_circulacao:
                    # Se houver mais de 1 circulacao (provavelmente, pode ter ocorrido de uma circulação não ter dado baixa nas situacoes de itemcirculacao e Dispositivos)
                    # Caso aconteca a condição abaixo, debugar lógica de baixas
                    if item_em_circulacao_qs.count() > 1:
                        item_circs = (", ").join(item_em_circulacao_qs.values_list("circulacao__id", flat=True))
                        raise ValidationError({
                            'situacao': f'OPS! Item em várias circulação. Item encontrados nas seguintes empréstimos {item_circs}'})

                    # Obter a sala onde o item está em circulacao
                    sala = item_em_circulacao_qs.first().circulacao.local.descricao
                    raise ValidationError({'situacao': f'Dispositivo em circulação no local {sala}'})
                
        except Dispositivo.DoesNotExist as ex:
            pass
        
    def is_disponivel(self):
        # Recurso está disponível quando o próprio status é DISPONÍVEL e desde que 
        # ele não esteja como EM_CIRCULACAO
        disponivel = self.situacao == enums.StatusDispositivo.DISPONIVEL.name
        tem_pendencia =  self.entrega_itens.exclude(
            situacao__in=[
                enums.StatusItemCirculacao.BAIXADO_NORMAL.name, 
                enums.StatusItemCirculacao.DEVOLVIDO_AVARIA.name, 
                enums.StatusItemCirculacao.EXTRAVIADO.name
            ]).exists()
        return disponivel and tem_pendencia

    def get_disponivel_label(self):
        """ Legenda amigável """
        return 'Sim' if self.is_disponivel() else 'Não'
    
    def create_log(self, observacao='', created_by=None, circulacao=None):
        """ criação de logs via related_name """
        self.logdispositivo_set.create(
            dispositivo=self,
            circulacao=circulacao,
            situacao=self.situacao,
            obs=observacao,
            created_by=created_by
        )

    def set_dispositivo_manutencao(self, observacao, created_by):
        """ Alterar dispositivo para Manutenção """
        with transaction.atomic():
            if self.situacao == enums.StatusDispositivo.MANUTENCAO.name:
                raise ValidationError({'situacao': f'Dispositivo {self.identificador} já está como: {enums.StatusDispositivo.MANUTENCAO.value}'})

            self.situacao = enums.StatusDispositivo.MANUTENCAO.name
            self.obs = observacao
            self.save()

            self.create_log(observacao, created_by)
            self.clean()
            return self

    def set_dispositivo_extravio(self, observacao, created_by, circulacao=None):
        """ Alterar dispositivo para Extravio """
        with transaction.atomic():
            if self.situacao == enums.StatusDispositivo.EXTRAVIO.name:
                raise ValidationError({'situacao': f'Dispositivo já está como: {enums.StatusDispositivo.EXTRAVIO.value}'})

            self.situacao = enums.StatusDispositivo.EXTRAVIO.name
            self.obs = observacao
            self.save()

            self.create_log(observacao, created_by, circulacao)
            self.clean()
            return self

    def set_dispositivo_disponivel(self, obs, created_by, circulacao=None):
        """ Disponibiliza Dispositivo """
        with transaction.atomic():
            if self.itemcirculacao_set.filter(
                situacao = enums.StatusItemCirculacao.EM_CIRCULACAO.name
                ).exists():
                raise ValidationError({'situacao': f'Dispositivo ainda está como: {enums.StatusItemCirculacao.EM_CIRCULACAO.value}'})

            self.situacao = enums.StatusDispositivo.DISPONIVEL.name
            self.obs = obs
            self.save()
            self.create_log(obs, created_by, circulacao)
            self.clean()
            return self

    def set_dispositivo_circulacao(self, obs, created_by, circulacao=None):
        with transaction.atomic():
            if self.situacao == enums.StatusDispositivo.EM_CIRCULACAO.name:
                raise ValidationError({
                    'situacao': f'Dispositivo {self.identificador} já está como: {enums.StatusDispositivo.EM_CIRCULACAO.value}'})
            self.situacao = enums.StatusDispositivo.EM_CIRCULACAO.name
            self.obs = obs
            self.save()

            self.create_log(obs, created_by, circulacao)
            self.clean()
            return self

    def set_dispositivo_avaria(self, obs, created_by, circulacao=None):
        with transaction.atomic():
            if self.situacao == enums.StatusDispositivo.AVARIADO.name:
                raise ValidationError({
                    'situacao': f'Dispositivo já está como: {enums.StatusDispositivo.AVARIADO.value}'})
            self.situacao = enums.StatusDispositivo.AVARIADO.name
            self.obs = obs
            self.save()

            self.create_log(obs, created_by, circulacao)
            self.clean()
            return self

    class Meta:
        ordering = ('equipamento__descricao',)


class LogDispositivo(TimeStampedModel):
    updated_at = None
    updated_by = None
    circulacao = models.ForeignKey('Circulacao', on_delete=models.DO_NOTHING, blank=True, null=True)
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    situacao = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in enums.StatusDispositivo], blank=False, null=True)
    obs = models.TextField(null=True, blank=True)

    def situacao_object(self):
        return enums.StatusDispositivo[self.situacao].alias
    
    def circulacao_object(self):
        return self.circulacao
    
    def dispositivo_object(self):
        return self.dispositivo

    def responsavel(self):
        try:
            return self.circulacao.responsavel
        except:
            return ''

    def circulacao_id(self):
        try:
            return self.circulacao.id
        except:
            return ''

    def local(self):
        try:
            return self.circulacao.local.descricao
        except:
            return ''

    def __str__(self):
        return self.dispositivo.identificador

    class Meta:
        ordering = ('-created_at',)


class ItemCirculacao(TimeStampedModel):
    circulacao = models.ForeignKey('Circulacao', on_delete=models.CASCADE, blank=False, null=True)
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.PROTECT, blank=False, null=True)
    situacao = models.CharField(max_length=50, default=enums.StatusItemCirculacao.EM_CIRCULACAO.name,
                                choices=[(tag.name, tag.value) for tag in enums.StatusItemCirculacao], blank=False)
    obs = models.TextField(blank=True, null=True)
    devolvido_em = models.DateTimeField('devolvido em', auto_now_add=False, auto_now=False, null=True, blank=True)
    recebedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                  null=True, blank=True,
                                   related_name="%(app_label)s_%(class)s_recebedor_related",
                                   related_query_name="%(app_label)s_%(class)ss_recebedor", )

    def circulacao_id(self):
        return self.circulacao.id

    def recebedor_object(self):
        return self.recebedor

    def dispositivo_object(self):
        return self.dispositivo

    def situacao_object(self):
        return enums.StatusItemCirculacao[self.situacao].alias

    @classmethod
    def create(cls, *args, **kwargs):
        with transaction.atomic():
            item_emprestimo = cls(
                circulacao=kwargs.get('circulacao'),
                dispositivo=kwargs.get('dispositivo'),
                situacao=enums.StatusItemCirculacao.EM_CIRCULACAO.name,
                obs=kwargs.get('obs'),
                recebedor=None,
                devolvido_em=None,
                created_by=kwargs.get('created_by')
            )
            item_emprestimo.clean()
            item_emprestimo.save()

            item_emprestimo.dispositivo.set_dispositivo_circulacao(
                kwargs.get('obs'),
                kwargs.get('created_by'),
                kwargs.get('circulacao')
            )
            return item_emprestimo

    def __str__(self):
        return self.dispositivo.equipamento.descricao

    def clean(self):
        if self.situacao in [
                enums.StatusItemCirculacao.DEVOLVIDO_AVARIA.name,
                enums.StatusItemCirculacao.EXTRAVIADO.name]:
            if not self.obs:
                raise ValidationError({
                    'obs':'Necessário incluir uma observação para esta situação'})

        if self.situacao != enums.StatusItemCirculacao.EM_CIRCULACAO.name:
            if not self.devolvido_em:
                raise ValidationError({'devolvido_em':'Data de devolução não informada'})

        if self.situacao == None:
            raise ValidationError({'situacao':'A situação é obrigatória'})

        if self.circulacao == None:
            raise ValidationError({'circulacao':'Circulação não informada'})

        if self.dispositivo == None:
            raise ValidationError({'dispositivo':'Dispositivo não informado'})

    def auto_finalizar_circulacao(self, obs, recebedor):
        """ Auto finalizar quando não houver mais itens em circulacao """
        
        # se não existir mais nenhum item e a circulacao não estiver finalizada
        if (not self.circulacao.itens_em_circulacao().exists()) and \
            self.circulacao.situacao != enums.StatusCirculacao.FINALIZADO.name:

            circ = self.circulacao.set_circulacao_baixar(obs, recebedor, self.devolvido_em)
            self.circulacao.logcirculacao_set.create(
                circulacao=circ,
                situacao=circ.situacao,
                obs=circ.obs,
                created_by=circ.baixado_por
            )

    def set_item_circulacao_receber(self, obs, recebedor, devolvido_em):
        """ Disponibilizar dispositivo quando for recebido """
        with transaction.atomic():
            if self.situacao == enums.StatusItemCirculacao.BAIXADO_NORMAL.name:
                raise ValidationError({'situacao': f'Item já está como: {enums.StatusItemCirculacao.BAIXADO_NORMAL.value}'})
            
            self.situacao = enums.StatusItemCirculacao.BAIXADO_NORMAL.name
            self.recebedor = recebedor
            self.devolvido_em = devolvido_em
            self.obs = obs
            self.clean()
            self.save()

            self.dispositivo.set_dispositivo_disponivel(obs, recebedor, self.circulacao)
            self.auto_finalizar_circulacao(obs, recebedor)
            return self

    def set_item_circulacao_estornar(self, obs, usuario):
        """ Atualizar dispositivo quando o mesmo for estornado """
        with transaction.atomic():
            if self.circulacao.situacao == enums.StatusCirculacao.CANCELADO.name:
                raise ValidationError({'situacao': f'Não é possível estornar um item de uma circulação cancelada!'})
            
            if self.situacao == enums.StatusItemCirculacao.EM_CIRCULACAO.name:
                raise ValidationError({'situacao': f'Item {self.dispositivo.identificador} já está como: {enums.StatusItemCirculacao.EM_CIRCULACAO.value}'})
            
            if not self.dispositivo.situacao in [enums.StatusDispositivo.DISPONIVEL.name]:
                raise ValidationError({'dispositivo': f'Dispositivo {self.dispositivo.identificador} não está disponível para estorno. Situação atual é {str(self.dispositivo.situacao)}'})
            
            self.situacao = enums.StatusItemCirculacao.EM_CIRCULACAO.name
            self.obs = obs
            self.devolvido_em = None
            self.clean()
            self.save()
            
            self.dispositivo.set_dispositivo_circulacao(obs, usuario, self.circulacao)
            if self.circulacao.situacao == enums.StatusCirculacao.FINALIZADO.name:
                self.circulacao.set_circulacao_reabrir(obs, usuario)
            return self

    def set_item_circulacao_cancelar(self, obs, created_by):
        """ Atualizar dispositivo quando a circulação for cancelada """
        with transaction.atomic():
            if self.situacao == enums.StatusItemCirculacao.CIRCULACAO_CANCELADA.name:
                raise ValidationError({'situacao': f'Item já está como: {enums.StatusItemCirculacao.CIRCULACAO_CANCELADA.value}'})
            
            self.situacao = enums.StatusItemCirculacao.CIRCULACAO_CANCELADA.name
            self.obs = obs
            self.devolvido_em = datetime.now()
            self.clean()
            self.save()

            self.dispositivo.set_dispositivo_disponivel(obs, created_by, self.circulacao)
            self.auto_finalizar_circulacao(obs, created_by)
            return self
    
    def set_item_circulacao_avaria(self, obs, recebedor, devolvido_em):
        """ Atualizar dispositivo para status de avaria """
        with transaction.atomic():
            if self.situacao == enums.StatusItemCirculacao.DEVOLVIDO_AVARIA.name:
                raise ValidationError({'situacao': f'Item já está como: {enums.StatusItemCirculacao.DEVOLVIDO_AVARIA.value}'})
            
            self.situacao = enums.StatusItemCirculacao.DEVOLVIDO_AVARIA.name
            self.recebedor = recebedor
            self.devolvido_em = devolvido_em
            self.obs = obs
            self.clean()
            self.save()

            self.dispositivo.set_dispositivo_avaria(obs, recebedor, self.circulacao)
            self.auto_finalizar_circulacao(obs, recebedor)
            return self

    def set_item_circulacao_extravio(self, obs, recebedor, devolvido_em):
        """ Atualizar dispositivo para status de extravio """
        with transaction.atomic():
            if self.situacao == enums.StatusItemCirculacao.EXTRAVIADO.name:
                raise ValidationError({'situacao': f'Item já está como: {enums.StatusItemCirculacao.EXTRAVIADO.value}'})
            
            self.situacao = enums.StatusItemCirculacao.EXTRAVIADO.name
            self.recebedor = recebedor
            self.devolvido_em = devolvido_em
            self.obs = obs
            self.clean()
            self.save()

            self.dispositivo.set_dispositivo_extravio(obs, recebedor, self.circulacao)
            self.auto_finalizar_circulacao(obs, recebedor)
            return self

    def set_item_circulacao_em_circulacao(self, obs, created_by):
        """ Atualizar dispositivo quando em circulação """
        with transaction.atomic():

            self.situacao = enums.StatusItemCirculacao.EM_CIRCULACAO.name
            self.obs = obs
            self.clean()
            self.save()

            if not self.dispositivo.valida_disponibilidade():
                raise ValidationError({
                    'dispositivo': f'Dispositivo {self.dispositivo.identificador} não está disponível para circulação...'})
            self.dispositivo.set_dispositivo_circulacao(obs, created_by, self.circulacao)
            return self

    class Meta:
        verbose_name = 'Item de Circulação'
        verbose_name_plural = 'Itens de Circulação'
        ordering = ('-circulacao__created_at','circulacao__id', 'dispositivo__identificador')


class Circulacao(TimeStampedModel):
    local = models.ForeignKey(LocalUso, on_delete=models.PROTECT, blank=False, null=True)
    responsavel = models.CharField(max_length=255, null=True, blank=False, verbose_name="Responsável")
    email = models.CharField(max_length=255, null=True, blank=True, verbose_name="E-mail")
    previsao_devolucao = models.DateTimeField(auto_now_add=False, auto_now=False, verbose_name="Previsão Devolução")
    data_baixa = models.DateTimeField(auto_now_add=False, auto_now=False, verbose_name="Data de baixa", blank=True, null=True)
    situacao = models.CharField(max_length=50, default=enums.StatusCirculacao.ABERTO.name,
                                choices=[(tag.name, tag.value) for tag in enums.StatusCirculacao], blank=False)
    obs = models.TextField(blank=True, null=True)
    motivo_cancelamento = models.TextField(blank=True, null=True)
    baixado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True,
                                   related_name="%(app_label)s_%(class)s_baixado_related",
                                   related_query_name="%(app_label)s_%(class)ss_baixado_por", )

    @property
    def dict_read_only(self):
        # Dict de teste
        return {
            'id': self.id,
            'local': self.local.id,
            'local_object': {
                'id': self.local.id,
                'descricao': self.local.descricao
            },
            'item_objects': [
                {
                    'id': item.id,
                    'situacao': item.situacao,
                    'dispositivo_object': {
                        'identificador': item.dispositivo.identificador,
                        'equipamento_object': {
                            'id': item.dispositivo.equipamento.id,
                            'descricao':item.dispositivo.equipamento.descricao
                        },
                    },
                    'situacao_object': item.situacao_object(),
                    'created_by': {
                        'first_name': item.created_by.first_name if item.created_by else None,
                        'last_name': item.created_by.last_name if item.created_by else None
                    },
                    'updated_by': {
                        'first_name': item.updated_by.first_name if item.updated_by else None,
                        'last_name': item.updated_by.last_name if item.updated_by else None
                    },
                    'created_at': item.created_at,
                    'updated_at': item.updated_at,
                    'obs': item.obs
                }
                for item in self.itemcirculacao_set.all()
            ],
            'situacao_object': self.situacao_object(),
            'created_by': {
                'first_name': self.created_by.first_name if self.created_by else None,
                'last_name': self.created_by.last_name if self.created_by else None
            },
            'updated_by': {
                'first_name': self.updated_by.first_name if self.updated_by else None,
                'last_name': self.updated_by.last_name if self.updated_by else None
            },
            'baixado_por': {
                'first_name': self.baixado_por.first_name if self.baixado_por else None,
                'last_name': self.baixado_por.last_name if self.baixado_por else None
            },
            'situacao': self.situacao,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'responsavel': self.responsavel,
            'email': self.email,
            'previsao_devolucao': self.previsao_devolucao,
            'data_baixa': self.data_baixa,
            'obs': self.obs,
            'motivo_cancelamento': self.motivo_cancelamento,
        }

    def baixado_por_object(self):
        return self.baixado_por

    def count_itens(self):
        return self.itens_em_circulacao().count()
    count_itens.short_description = 'Itens...'

    def local_object(self):
        return self.local

    def situacao_object(self):
        return enums.StatusCirculacao[self.situacao].alias

    def item_objects(self):
        itens =  self.itemcirculacao_set.all()
        return itens
    
    def clean(self):
        if not self.responsavel:
            raise ValidationError({'responsavel':'Responsável não informado!'})

        if not self.local:
            raise ValidationError({'local':'Local não informado!'})

        self.responsavel = (self.responsavel or '').upper()

        # Para itens cancelados
        if self.situacao in [enums.StatusCirculacao.CANCELADO.name]:
            if not self.motivo_cancelamento:
                raise ValidationError({
                    'motivo_cancelamento':'Para efetuar um cancelamento é necessário informar um motivo!'})

            if not self.data_baixa:
                # o cancelamento recebe a data now() automaticamente
                raise ValidationError({
                    'data_baixa':'Data de baixa não definida automaticamente!'})
        
        # Para itens Finalizados
        if self.situacao in [enums.StatusCirculacao.FINALIZADO.name]:
            if not self.data_baixa:
                raise ValidationError({'data_baixa':'Data de baixa não informada!'})
            
            if not self.baixado_por:
                raise ValidationError({
                    'baixado_por':'Usuário que efetivou a baixa não foi identificado!'})

        # Para itens Transferidos
        if self.situacao in [enums.StatusCirculacao.TRANSFERIDO.name]:
            if not self.previsao_devolucao:
                raise ValidationError({
                    'previsao_devolucao':'Nova previsão de devolução não informada!'})

    @classmethod
    def create(cls, *args, **kwargs):
        """ override de criação para Circulação """
        with transaction.atomic():
            itens_dispositivos = kwargs.pop('itens_dispositivos', [])
            local = kwargs.get('local')
            responsavel = kwargs.get('responsavel')
            email = kwargs.get('email')
            obs = kwargs.get('obs')
            previsao_devolucao = kwargs.get('previsao_devolucao')
            created_by = kwargs.get('created_by')
            circulacao = cls(
                local=local,
                responsavel=responsavel,
                email=email,
                obs=obs,
                previsao_devolucao=previsao_devolucao,
                created_by=created_by
            )
            circulacao.clean()
            circulacao.save()

            # Valida se já existe uma circulacao no local selecionado
            existe_circulacao_no_local = Circulacao.objects \
                                    .filter(local=local, situacao=enums.StatusCirculacao.ABERTO.name) \
                                    .exclude(id=circulacao.id) \
                                    .exists()
            if existe_circulacao_no_local:
                raise ValidationError({'local': f'Já existe uma circulação no local informado!'})

            for d in itens_dispositivos:
                # criar instancias de ItemCirculacao para vincular à circulacao
                try:
                    dispositivo = Dispositivo.objects.get(id = d)
                    if not dispositivo.valida_disponibilidade():
                        raise ValidationError({
                            'itens': f'Dispositivo {dispositivo.identificador} não está disponível para circulação!'})
                    # filtrar apenas dispositivos Disponíveis
                    item = ItemCirculacao.objects.create(
                        circulacao=circulacao,
                        dispositivo=dispositivo,
                        created_by=kwargs.get('created_by')
                    )
                except Dispositivo.DoesNotExist as ex:
                    raise ValidationError({'itens': f'Dispositivo {str(d)} não encontrado!'})
                # Atualizar situacao
                item.set_item_circulacao_em_circulacao(obs='', created_by=kwargs.get('created_by'))

            circulacao.logcirculacao_set.create(
                circulacao=circulacao,
                situacao=enums.StatusCirculacao.ABERTO.name,
                obs='',
                created_by=kwargs.get('created_by')
            )
            
        return circulacao

    def __str__(self):
        return f'{ self.local}'
    
    def itens_em_circulacao(self):
        itens =  self.itemcirculacao_set.filter(situacao = enums.StatusItemCirculacao.EM_CIRCULACAO.name)
        return itens
    
    def set_circulacao_baixar(self, obs, baixado_por, data_baixa):
        with transaction.atomic():

            if self.situacao == enums.StatusCirculacao.FINALIZADO.name:
                raise ValidationError({'situacao': f'Circulação já está como: {enums.StatusCirculacao.FINALIZADO.value}'})
            
            for i in self.itens_em_circulacao():
                i.set_item_circulacao_receber(obs, baixado_por, data_baixa)

            if self.itens_em_circulacao().exists():
                raise ValidationError({'itens':'Ainda existem itens não baixados'})
            
            self.situacao = enums.StatusCirculacao.FINALIZADO.name
            self.data_baixa = data_baixa
            self.baixado_por = baixado_por
            self.updated_by = baixado_por
            self.obs = obs
            self.clean()
            self.save()

            return self

    def set_circulacao_cancelar(self, motivo, baixado_por):
        with transaction.atomic():
            if self.situacao == enums.StatusCirculacao.CANCELADO.name:
                raise ValidationError({'situacao': f'Circulação já está como: {enums.StatusCirculacao.CANCELADO.value}'})
            for i in self.itens_em_circulacao():
                i.set_item_circulacao_cancelar('Circulação cancelada por motivo: \"%s\"' % motivo, baixado_por)
            self.situacao = enums.StatusCirculacao.CANCELADO.name
            self.baixado_por = baixado_por
            self.updated_by = baixado_por
            self.motivo_cancelamento = motivo
            self.obs = ", ".join(list(filter(lambda x: not x in [None, ''],[self.obs, motivo])))
            self.data_baixa = datetime.now()
            self.clean()
            self.save()

            self.logcirculacao_set.create(
                circulacao=self,
                situacao=self.situacao,
                obs='Circulação cancelada por %s' % motivo,
                created_by=baixado_por
            )
            return self

    def set_circulacao_transferir(self, responsavel, email, previsao_devolucao, transferidor, local):
        with transaction.atomic():
            # não alterar status, continuar como aberto, utilizar TRANSFERIDO apenas no log da circulacao
            self.situacao = enums.StatusCirculacao.ABERTO.name
            obs = 'transferido de %s para %s. Transferência realizada por %s' % (
                                            self.responsavel, 
                                            responsavel, 
                                            transferidor
                                        )
            if self.responsavel == (responsavel or '').upper() or not responsavel:
                raise ValidationError({'responsavel': f'Tranferência não identificada pelo responsável!'})
            if not local:
                raise ValidationError({'local': f'Local não informado para transferência'})
                        
            self.responsavel = responsavel
            self.email = email
            self.previsao_devolucao = previsao_devolucao
            self.updated_by = transferidor
            self.obs = ", ".join(list(filter(lambda x: not x in [None, ''],[self.obs, ('Responsável %s atribuído' % responsavel)])))
            self.clean()
            self.save()
            self.logcirculacao_set.create(
                circulacao=self,
                situacao=enums.StatusCirculacao.TRANSFERIDO.name,
                obs=obs,
                created_by=transferidor
            )
            return self
    
    def set_circulacao_reabrir(self, obs, reaberto_por):
        with transaction.atomic():
            # não alterar status, continuar como aberto, utilizar TRANSFERIDO apenas no log da circulacao
            self.situacao = enums.StatusCirculacao.ABERTO.name
            obs = 'circulação reaberta por %s' % reaberto_por
            self.updated_by = reaberto_por
            self.obs = ", ".join(list(filter(lambda x: not x in [None, ''],[self.obs, obs])))
            self.clean()
            self.save()
            self.logcirculacao_set.create(
                circulacao=self,
                situacao=enums.StatusCirculacao.ABERTO.name,
                obs=obs,
                created_by=reaberto_por
            )
            return self
    
    class Meta:
        verbose_name = 'Circulação de Equipamento'
        ordering = ('-created_at',)


class LogCirculacao(TimeStampedModel):
    updated_at = None
    updated_by = None

    circulacao = models.ForeignKey(Circulacao, on_delete=models.CASCADE)
    situacao = models.CharField(max_length=50, choices=[(tag.name, tag.value) for tag in enums.StatusCirculacao], blank=False)
    obs = models.TextField(null=True, blank=True)

    def circulacao_object(self):
        return self.circulacao
    
    def situacao_object(self):
        return enums.StatusCirculacao[self.situacao].alias

    def circulacao_id(self):
        try: return self.circulacao.id
        except: return ''

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name="Log de Circulação"
        verbose_name_plural="Logs de Circulação"
        ordering = ('-created_at',)


