from django.db import models
from base.models import Arquivo, TimeStampedModel, TeamsChannel
from base.enums import *
from .enums import StatusReservaEnum
from users.models import User
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from itertools import count as itercount


class Configuracao(TimeStampedModel):
    descricao = models.CharField(max_length=100, default="Configuração padrão", null=True, blank=False, verbose_name="Descrição",
                                                unique=True, error_messages = { "unique": "Já existe uma configuração cadastrada com esta descrição!" })
    ignora_regras_admins = models.BooleanField(default=False, verbose_name= 'Ignora restrição de horários',
                                                help_text='Ignora as restrições(bloqueios) de intervalos de horários definidos em cada espaço para super usuários')
    ignora_choques_admins = models.BooleanField(default=False, verbose_name='Ignora choques de horários',
                                                help_text='Ignora choques de horários para super usuários definido no espaço de reserva')
    ignora_duracao_admins = models.BooleanField(default=False, verbose_name='Ignora duração da reserva',
                                                help_text='Ignora duração de uma reserva, para super usuários, definida no espaço para duração máxima e mínima')
    ignora_min_criacao_admins = models.BooleanField(default=False, verbose_name='Ignora carência mínima',
                                                help_text='Ignora o prazo mínimo para o registro de uma reserva, quando realizado por um super usuário')
    ignora_limite_abertura_admins = models.BooleanField(default=False, verbose_name='Ignora limite de abertura por usuário',
                                                help_text='Ignora parâmetros de limite de abertura de reserva para super usuários')
    ignora_params_espaco_admins = models.BooleanField(default=False, verbose_name='Ignora parâmetros de espaço',
                                                help_text='Ignora parâmetros de espaço, para super usuários, definidos para criação de reservas ao sábados e domingos')
    dias_retroativos = models.PositiveIntegerField(default=0, blank=False, null=True, verbose_name="Dias retroativos",
                                                help_text="Dias retroativos para exibição das reservas anteriores ao dia atual, no calendário.")
    sistema_liberado = models.BooleanField(default=False, verbose_name='Sistema ativo',
                                                help_text='Habilita o sistema e permite o registro de novas reservas')

    def clean(self):
        config = Configuracao.objects.exclude(id=self.id).count()
        if config > 0:
            raise ValidationError("Já existe uma configuração registrada no sistema!")

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Configuração'
        verbose_name_plural = 'Configurações'


class Finalidade(TimeStampedModel):
    descricao = models.CharField(max_length=200, blank=False, unique=True, null=True, verbose_name='Finalidade',
                    error_messages = { "unique": "Já existe uma finalidade cadastrada com a descrição informada!" })
    
    def __str__(self):
        return f'{self.descricao}'

    class Meta:
        ordering = ('descricao',)


class TipoEspaco(TimeStampedModel):
    descricao = models.CharField(max_length=200, blank=False, unique=True, null=True, verbose_name='Tipo',
                error_messages = { "unique": "Já existe um tipo de espaço com a descrição informada!" })

    def __str__(self):
        return f'{self.descricao}'

    class Meta:
        verbose_name = 'Tipo de Espaço'
        verbose_name_plural = 'Tipos de Espaços'
        ordering = ('descricao',)


class Regra(TimeStampedModel):
    WEEK_DAYS = [ (i.value,n.value) for i, n in zip(DayOfWeekIndexEnum, DayOfWeekNameEnum)]
    week_day = models.PositiveIntegerField(choices=WEEK_DAYS, blank=False, null=True, verbose_name="Dia da Semana")
    start_time = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='Horário inicial', null=True, blank=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='Horário final', null=True, blank=False)

    def __str__(self):
        return f'{self.week_day_name} | {self.start_time} - {self.end_time}'
    
    @property
    def legenda(self):
        return f'{self.week_day_name} das {self.start_time} às {self.end_time}'
    
    def weekday_enums(self):
        return [
            {
                'weekday_index': i.value,
                'weekday_name': n.value 
            } 
            for i, n in zip(DayOfWeekIndexEnum, DayOfWeekNameEnum)
        ]

    @property
    def week_day_name(self):
        wd = [ i.name for i in DayOfWeekIndexEnum ]
        return DayOfWeekNameEnum[wd[self.week_day]].value

    def save(self, *args, **kwargs):
        super(Regra, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('week_day', 'start_time', 'end_time')
        ordering = ('week_day',)


class Espaco(TimeStampedModel):
    descricao = models.CharField(max_length=250, null=True, unique=True, blank=False, verbose_name='Descrição',
                                        error_messages = { "unique": "Já existe um Espaço cadastrada com este nome!" })
    color = models.CharField(max_length=20, blank=True, null=True, default='#a7abeb', verbose_name='Cor')
    regras = models.ManyToManyField(Regra, verbose_name='Regras', blank=True,
                                        help_text='Parametrização de horários para este espaço')
    gestores = models.ManyToManyField(User, blank=False, verbose_name='Gestores do espaço', related_name='gestor_espaco_users')
    admins = models.ManyToManyField(User, blank=True, verbose_name='Super usuários do espaço', related_name='admin_users',
                                        help_text='Para estes usuários, serão ignoradas todas as restrições, exceto choques de horário!')
    teams = models.ManyToManyField(TeamsChannel, blank=True, verbose_name='Integrar Canal Teams',
                                        help_text='Selecionar canais do Teams para disparo de notificação')
    tipo_espaco = models.ForeignKey(TipoEspaco, on_delete=models.PROTECT, null=True, blank=False, verbose_name='Tipo do espaço')
    # Duração de agenda por espaço
    max_duracao = models.IntegerField(default=240, verbose_name='Duração máxima (minutos)',
                                        help_text="Duração máxima de um evento (horas)", null=True, blank=False)
    min_duracao = models.IntegerField(default=30, verbose_name='Duração mínima (minutos)',
                                        help_text="Duração mínima de um evento (horas)", null=True, blank=False)
    min_criacao = models.IntegerField(default=24, verbose_name='Carência de abertura (horas)',
                                        help_text="Prazo mínimo para registrar uma agenda (horas)", null=True, blank=False)
    permite_criar_sabados = models.BooleanField(default=False, blank=True, verbose_name='Permitir registrar eventos aos Sábados')
    permite_reservar_sabado = models.BooleanField(default=False, blank=True, verbose_name='Permite reservar para dia de Sábado')
    considera_sabado_util = models.BooleanField(default=False, blank=True, verbose_name='Considera Sábado um dia útil',
                                        help_text='Considera o Sábado como sendo um dia útil para o cálculo de carência mínima para abertura de reserva. O período de carência incluirá apenas os dias úteis.')
    permite_criar_domingos = models.BooleanField(default=False, blank=True, verbose_name='Permitir registrar eventos aos Domingos')
    permite_reservar_domingo = models.BooleanField(default=False, blank=True, verbose_name='Permitir reservar para dia de Domingo')
    ativo = models.BooleanField(default=False, blank=True, verbose_name='Espaço ativo')
    instrucoes_espaco = models.TextField(max_length=5000, blank=True, null=True, verbose_name="Orientações do espaço")
    requer_aprovacao = models.BooleanField(default=True, verbose_name='Requer aprovação',
                                        help_text='Eventos ficam pendentes até a aprovação')
    limitar_abertura = models.BooleanField(default=False, verbose_name='Limitar Abertura de Reserva',
                                        help_text='Define se haverá limitação de abertura de reservas por um mesmo usuário. Requer campo QUANTIDADE LIMITE DE ABERTURA. Esta quantidade de reservas é baseada na contagem de reservas com status Abertos e Pendentes')
    enviar_notificacao = models.BooleanField(default=True, verbose_name='Enviar notificação por e-mail',
                                        help_text='Habilita o envio de e-mail quando as reservas são criadas, aprovadas ou canceladas')
    limitar_abertura_qtde = models.PositiveIntegerField(default=1, verbose_name='Quantidade Limite de abertura',
                                        help_text='Definie a quantidade máxima de reservas Abertas e/ou Pendentes solicitados por um mesmo usuário. Requer campo LIMITAR ABERTURA DE RESERVA. Esta quantidade de reservas é baseada na contagem de reservas com status Abertos e Pendentes')
    
    def __str__(self):
        return f'{self.descricao} ({self.tipo_espaco.descricao})'
    
    def alias(self):
        return f'abrir' # exibir na listagem do django admin
    
    def gestores_objects(self):
        # retorna lista de objetos gestores para preservar o campo serializer gestores (pk`s)
        return self.gestores.all()
    
    def admins_objects(self):
        # retorna lista de objetos admins para preservar o campo serializer admins (pk`s)
        return self.admins.all()
    
    def regras_objects(self):
        # retorna lista de objetos admins para preservar o campo serializer admins (pk`s)
        return self.regras.all()
    
    def tipo_espaco_object(self):
        return self.tipo_espaco
    
    def count_admins(self):
        return self.admins.count()
    count_admins.short_description="Admins"
    
    @property
    def _color(self):
        try:
            return format_html(f'<div style="width:15px;height:15px;border-radius:50%;background-color:{self.color}"></div>')
        except:
            return ''
    
    class Meta:
        verbose_name='Espaço'
        verbose_name_plural='Espaços'
        ordering = ('descricao',)
        permissions = (
            ('can_gerenciar_espaco', 'Pode gerenciar espaços'),
        )


class Reserva(TimeStampedModel):
    arquivos = models.ManyToManyField(Arquivo, verbose_name='Anexos', blank=True )
    responsavel = models.CharField(max_length=250, verbose_name='Responsável', blank=False, null=True)
    espaco = models.ForeignKey(Espaco, on_delete=models.PROTECT, null=True, blank=False, verbose_name='Espaço')
    finalidade = models.ForeignKey(Finalidade, on_delete=models.PROTECT, null=True, blank=False, verbose_name='Finalidade')
    date = models.DateField(auto_now_add=False, auto_now=False, verbose_name='Data', blank=False, null=True)
    start = models.TimeField(auto_now_add=False, auto_now=False, verbose_name='Início', blank=False, null=True)
    end = models.TimeField(auto_now_add=False, auto_now=False, verbose_name='Fim', blank=False, null=True)
    titulo = models.CharField(max_length=250, verbose_name='Título da agenda', blank=True, null=True)
    participantes = models.PositiveIntegerField(verbose_name='Qtde pessoas', blank=True, null=True, default=0)
    # Padrão de status de reserva é Aberto, para espaços com "requer_aprovacao" ativo, altera para PENDING
    status_reserva = models.CharField(max_length=50, default=StatusReservaEnum.OPENED.name, 
                                choices=[(s.name, s.value) for s in StatusReservaEnum], verbose_name='Status')
    status_descricao = models.TextField(verbose_name='Ressalva de status', blank=True, null=True)
    observacao = models.TextField(verbose_name='Observações', blank=True, null=True)

    def __str__(self):
        return f'{self.espaco} - {self.date_start_end}'
    
    def arquivos_objects(self):
        return self.arquivos.all()

    def finalidade_object(self):
        return self.finalidade

    def espaco_object(self):
        return self.espaco

    def get_status(self):
        try:
            return StatusReservaEnum[self.status_reserva].value
        except:
            return 'Status desconhecido'
    get_status.short_description = 'Status'
    
    @property
    def status_color_classname(self):
        cor = 'grey'
        if self.status_reserva == StatusReservaEnum.OPENED.name:
            cor = 'success'
        if self.status_reserva == StatusReservaEnum.PENDING.name:
            cor = 'warning'
        if self.status_reserva == StatusReservaEnum.CANCELLED.name:
            cor = 'error'
        return cor
    
    @property
    def status_color_hexadecimal(self):
        cor = '#ddd'
        if self.status_reserva == StatusReservaEnum.OPENED.name:
            cor = '#4caf50'
        if self.status_reserva == StatusReservaEnum.PENDING.name:
            cor = '#fb8c00'
        if self.status_reserva == StatusReservaEnum.CANCELLED.name:
            cor = '#ff5252'
        return cor
    
    def get_status_html(self):
        cor = self.status_color_hexadecimal

        return format_html(f'<div style="width:10px;height:10px;border-radius:50%;background-color:{cor};display: -webkit-inline-box;"></div> {StatusReservaEnum[self.status_reserva].value}')
    get_status_html.short_description = 'Status'
    
    @property
    def date_start_end(self):
        date = self.date
        if type(date) == str:
            date = datetime.strptime(date, FormatDateStringsEnum.DEFAULT_DB_FORMAT_DATE.value).date()
        date = date.strftime(FormatDateStringsEnum.DEFAULT_BR_FORMAT_DATE.value)
        return f'{date} {self.start} - {self.end}'

    @property
    def start_time(self):
        #date = datetime.strptime(self.date, FormatDateStringsEnum.DEFAULT_DB_FORMAT_DATE.value).date()
        st = f'{self.date.strftime(FormatDateStringsEnum.DEFAULT_BR_FORMAT_DATE.value)} {self.start.strftime(FormatDateStringsEnum.DEFAULT_FORMAT_TIME.value)}'
        return st

    @property
    def end_time(self):
        et = f'{self.date.strftime(FormatDateStringsEnum.DEFAULT_BR_FORMAT_DATE.value)} {self.end.strftime(FormatDateStringsEnum.DEFAULT_FORMAT_TIME.value)}'
        return et
    
    @property
    def status_andamento(self):
        try:
            format_db = FormatDateStringsEnum.DEFAULT_DB_FORMAT_DATETIME.value
            if datetime.strptime(f'{self.date} {self.start}', format_db) < datetime.now() \
                    and datetime.strptime(f'{self.date} {self.end}', format_db) > datetime.now():
                return 'Em andamento'
            elif datetime.strptime(f'{self.date} {self.end}', format_db) < datetime.now():
                return 'Finalizado'
            else:
                return 'Em breve'
        except Exception as e:
            return '--'

    def get_mail_gestores(self):
        cc = [ m.email for m in self.espaco.gestores.all() ]
        return cc

#     def delete_attachments(self):
#         self.arquivos.all().delete()
    def validate_superusers(self):
        return self.created_by in self.espaco.admins.all()

    def validate_gestores(self):
        return self.created_by in self.espaco.gestores.all()

    def validate_parametros_espaco(self):
        # ATIVO/INATIVO
        if not self.espaco.ativo:
            # self.delete_attachments()
            raise ValidationError({'espaco': 'Espaço inativo no momento!'})
        
        config = self.validate_configuracao()
        is_super = self.validate_superusers()
        if is_super and config.ignora_params_espaco_admins: return

        # Permite Gestores "burlar regras de carência"
        is_gestor = self.validate_gestores()
        if is_gestor and True: return #config.ignora_min_criacao_admins: return

        # VALIDA CRIACAO AOS SÁBADOS
        today = datetime.now().weekday()
        if not self.espaco.permite_criar_sabados:# and not self.espaco.ignora_criar_sabados:
            if today == DayOfWeekIndexEnum.SAT.value:
                raise ValidationError({'created_at': 'Hoje(SÁBADO), não é permitido registrar reserva para este espaço!'})

        # VALIDA CRIACAO AOS DOMINGOS
        if not self.espaco.permite_criar_domingos:# and not self.espaco.ignora_criar_domingos:
            if today == DayOfWeekIndexEnum.SUN.value:
                raise ValidationError({'created_at': 'Hoje(DOMINGO), não é permitido registrar reservas para este espaço!'})
        
    def validate_limite_reservas(self):
        config = self.validate_configuracao()
        is_super = self.validate_superusers()
        if is_super and config.ignora_limite_abertura_admins: return

        # Permite Gestores "burlar regras de carência"
        is_gestor = self.validate_gestores()
        if is_gestor and True: return #config.ignora_min_criacao_admins: return

        count_by_user = Reserva.objects \
            .exclude(status_reserva__in=[StatusReservaEnum.CANCELLED.name])\
            .filter(espaco=self.espaco) \
            .filter(created_by=self.created_by) \
            .filter(date__gte=datetime.now()) \
            .count()
        if count_by_user < self.espaco.limitar_abertura_qtde or self.espaco.limitar_abertura_qtde == 0:
            # Se a quantidade de registros do usuário for menor que o limite do Espaço, parametrizado, então liberar nova
            return

        raise ValidationError({'espaco': 'Limite de %s reservas para o Espaço %s foi excedido!' % (str(self.espaco.limitar_abertura_qtde), str(self.espaco.descricao))})

    def validate_campos_obrigatorios(self):
        # VALIDA SE ESPACO FOI INFORMADO
        if not self.espaco:
            # self.delete_attachments()
            raise ValidationError({'espaco': 'Espaço não informado!'})
        
        # VALIDA SE RESPONSAVEL FOI INFORMADO
        if not self.responsavel:
            # self.delete_attachments()
            raise ValidationError({'responsavel': 'Nenhum responsável informado!'})

        # VALIDA SE FINALIDADE FOI INFORMADA
        if not self.finalidade:
            # self.delete_attachments()
            raise ValidationError({'finalidade': 'Finalidade não informada!'})

        # VALIDA SE DATA FOI INFORMADA
        if not self.date:
            # self.delete_attachments()
            raise ValidationError({'date': 'Data não informada!'})

        # VALIDA SE HORA INICIO FOI INFORMADA
        if not self.start:
            # self.delete_attachments()
            raise ValidationError({'start': 'Horário inicial não informado!'})

        # VALIDA SE HORA FIM FOI INFORMADA
        if not self.end:
            # self.delete_attachments()
            raise ValidationError({'end': 'Horário final não informado!'})

    def validate_regras(self, start_reserva, end_reserva):
        config = self.validate_configuracao()

        # Permite Gestores "burlar" regras de restrições
        is_gestor = self.validate_gestores()
        if is_gestor:
            return # fake regras para gestores

        is_super = self.validate_superusers()
        if is_super and config.ignora_regras_admins: 
            return # fake regras para admins

        regras = self.espaco.regras.filter( week_day=start_reserva.weekday() )
        ## Regra 1: Horário inicial da reserva não pode estar dentro de uma regra
        ## inicio <= start_reserva < fim 
        regra1 = regras.filter(
            models.Q(start_time__lte=start_reserva.time()), 
            models.Q(end_time__gt=start_reserva.time())
        )

        ## Regra 2: Horário final da reserva não pode estar dentro de ums regra
        ## inicio < fim_reserva <= fim 
        regra2 = regras \
            .exclude(pk__in=regra1.values('pk')) \
            .filter(
            models.Q(start_time__lt=end_reserva.time()), 
            models.Q(end_time__gte=end_reserva.time())
        )

        ## Regra 3: Regra dentro do intervalo da reserva
        ## inicio >= inicio_reserva and fim <= fim_reserva
        regra3 = regras \
            .exclude(pk__in=regra1.values('pk')) \
            .exclude(pk__in=regra2.values('pk')) \
            .filter(
                models.Q(start_time__gte=start_reserva.time()), 
                models.Q(end_time__lte=end_reserva.time())
            )
        conflitos = []
        if regra1.count() > 0: conflitos += [r.legenda for r in regra1.all()]
        if regra2.count() > 0: conflitos += [r.legenda for r in regra2.all()]
        if regra3.count() > 0: conflitos += [r.legenda for r in regra3.all()]
        # Aplicar o set() e list() para remover os índices repetidos
        conflitos = list(set(conflitos))

        if len(conflitos) > 0:
            raise ValidationError({'start': "Não é possível reservar o espaço para este horário. Há restrições para os seguintes horários: %s" % (", ".join(conflitos))})

    def validate_duracao(self, start_reserva, end_reserva):
        # VALIDATION FINAL TIME LESS THEN INITIAL
        if start_reserva >= end_reserva:
            # self.delete_attachments()
            raise ValidationError({'start': 'Hora final não pode ser menor ou igual à hora inicial' })
        
        config = self.validate_configuracao()
        is_super = self.validate_superusers()
        if is_super and config.ignora_duracao_admins: return

        # Permite Gestores "burlar" regras de duração
        is_gestor = self.validate_gestores()
        if is_gestor and True: return #config.ignora_min_criacao_admins: return
        
        # MAX DURATION PARAM
        if end_reserva > (start_reserva + timedelta(minutes=self.espaco.max_duracao)):
            # self.delete_attachments()
            raise ValidationError({'end': 'Duração máxima permitida é de %s!' % self.minutesToHour(self.espaco.max_duracao) })
    
        # MIN DURATION PARAM
        if end_reserva < (start_reserva + timedelta(minutes=self.espaco.min_duracao)):
            # self.delete_attachments()
            raise ValidationError({'end': 'Duração mínima permitida é de, pelo menos, %s!' % self.minutesToHour(self.espaco.min_duracao) })

    def validate_configuracao(self):
        config = Configuracao.objects.first()
        if not config:
            raise ValidationError({'config': 'Nenhuma configuração de reservas foi encontrada!'})
        
        if not config.sistema_liberado:
            raise ValidationError({'config': 'Sistema bloqueado para novas reservas!'})

        return config

    def validate_choque_horario(self, st, et):
        config = self.validate_configuracao()
        is_super = self.validate_superusers()
        if is_super and config.ignora_choques_admins: return

        detected_roles = []
        hasRestrict = False
        filtro_reservas = Reserva.objects.filter(
                models.Q(date=st),
                models.Q(espaco=self.espaco), 
                ~models.Q(pk=self.pk), 
                ~models.Q(status_reserva=StatusReservaEnum.CANCELLED.name) )
            
        for ev in filtro_reservas:
            # validar horário da reserva com todas as reservas do dia
            exist_event = self.validate_role_time(ev.start, ev.end, st.time(), et.time())
            if exist_event:
                hasRestrict = True
                detected_roles += ['Conflito no horário: %s - %s' % (str(ev.start), str(ev.end)) ]
            
        if hasRestrict:
            raise ValidationError({'espaco': 'Validação de Horários para o espaço %s. %s' % (self.espaco, ". ".join(detected_roles)) })
    
    def validate_carencia(self, start_reserva):
        if start_reserva < datetime.now():
            raise ValidationError({'date': "Reserva não pode ser inferior ao horário atual"})

        config = self.validate_configuracao()
        is_super = self.validate_superusers()
        if is_super and config.ignora_min_criacao_admins: return
        # Permite Gestores "burlar regras de carência"
        is_gestor = self.validate_gestores()
        if is_gestor and True: return #config.ignora_min_criacao_admins: return

        # WORKDAYS VALIDATION
        if self.espaco.min_criacao != 0:
            min_date_allowed = self.calcula_horas_uteis()
            if start_reserva < min_date_allowed:
                # self.delete_attachments()
                raise ValidationError({'date': 'Data e horário não podem ser inferior a %s horas úteis. Data mínima prevista: %s' % (self.espaco.min_criacao, min_date_allowed.strftime(FormatDateStringsEnum.DEFAULT_BR_FORMAT_DATETIME.value) )})
    
    def validate_reservar_sabado_domingo(self, st):
        # Permite Gestores "burlar"esta regra""
        is_gestor = self.validate_gestores()
        if is_gestor and True: return 

        if not self.espaco.permite_reservar_sabado:
            if st.weekday() in [DayOfWeekIndexEnum.SAT.value]:
                raise ValidationError({'date': 'Espaço não habilitado para reservar em dias de Sábado'})
        
        if not self.espaco.permite_reservar_domingo:
            if st.weekday() in [DayOfWeekIndexEnum.SUN.value]:
                raise ValidationError({'date': 'Espaço não habilitado para reservar em dias de Domingo'})

    def inicializa_status(self):
        # Status inicial para requer_aprovacao, quando habilitado
        # Se o usuário pertencer aos admins do Espaço
        if not self.status_reserva:
            if self.espaco.requer_aprovacao: # se requer aprovacao
                self.status_reserva = StatusReservaEnum.PENDING.name # criar como pendente
            else:
                self.status_reserva = StatusReservaEnum.OPENED.name # criar como aberto

    def set_uppercase(self):
        # SAVE UPPERCASE
        if self.responsavel: 
            self.responsavel = self.responsavel.upper()
        if self.titulo:
            self.titulo = self.titulo.upper()
        if self.status_descricao:
            self.status_descricao = self.status_descricao.upper()

    def set_cancelled(self):
        self.status_reserva = StatusReservaEnum.CANCELLED.name
        self.save()
    
    def set_opened(self):
        self.status_reserva = StatusReservaEnum.OPENED.name
        self.save()

    def clean(self):
        self.validate_limite_reservas()
        self.validate_campos_obrigatorios()
        self.validate_parametros_espaco()

        self.date = self.date.strftime(FormatDateStringsEnum.DEFAULT_DB_FORMAT_DATE.value)
        self.start = self.start.strftime(FormatDateStringsEnum.DEFAULT_FORMAT_TIME.value)
        self.end = self.end.strftime(FormatDateStringsEnum.DEFAULT_FORMAT_TIME.value)
        
        format_db = FormatDateStringsEnum.DEFAULT_DB_FORMAT_DATETIME.value
        st = datetime.strptime(f'{self.date} {self.start}:00', format_db)
        et = datetime.strptime(f'{self.date} {self.end}:00', format_db)
        
        # VALIDAR SABADO E DOMINGO
        self.validate_reservar_sabado_domingo(st)

        # VALIDATE CARENCIA (PRAZO MINIMO PARA ABERTURA)
        self.validate_carencia(st)

        # VALIDATE DURACAO
        self.validate_duracao(st, et)

        # DEFINE STATUS AO ABRIR RESERVA
        self.inicializa_status()
        
        # VALIDATE RESTRICOES
        self.validate_regras(st, et)
        
        # VALIDATE CONFLICT DATE/TIME EVENT
        self.validate_choque_horario(st, et)
        
        # DEFINIR MAIUSCULOS
        self.set_uppercase()
        
    def minutesToHour(self, minutes):
        tempo = str(timedelta(minutes=minutes))
        h, m, s = tempo.split(':')
        formato = '{:02d}h{:02d}m'.format(int(h), int(m))
        return formato
    
    def validate_role_time(self, regra_start, regra_end, start, end):
        ## inicio <= start_reserva < fim 
        regra1 = regra_start <= start < regra_end
        ## inicio < fim_reserva <= fim 
        regra2 = regra_start < end <= regra_end
        ## inicio >= inicio_reserva and fim <= fim_reserva
        regra3 = regra_start >= start and regra_end <= end
        # print(regra1, regra2, regra3)
        return regra1 or regra2 or regra3
    
    def calcula_horas_uteis(self):
        horas_carencia = self.espaco.min_criacao
        today = datetime.now()
        SAT, SUN = DayOfWeekIndexEnum.SAT.value, DayOfWeekIndexEnum.SUN.value
        fds = [SUN]

        # incluir SAT se não for considerado um dia util
        if not self.espaco.considera_sabado_util:
            fds += [SAT]
        
        sum_hours_from_now = 0
        totalIterations = 0
        for i in itercount(0):

            totalIterations += 1
            data = today + timedelta(hours= i + 1)

            if data.weekday() in fds:
                pass
            else:
                sum_hours_from_now += 1

            if sum_hours_from_now == horas_carencia:
                break

            if sum_hours_from_now >= 8760:
                # condição de segurança para itertools
                # 8760 = horas totais no intervalo de 1 ano
                break
        min_date = today + timedelta(hours=totalIterations)
        return min_date
        
    """
    def save(self, *args, **kwargs):
        #self.clean()
        #self.full_clean()
        return super().save(*args, **kwargs)
    """

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        permissions = (
            ('can_acessar_agendalabs', 'Pode acessar AgendaLabs'),
            ('can_aprovar_reserva', 'Pode aprovar uma reserva'),
            ('can_cancelar_reserva', 'Pode cancelar uma reserva'),
        )
        

class LogAgenda(models.Model):
    log = models.TextField(null=True, blank=False)
    log_at = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name='Registro do log', null=True, blank=False)
    log_type = models.CharField(max_length=100, default=LogTypeEnum.VIEW.name, choices=[(i.name, i.value) for i in LogTypeEnum], null=True, blank=False)
    log_app = models.CharField(max_length=100, default=AppEnum.BASE.name, choices=[(i.name, i.value) for i in AppEnum], null=True, blank=False)
    log_action = models.CharField(max_length=100, default=ActionEnum.VIEW.name, choices=[(i.name, i.value) for i in ActionEnum], null=True, blank=False)
    log_model = models.CharField(max_length=100, default='LogAgenda', null=True, blank=False)
    log_reserva = models.ForeignKey(Reserva, related_name="logs", on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        try:
            app = AppEnum[self.log_app].value
        except:
            app = self.log_app
        try:
            type_ = LogTypeEnum[self.log_type].value
        except:
            type_ = self.log_type

        return f'{app} - {type_} - {self.log_at} - {self.log_model} '
    
    def reserva_object(self):
        return self.log_reserva
