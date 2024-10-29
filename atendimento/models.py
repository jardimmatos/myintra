from django.db import models, transaction
from base.models import TimeStampedIDModel
from django.conf import settings
from . import enums
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from base.utils import call_ws


class Unidade(TimeStampedIDModel):
    nome = models.CharField(max_length=255, unique=True, null=True, blank=False)
    descricao = models.TextField(null=True, blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Local(TimeStampedIDModel):
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, null=True, blank=False)
    nome = models.CharField(max_length=255, null=True, blank=False)

    def __str__(self):
        return f"{self.unidade} - {self.nome}"
    
    class Meta:
        unique_together = ('unidade', 'nome')


class Prioridade(TimeStampedIDModel):
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, null=True, blank=False)
    nome = models.CharField(max_length=255, null=True, blank=False)
    peso = models.IntegerField(default=1, blank=False, null=True)

    def __str__(self):
        return f"{self.unidade} - {self.nome}"

    class Meta:
        unique_together = ('unidade', 'nome')


class Departamento(TimeStampedIDModel):
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, null=True, blank=False)
    nome = models.CharField(max_length=255, null=True, blank=False)
    descricao = models.TextField(null=True, blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.unidade} - {self.nome}"

    class Meta:
        unique_together = ('unidade', 'nome')


class Servico(TimeStampedIDModel):
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, null=True, blank=False)
    nome = models.CharField(max_length=255, null=True, blank=False)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=False)
    sigla = models.CharField(max_length=4, null=True, blank=False)
    descricao = models.TextField(null=True, blank=True)
    # peso = models.IntegerField(default=1, blank=False, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.unidade} - {self.nome}"

    def departamento_object(self):
        return self.departamento

    class Meta:
        unique_together = ('unidade', 'nome')


class Cliente(TimeStampedIDModel):
    matricula = models.CharField(max_length=20, null=True, blank=True)
    nome = models.CharField(max_length=255, null=True, blank=False)
    email = models.CharField(max_length=255, null=True, blank=True)
    celular = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nome


class Perfil(TimeStampedIDModel):
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, null=True, blank=False)
    nome = models.CharField(max_length=255, null=True, blank=False)
    descricao = models.TextField(null=True, blank=True)
    pode_atender = models.BooleanField(default=False)
    acessa_triagem = models.BooleanField(default=False)
    acessa_painel = models.BooleanField(default=False)
    # pode_configurar = models.BooleanField(default=False)
    # acessa_monitor = models.BooleanField(default=False)
    # gera_relatorios = models.BooleanField(default=False)
    # gerencia_atendentes = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.unidade} - {self.nome}"

    class Meta:
        unique_together = ('unidade', 'nome')


class Atendente(TimeStampedIDModel):
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, null=True, blank=False)
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=False)
    local = models.ForeignKey(Local, on_delete=models.CASCADE, null=True, blank=False)
    numero_local = models.CharField(max_length=50, null=True, blank=False)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, null=True, blank=False)
    prioridade = models.ForeignKey(Prioridade, on_delete=models.PROTECT, null=True, blank=True, default=None)
    servicos = models.ManyToManyField(Servico, blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario}"
    
    def clean(self):
        if self.local and self.local.unidade != self.unidade:
            raise ValidationError({'local': "Unidade do Local é diferente da Unidade do Atendente!"})
        
        if self.prioridade and self.prioridade.unidade != self.unidade:
            raise ValidationError({'prioridade': "Unidade da Prioridade é diferente da Unidade do Atendente!"})
        
        if self.perfil and self.perfil.unidade != self.unidade:
            raise ValidationError({'perfil': "Unidade do Perfil é diferente da Unidade do Atendente!"})
    
    def unidade_object(self):
        return self.unidade
    
    def perfil_object(self):
        return self.perfil
    
    def usuario_object(self):
        return self.usuario
    
    def prioridade_object(self):
        return self.prioridade
    
    def local_object(self):
        return self.local

    def alterar_numero_local(self, args):
        if 'numero_local' in args:
            self.numero_local = args.get('numero_local')
        if 'prioridade' in args:
            try:
                self.prioridade = Prioridade.objects.get(pk=args.get('prioridade'))
            except Exception as ex:
                raise ValidationError(f"Prioridade não informada para o atendente!")

    def to_label_local(self):
        try: return self.local.nome
        except: return self.local
    to_label_local.short_description = 'Local'

    def to_label_perfil(self):
        try: return self.perfil.nome
        except: return self.perfil
    to_label_perfil.short_description = 'Perfil'

    def to_label_unidade(self):
        try: return self.unidade.nome
        except: return self.unidade
    to_label_unidade.short_description = 'Unidade'

class PainelSenha(TimeStampedIDModel):
    # Manter registros no histórico de senhas chamadas para o painel
    atendimento = models.OneToOneField('Atendimento', on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        return f'{self.atendimento}'
    
    def atendimento_object(self):
        return self.atendimento

    def ref_atendimento(self):
        return self.atendimento.id

    def chamar_senha_painel(self):
        # Valida se o status do atendimento é Chamado(status_atendimento alterado antes de ser chamado no painel)
        self.atendimento.target_before_status_validation([enums.StatusAtendimento.chamado.name])

        unidade_id = self.atendimento.unidade.id
        historicos = PainelSenha.objects \
                        .filter(atendimento__unidade__id=unidade_id) \
                        .filter(created_at__gte=(datetime.now()-timedelta(days=1))) \
                        .exclude(pk=self.pk) \
                        .order_by('-created_at')
        historicos = [{
            'sigla_senha': h.atendimento.sigla_senha,
            'local': f"{h.atendimento.atendente.local.nome} {h.atendimento.atendente.numero_local}",
            'prioridade': f"{h.atendimento.prioridade.nome}",
        } for h in historicos[:4]]
        obj = {
            'id':self.atendimento.id,
            'prioridade': self.atendimento.prioridade.nome,
            'sigla_senha': self.atendimento.sigla_senha,
            'atendente': self.atendimento.atendente.usuario.first_name,
            'servico': self.atendimento.servico.nome,
            'local': f"{self.atendimento.atendente.local.nome} {self.atendimento.atendente.numero_local}",
            'historico': historicos
        }
        call_ws(f'room_channel_painel_atendimento_{unidade_id}', '', 'CALL-TICKET', obj, notify=True)
        return obj

    def sigla_senha(self):
        return f"{self.atendimento.sigla_senha}"
        

class Atendimento(TimeStampedIDModel):
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, null=True, blank=False, verbose_name="Unidade de Atendimento", help_text="Unidade à qual o atendimento pertence")
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, null=True, blank=True, help_text="Cliente identificado para o Atendimento")
    prioridade = models.ForeignKey(Prioridade, on_delete=models.CASCADE, null=True, blank=False, help_text="Prioridade definida para o Atendimento")
    senha = models.IntegerField(null=True, blank=False, help_text="Sequência de senha do dia/serviço") # incremental pelo serviço do atendimento

    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, null=True, blank=False, verbose_name="Serviço", help_text="Serviço definido na triagem de senha. Se redirecionado, este serviço pode ser alterado")
    atendente_tri = models.ForeignKey(Atendente, on_delete=models.CASCADE, null=True, blank=False, related_name='atendimento_usuario_tri', verbose_name="Triagem", help_text="Usuário que realizou a triagem da senha")
    redirecionado_por = models.ForeignKey(Atendente, on_delete=models.CASCADE, null=True, blank=True, related_name='atendimento_redirecionado_por', verbose_name="Redirecionador", help_text="Usuário que realizou o redirecionamento para outro serviço")
    servico_original = models.ForeignKey(Servico, on_delete=models.CASCADE, null=True, blank=True, related_name='servico_original_atendimento',
                                            help_text="Serviço original definido antes de qualquer redirecionamento")

    data_chegada = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True, verbose_name="Chegada", help_text="Data/Hora definida no ato da triagem da senha")
    data_chamada = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True, verbose_name="Chamada", help_text="Data/Hora definida no ato da chamada de senha no Painel")
    data_inicio = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True, verbose_name="Início", help_text="Data/Hora definida no ato do início do atendimento")
    data_fim = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True, verbose_name="Encerramento", help_text="Data/Hora definida no ato do encerramento do atendimento")

    # Campos nulos no ato da triagem, preenchidos somente na chamada de senha
    atendente = models.ForeignKey(Atendente, on_delete=models.CASCADE, null=True, blank=True, related_name='atendimento_atendente', help_text="Atendente responsável pelo atendimento")
    local = models.ForeignKey(Local, on_delete=models.CASCADE, null=True, blank=True, help_text="Local de Atendimento parametrizado para o usuário atendente")

    # diferenca entre (data_chegada - data_chamada)
    tempo_espera = models.IntegerField(default=None, null=True, blank=True, verbose_name="Espera", help_text="Tempo de espera em segundos") # atualizar na chamada da senha

    # diferenca entre (data_chamada - data_inicio)
    tempo_deslocamento = models.IntegerField(default=None, null=True, blank=True, verbose_name="Deslocamento", help_text="Tempo entre a chamada de senha no painel e início do atendimento") # atualiza no início do atendimento

    # diferenca entre (data_inicio - data_fim)
    tempo_atendimento = models.IntegerField(default=None, null=True, blank=True, help_text="Tempo entre o início e o encerramento do atendimento") # atualiza no término do atendimento

    # soma do tempo total (tempo_espera + tempo_atendimento + tempo_deslocamento )
    tempo_permanencia = models.IntegerField(default=None, null=True, blank=True, verbose_name="Permanência", help_text="Tempo total desde a triagem de senha até o tempo de encerramento") # atualiza no término do atendimento

    avaliacao = models.IntegerField(default=None, null=True, blank=True, verbose_name="Nota", help_text="Nota de avaliação do atendimento") # Avaliação

    status_atendimento = models.CharField(max_length=50, default=enums.StatusAtendimento.emitido.name,
                                            choices=[(s.name, s.value) for s in enums.StatusAtendimento],
                                            null=True, blank=False, verbose_name="Status", help_text="Status atual do atendimento")
    sigla_senha = models.CharField(max_length=50, null=True, blank=False)
    resolucao = models.CharField(max_length=50, default=None, choices=[(r.name, r.value) for r in enums.ResolucaoAtendimento],
                                null=True, blank=True, verbose_name="Resolução", help_text="Estado de Resolução do atendimento")
    obs = models.TextField(null=True, blank=True, verbose_name="Observação", help_text="Informações adicionais sobre o atendimento além das observações comentadas")

    historico = models.BooleanField(default=False, verbose_name="Histórico", help_text="Os Atendimentos são definidos como históricos quando foram finalizados como encerrados ou não comparecidos do dia anterior. Para os demais atendimentos(do dia anterior), é necessário encerrá-los")

    def prioridade_object(self):
        return self.prioridade
    
    def unidade_object(self):
        return self.unidade
    
    def servico_object(self):
        return self.servico
    
    def cliente_object(self):
        return self.cliente
    
    def local_object(self):
        return self.local
    
    def seconds_to_hours(self, seconds):
        return str(datetime.fromtimestamp(seconds))[11:19]

    def tempo_espera_h(self):
        return self.tempo_espera

    def tempo_deslocamento_h(self):
        return self.tempo_deslocamento

    def tempo_atendimento_h(self):
        return self.tempo_atendimento

    def tempo_permanencia_h(self):
        return self.tempo_permanencia

    def __str__(self):
        return f"{self.unidade} - {self.prioridade} - {self.servico}"

    def cadastrar_cliente(self, args):
        if not 'cliente' in args: return None
        obj, create = Cliente.objects.get_or_create(matricula=args.get('cliente',{}).get('matricula'), defaults={
            'nome': args.get('cliente',{}).get('nome'),
            'email': args.get('cliente',{}).get('email'),
            'celular': args.get('cliente',{}).get('celular'),
        })
        return obj

    def triagem_senha(self, args):
        with transaction.atomic():
            self = Atendimento()
            self.status_atendimento = enums.StatusAtendimento.emitido.name
            self.data_chegada = datetime.now()

            self.cliente = self.cadastrar_cliente(args)

            if not 'unidade' in args: raise ValidationError("Unidade não informado!")
            try:
                self.unidade = Unidade.objects.get(pk=args.get('unidade'))
            except Exception as ex:
                raise ValidationError(f"Falha ao selecionar Unidade!")

            if not 'servico' in args: raise ValidationError("Serviço não informado!")
            try:
                self.servico = Servico.objects.get(pk=args.get('servico'))
                self.servico_original = Servico.objects.get(pk=args.get('servico'))
            except Exception as ex:
                raise ValidationError(f"Falha ao selecionar Serviço/Departamento!")

            if not 'prioridade' in args: raise ValidationError("Prioridade não informada!")
            try:
                self.prioridade = Prioridade.objects.get(pk=args.get('prioridade'))
            except Exception as ex:
                raise ValidationError(f"Falha ao selecionar prioridade!")
            
            self.sigla = self.servico.sigla
            
            if not 'atendente_tri' in args: raise ValidationError(f"Usuário de triagem Não informado!")
            try:
                self.atendente_tri = Atendente.objects.get(pk=args.get('atendente_tri'))
            except Exception as ex:
                raise ValidationError(f"Falha ao atribuir usuário na triagem de senha!")
            try:
                counter = Atendimento.objects.filter(
                        unidade__id=args.get('unidade'),
                        servico_original__id=args.get('servico'),
                        historico=False
                    ).last().senha + 1
            except:
                counter = 1
            self.senha = counter
            self.sigla_senha = f"{self.sigla}{self.senha:0>3}"
            self.save()

            return Atendimento.objects.get(id=self.id)
    
    def redirecionar_atendimento(self, args):
        """ args = { servico: servico_id } """
        # Atendimento precisar estar com um dos status antes desta ação
        self.target_before_status_validation([enums.StatusAtendimento.chamado.name, enums.StatusAtendimento.iniciado.name])
        """
        Atualiza campo redirecionado_por
        Atualiza campo servico
        Limpa atendente atual
        local atual
        Altera status para transferido
        Limpa data chamada
        Limpa Data inicio
        """
        with transaction.atomic():
            try:
                servico = Servico.objects.get(pk=args.get('servico'))
            except Servico.DoesNotExist: return ValidationError("Servico não encontrado!")

            
            self.redirecionado_por = self.atendente
            self.servico = servico
            self.atendente = None
            self.obs = args.get('obs') or self.obs
            self.local = None
            self.data_chamada = None
            self.data_inicio = None
            self.status_atendimento = enums.StatusAtendimento.transferido.name
            self.save()
        return Atendimento.objects.get(id=self.id)

    def proxima_senha(self, args):
        # Atendimento precisar estar com o status antes desta ação
        self.target_before_status_validation([enums.StatusAtendimento.emitido.name, enums.StatusAtendimento.transferido.name])

        # não limitar mais à data de chamada
        if not self.data_chamada or True:
            with transaction.atomic():
                if not 'atendente' in args: raise ValidationError("Atendente não informado!")
                self.status_atendimento = enums.StatusAtendimento.chamado.name
                self.data_chamada = datetime.now()
                self.atendente = args.get('atendente')
                self.local = self.atendente.local
                self.save()

                try:
                    # calcular tempo
                    at = Atendimento.objects.get(id=self.id)
                    diferenca_espera = (at.data_chamada - at.data_chegada)
                    at.tempo_espera = int(diferenca_espera.total_seconds())
                    at.save()
                except Exception as ex:
                    print(ex)
                    raise ValidationError(f"Falha ao calcular tempo de espera!")

                try:
                    # Disparar Senha
                    painel, created = PainelSenha.objects.get_or_create(atendimento=self)
                    if 'silent' in args:
                        pass # não chamar no painel
                    else:
                        painel.chamar_senha_painel()
                except Exception as ex:
                    print(ex)
                    raise ValidationError(f"Falha ao criar chamada de Painel!")
        return Atendimento.objects.get(id=self.id)

    def iniciar_atendimento(self):
        if self.status_atendimento == enums.StatusAtendimento.iniciado.name:
            raise ValidationError(f"Atendimento já foi iniciado!")

        # Atendimento precisar estar com o status antes desta ação
        self.target_before_status_validation([enums.StatusAtendimento.chamado.name])

        self.data_inicio = datetime.now()
        self.status_atendimento = enums.StatusAtendimento.iniciado.name
        self.save()

        # calcular tempo
        at = Atendimento.objects.get(id=self.id)
        diferenca_deslocamento = (at.data_inicio - at.data_chamada)
        at.tempo_deslocamento = int(diferenca_deslocamento.total_seconds())
        at.save()

        return Atendimento.objects.get(id=self.id)

    def encerrar_atendimento(self, args):
        if self.status_atendimento == enums.StatusAtendimento.encerrado.name:
            raise ValidationError(f"Atendimento já foi encerrado!")
        # Atendimento precisar estar com o status antes desta ação
        self.target_before_status_validation([enums.StatusAtendimento.iniciado.name])

        self.data_fim = datetime.now()
        self.status_atendimento = enums.StatusAtendimento.encerrado.name
        if 'resolucao' in args:
            self.resolucao = enums.ResolucaoAtendimento[args.get('resolucao')].name
        else:
            raise ValidationError(f"Resolução não informada para o atendimento!")

        if 'obs' in args:
            self.obs = args.get('obs')
        self.save()

        # calcula tempo
        at = Atendimento.objects.get(id=self.id)
        diferenca_atendimento = (at.data_fim - at.data_inicio)
        at.tempo_atendimento = int(diferenca_atendimento.total_seconds())
        at.tempo_permanencia = at.tempo_espera + at.tempo_atendimento + at.tempo_deslocamento
        at.save()

        return Atendimento.objects.get(id=self.id)

    def nao_compareceu_atendimento(self):
        # if self.status_atendimento == enums.StatusAtendimento.nao_compareceu.name:
        #     raise ValidationError(f"Atendimento já foi encerrado!")
        # Atendimento precisar estar com o status antes desta ação
        self.target_before_status_validation([enums.StatusAtendimento.chamado.name])

        self.data_inicio = datetime.now()
        self.data_fim = self.data_inicio
        self.status_atendimento = enums.StatusAtendimento.nao_compareceu.name
        self.save()

        # calcula tempo
        at = Atendimento.objects.get(id=self.id)
        diferenca_espera = (at.data_chamada - at.data_chegada)
        at.tempo_espera = int(diferenca_espera.total_seconds())
        diferenca_deslocamento = (at.data_inicio - at.data_chamada)
        at.tempo_deslocamento = int(diferenca_deslocamento.total_seconds())
        at.tempo_atendimento = 0
        at.tempo_permanencia = at.tempo_espera + at.tempo_atendimento + at.tempo_deslocamento
        at.save()

        return Atendimento.objects.get(id=self.id)

    def avaliar_atendimento(self, args):
        # Atendimento precisar estar com o status antes desta ação
        self.target_before_status_validation([enums.StatusAtendimento.encerrado.name])
        if self.avaliacao:
            return #raise ValidationError(f"Atendimento já foi avaliado!")

        if 'nota' in args and int(args.get('nota')) in range(1,11):
            self.avaliacao = int(args.get('nota'))
        else:
            raise ValidationError(f"Nota inválida!")

        self.save()

        # return Atendimento.objects.get(id=self.id)

    def target_before_status_validation(self, target_before=[]):
        """ Valida qual o status anterior é necessário para o atendimento precisar prosseguir com o fluxo """
        if self.status_atendimento in target_before:
            return True # OK
        elif self.status_atendimento == enums.StatusAtendimento.emitido.name:
            raise ValidationError("Senha do atendimento precisar ser chamado")
        elif self.status_atendimento == enums.StatusAtendimento.chamado.name:
            raise ValidationError("Atendimento foi chamado. Atendimento precisar ser Iniciado ou definido como \"Não compareceu\"")
        # elif self.status_atendimento == enums.StatusAtendimento.transferido.name:
        #     raise ValidationError("Atendimento foi transferido. Atendimento precisar ser Iniciado ou definido como \"Não compareceu\"")
        elif self.status_atendimento == enums.StatusAtendimento.iniciado.name:
            raise ValidationError("Senha do atendimento precisar ser encerrado!")
        elif self.status_atendimento in enums.StatusAtendimento.encerrado.name:
            raise ValidationError("Atendimento já foi encerrado!")
        elif self.status_atendimento in enums.StatusAtendimento.nao_compareceu.name:
            raise ValidationError("Cliente não compareceu ao atendimento!")
        raise ValidationError("Nenhum target identificado")
    
    def senhas_por_servicos_do_atendente(self, unidade_id, atendente_id):
        atendente = Atendente.objects.get(pk=atendente_id)
        atendimentos = Atendimento.objects \
            .filter(unidade=unidade_id) \
            .filter(servico__id__in=atendente.servicos.values_list('id', flat=True))
        return atendimentos

    def to_label_prioridade(self):
        try: return self.prioridade.nome
        except: return self.prioridade
    to_label_prioridade.short_description = 'Prioridade'

    def to_label_servico(self):
        try: return self.servico.nome
        except: return self.servico
    to_label_servico.short_description = 'Serviço'

    def to_label_local(self):
        try: return self.local.nome
        except: return self.local
    to_label_local.short_description = 'Local'

    def to_label_atendente(self):
        try: return self.atendente.usuario.username
        except: return self.atendente
    to_label_atendente.short_description = 'Atendente'


class AtendimentoComentario(TimeStampedIDModel):
    atendimento = models.ForeignKey(Atendimento, on_delete=models.CASCADE, blank=False, null=True)
    comentario = models.TextField(max_length=5000)

    def __str__(self):
        return f'{self.atendimento} - {self.comentario}'

    def created_by_object(self):
        return self.created_by

    def updated_by_object(self):
        return self.updated_by

    class Meta:
        verbose_name = "Comentário de Atendimento"
        verbose_name_plural = "Comentários de Atendimento"
        ordering = ('-created_at',)

