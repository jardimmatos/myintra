import datetime
from django.utils import timezone
from django.test import TestCase
from . import models as models_agenda
from base import models as models_base
from users import models as models_user
from agenda.enums import *
from base.enums import *
from django.core.exceptions import ValidationError


class AgendamentoTestCase(TestCase):

    def setUp(self):

        self.configuracao = models_agenda.Configuracao.objects.create(
            descricao='Config',
            ignora_regras_admins=True,
            ignora_choques_admins=True,
            ignora_duracao_admins=True,
            ignora_min_criacao_admins=True,
            ignora_limite_abertura_admins=True,
            ignora_params_espaco_admins=True,
            dias_retroativos=180,
            sistema_liberado=True
        )

        self.regra = models_agenda.Regra.objects.create(
            week_day=DayOfWeekIndexEnum.MON.value,
            start_time='08:00',
            end_time='12:00',
        )
        self.gestor = models_user.User.objects.create(
            username='user',
            email='mail@mail.com',
            is_active = True,
        )
        self.tipo_espaco = models_agenda.TipoEspaco.objects.create(
            descricao = 'Aula',
        )
        self.finalidade = models_agenda.Finalidade.objects.create(
            descricao = 'Aula Prática',
        )
        self.espaco = models_agenda.Espaco.objects.create(
            descricao = 'Sala A',
            color = '#ddd',
            tipo_espaco = self.tipo_espaco,
            ativo = True,
            requer_aprovacao = False,
            # admins= [],
            # teams= [],
            max_duracao= 240,
            min_duracao= 30,
            min_criacao= 24, # 24h
            permite_criar_sabados= False,
            permite_reservar_sabado= False,
            considera_sabado_util= False,
            permite_criar_domingos= False,
            permite_reservar_domingo= False,
            instrucoes_espaco= 'Instruções do espaço aqui...',
            limitar_abertura= False,
            enviar_notificacao= True,
            limitar_abertura_qtde= 0,
        )
        self.espaco.regras.set([self.regra])
        self.espaco.gestores.set([self.gestor])

        to_date = datetime.datetime(2024,11,7)
        start_time=datetime.time(19,0,0)
        end_time=datetime.time(22,0,0)

        self.agendamento = models_agenda.Reserva.objects.create(
            responsavel="Augustus",
            espaco=self.espaco,
            finalidade=self.finalidade,
            date=to_date,
            start=start_time,
            end=end_time,
            titulo='Titulo',
        )
    
    # Testes Unitários

    def test_metodo_clean(self):
        to_date = datetime.datetime(2024,11,8)
        start_time=datetime.time(19,0,0)
        end_time=datetime.time(22,0,0)
        agenda = models_agenda.Reserva()
        agenda.responsavel="Augustus2"
        agenda.espaco=self.espaco
        agenda.finalidade=self.finalidade
        agenda.date=to_date
        agenda.start=start_time
        agenda.end=end_time
        agenda.titulo='Titulo'
        agenda.participantes=0
        self.assertRaises(ValidationError, agenda.clean() )

