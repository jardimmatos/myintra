# flake8: noqa

from django.test import TestCase
from . import models
from . import enums
from users.models import User
# from django.core.exceptions import ValidationError
# from datetime import datetime


class AtendimentoTestCase(TestCase):

    def setUp(self):
        self.unidade, _ = models.Unidade.objects.get_or_create(nome="SGDB")
        self.cliente, _ = models.Cliente.objects.get_or_create(
            matricula="001-001234", nome="Agostinho Junior")
        self.departamento, _ = models.Departamento.objects.get_or_create(
            unidade=self.unidade, nome="Departamento A")
        self.prioridade, _ = models.Prioridade.objects.get_or_create(
            unidade=self.unidade, nome="Prioridade A")
        self.perfil, _ = models.Perfil.objects.get_or_create(
            unidade=self.unidade, nome="Perfil A")
        self.local, _ = models.Local.objects.get_or_create(
            unidade=self.unidade, nome="Local A")
        self.usuario, _ = User.objects.get_or_create(
            username="teste", email="mail@mail.com", first_name="Triage",
            last_name="Userr")
        self.atendente, _ = models.Atendente.objects.get_or_create(
            usuario=self.usuario, perfil=self.perfil,
            prioridade=self.prioridade, local=self.local, numero_local="1")
        self.servico, _ = models.Servico.objects.get_or_create(
            unidade=self.unidade, nome="Serviço A", peso=1)
        self.args = {
            "unidade": self.unidade.id,
            "prioridade": self.prioridade.id,
            "atendente_tri": self.atendente.id,
            "cliente": {
                "matricula": "000-001234",
                "nome": "ARTHUR",
                "email": "arthur@mail.com",
                "celular": "123456789"
            }
        }
        self.a = models.Atendimento()
        self.atendimento = self.a.triagem_senha(self.args)

    def test_fluxo(self):
        self.assertIsNotNone(self.unidade)
        self.assertIsNotNone(self.cliente)
        self.assertIsNotNone(self.departamento)
        self.assertIsNotNone(self.prioridade)
        self.assertIsNotNone(self.perfil)
        self.assertIsNotNone(self.local)
        self.assertIsNotNone(self.usuario)
        self.assertIsNotNone(self.servico)

        self.assertIsNotNone(self.atendimento)
        self.assertIsNotNone(self.atendimento.unidade)
        self.assertIsNotNone(self.atendimento.cliente)
        self.assertIsNotNone(self.atendimento.prioridade)
        self.assertIsNotNone(self.atendimento.atendente_tri)
        self.assertIsNotNone(self.atendimento.data_chegada)

        self.assertIsNone(self.atendimento.data_chamada)
        self.assertIsNone(self.atendimento.data_inicio)
        self.assertIsNone(self.atendimento.data_fim)
        self.assertIsNone(self.atendimento.atendente)
        self.assertIsNone(self.atendimento.local)
        self.assertIsNone(self.atendimento.tempo_espera)
        self.assertIsNone(self.atendimento.tempo_deslocamento)
        self.assertIsNone(self.atendimento.tempo_atendimento)
        self.assertIsNone(self.atendimento.tempo_permanencia)
        self.assertIsNone(self.atendimento.resolucao)
        self.assertIsNone(self.atendimento.obs)

        self.assertEqual(self.atendimento.status_atendimento, enums.StatusAtendimento.emitido.name)
        self.assertEqual(self.atendimento.cliente.matricula, "000-001234")
        self.assertEqual(str(self.atendimento.sigla_senha), str("DEPS001"))
        self.assertEqual(str(self.atendimento.senha), str(1))

        # Chamar Senha
        chamar = {
            'atendente': self.atendente
        }
        self.atendimento = self.atendimento.chamar_senha(chamar)
        self.assertIsNotNone(self.atendimento.data_chamada)
        self.assertIsNotNone(self.atendimento.local)
        self.assertIsNotNone(self.atendimento.tempo_espera)
        self.assertEqual(self.atendimento.status_atendimento, enums.StatusAtendimento.chamado.name)
        self.assertEqual(self.atendimento, self.atendimento.painelsenha.atendimento)
        self.assertTrue(models.PainelSenha.objects.filter(atendimento__id=self.atendimento.id).exists())

        # iniciar_atendimento
        self.atendimento = self.atendimento.iniciar_atendimento()
        self.assertIsNotNone(self.atendimento.data_inicio)
        self.assertIsNotNone(self.atendimento.tempo_deslocamento)
        self.assertEqual(self.atendimento.status_atendimento, enums.StatusAtendimento.iniciado.name)

        args = {
            'resolucao': enums.ResolucaoAtendimento.resolvido.name
        }
        self.atendimento = self.atendimento.encerrar_atendimento(args)
        self.assertIsNotNone(self.atendimento.data_fim)
        self.assertIsNotNone(self.atendimento.tempo_atendimento)
        self.assertIsNotNone(self.atendimento.tempo_permanencia)
        self.assertIsNotNone(self.atendimento.resolucao)
        self.assertEqual(self.atendimento.status_atendimento, enums.StatusAtendimento.encerrado.name)
        self.assertIn(self.atendimento.resolucao, [r.name for r in enums.ResolucaoAtendimento])
