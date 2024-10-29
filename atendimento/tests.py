from datetime import datetime
from django.test import TestCase
from . import models
from . import enums
from django.core.exceptions import ValidationError
from users.models import User, Local
from filial.models import Filial
from coligadas.models import Coligada

class AtendimentoTestCase(TestCase):

    def setUp(self):
        self.unidade, _ = models.Unidade.objects.get_or_create(nome="SGDB")
        self.cliente, _ = models.Cliente.objects.get_or_create(matricula="002-009279", nome="Agostinho Junior")
        self.coligada, _ = Coligada.objects.get_or_create(codcoligada=1, descricao="Coligada A")
        self.filial, _ = Filial.objects.get_or_create(coligada=self.coligada, codfilial=1, codtipocurso=1)
        self.departamento, _ = models.Departamento.objects.get_or_create(unidade=self.unidade, nome="Departamento A")
        self.prioridade, _ = models.Prioridade.objects.get_or_create(unidade=self.unidade, nome="Prioridade A")
        self.perfil, _ = models.Perfil.objects.get_or_create(unidade=self.unidade, nome="Perfil A")
        self.local, _ = models.Local.objects.get_or_create(unidade=self.unidade, nome="Local A")
        self.user_local, _ = Local.objects.get_or_create(codsetor="123113", setor="aasdasd", codfilial=1)
        self.usuario, _ = User.objects.get_or_create(
                                                    username="teste",
                                                    email="mail@mail.com",
                                                    first_name="Triage",
                                                    last_name="Userr"
                                                    )
        self.usuario.filiais.set([self.filial])
        self.usuario.locais.set([self.user_local])
        self.atendente, _ = models.Atendente.objects.get_or_create(usuario=self.usuario, perfil=self.perfil, prioridade=self.prioridade, local=self.local, numero_local="1")
        self.servico, _ = models.Servico.objects.get_or_create(unidade=self.unidade, nome="Serviço A", peso=1)
        self.servico_departamento, _ = models.ServicoDepartamento.objects.get_or_create(unidade=self.unidade, servico=self.servico, departamento=self.departamento, sigla="DEPS")
        self.args = {
            "unidade": self.unidade.id,
            "servico_departamento": self.servico_departamento.id,
            "prioridade": self.prioridade.id,
            "atendente_tri": self.atendente.id,
            "cliente": {
                "matricula": "002-009279",
                "nome": "ARTHUR MILLER",
                "email": "arthur@mail.com",
                "celular": "123456789"
            }
        }
        self.a = models.Atendimento()
        self.atendimento = self.a.triagem_senha(self.args)
        
        
        
    def test_fluxo(self):
        self.assertIsNotNone(self.unidade)
        self.assertIsNotNone(self.cliente)
        self.assertIsNotNone(self.coligada)
        self.assertIsNotNone(self.filial)
        self.assertIsNotNone(self.departamento)
        self.assertIsNotNone(self.prioridade)
        self.assertIsNotNone(self.perfil)
        self.assertIsNotNone(self.local)
        self.assertIsNotNone(self.user_local)
        self.assertIsNotNone(self.usuario)
        self.assertIsNotNone(self.servico)
        self.assertIsNotNone(self.servico_departamento)
        
        self.assertIsNotNone(self.atendimento)
        self.assertIsNotNone(self.atendimento.unidade)
        self.assertIsNotNone(self.atendimento.cliente)
        self.assertIsNotNone(self.atendimento.prioridade)
        self.assertIsNotNone(self.atendimento.servico_departamento)
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
        self.assertEqual(self.atendimento.cliente.matricula, "002-009279")
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

    
        
    # self.assertRaises(ValidationError, a.triagem_senha(self.args))


'''
from .models import *
from .utils import *
from django.utils import timezone
from .serializers import *

class BaseCrudsTest(TestCase):

    def testar_serializers(self):
        filial = Filial.objects.create(nome='FILIAL1')
        serialfilial = FilialSerializer(filial, many=False)
        self.assertIsNotNone(serialfilial.data)
        print(serialfilial.data)

        marca = Marca.objects.create(descricao='Dell')
        serialmarca = MarcaSerializer(Marca.objects.all(), many=True)
        self.assertIsNotNone(serialmarca.data)
        print(serialmarca.data)

        finalidade = Finalidade.objects.create(descricao='Aula')
        serialfinalidade = FinalidadeSerializer(finalidade, many=False)
        self.assertIsNotNone(serialfinalidade.data)
        from django.http import JsonResponse
        print( JsonResponse(serialfinalidade.data)) 

        dispositivo = Dispositivo.objects.create(descricao='Notebook', marca=marca)
        serialdispositivo = DispositivoSerializer(Dispositivo.objects.all(), many=True)
        self.assertIsNotNone(serialdispositivo.data)
        print(serialdispositivo.data)

    def testar_baixa_item_entrega(self):
        filial = Filial.objects.create(nome='FILIAL1')
        marca1 = Marca.objects.create(descricao='Dell')
        marca2 = Marca.objects.create(descricao='Apple')
        finalidade = Finalidade.objects.create(descricao='Aula')
        dispositivo1 = Dispositivo.objects.create(descricao='Notebook', marca=marca1)
        dispositivo2 = Dispositivo.objects.create(descricao='iPad', marca=marca2)    
        
        recurso1 = Recurso.objects.create(identificador='1234', filial=filial, dispositivo=dispositivo1)
        self.assertIs(recurso1.is_disponivel(), True)

        recurso2 = Recurso.objects.create(identificador='123456', filial=filial, dispositivo=dispositivo2)
        self.assertIs(recurso2.is_disponivel(), True)
        
        entrega = Entrega.objects.create(
            destinatario = 'Augustus Cliente',
            emitido_em = timezone.now(),
            finalidade = finalidade,
        )
        self.assertIsInstance(entrega, Entrega)

        itens = [ 
            EntregaItem(entrega = entrega,recurso = recurso1),
            EntregaItem(entrega = entrega,recurso = recurso2)
        ]

        create_itens = EntregaItem.objects.bulk_create(itens)
        
        # Recursos devem estar indisponível
        self.assertIs(recurso1.is_disponivel(), False)
        self.assertIs(recurso2.is_disponivel(), False)

        # Existe dois itens na Entrega
        self.assertTrue(Entrega.objects.first().entrega_itens.all().count() == 2)

        # Status da Entrega inicializa como ABERTO
        self.assertIs(entrega.status, StatusEntrega.ABERTO.value)

        # Destinatário não é None
        self.assertIsNot(entrega.destinatario, None)

        # Itens da entrega tem status Emprestado
        self.assertIs(entrega.entrega_itens.filter(status=StatusCirculacao.EMPRESTADO.value).count(), 2)

        # Baixar Item
        recebedor = 'Augustus'

        item1 = EntregaItem.objects.filter(recurso=recurso1).first()
        item1.baixar_normal(recebedor)
        
        # Registrar nome do recebedor do item na baixa não deve ser None
        self.assertIsNot(item1.recebedor, None)

        # Status da Entrega deve continuar ABERTO
        self.assertTrue(entrega.status == StatusEntrega.ABERTO.value)

        # Item1 da entrega deve constar como DISPONIVEL
        self.assertTrue(entrega.entrega_itens.get(id=item1.id).status == StatusCirculacao.DISPONIVEL.value)

        # Recurso do Item1 deve estar disponível após a baixa dele
        recurso1_disponivel = item1.recurso.is_disponivel()
        self.assertTrue(recurso1_disponivel)

        # Item2 da entrega deve constar como EMPRESTADO
        self.assertTrue(entrega.entrega_itens.exclude(id=item1.id).first().status == StatusCirculacao.EMPRESTADO.value)

        # Baixar item2 com Avaria
        item2 = EntregaItem.objects.filter(recurso=recurso2).first()
        item2.baixar_avaria(recebedor, "Monitor trincado")
        
        # Item2 da entrega deve constar como Devolvido com avaria
        self.assertTrue(entrega.entrega_itens.get(id=item2.id).status == StatusCirculacao.DEVOLVIDO_AVARIA.value)

        # Recurso do Item2 deve estar AVARIADO e indisponível após a baixa dele
        item2 = EntregaItem.objects.filter(recurso__id=recurso2.id).first()
        self.assertFalse(item2.recurso.is_disponivel())
        self.assertTrue(item2.recurso.situacao == StatusRecurso.AVARIADO.value)
        
        # Item2 deve constar obs de devolução com avaria
        self.assertIsNot(item2.obs, None)

        # Entrega deve baixar quando não houver mais nenhum item emprestado
        entrega = Entrega.objects.first()
        self.assertTrue(entrega.status == StatusEntrega.FINALIZADO.value)

        if entrega.status == StatusEntrega.FINALIZADO.value:
            # Registrar nome do recebedor da entrega na baixa não deve ser None
            self.assertTrue(entrega.baixado_por == recebedor)

        recurso = Recurso.objects.get(pk=item2.pk)

        #  Definir como DISPONIVEL
        recurso.set_situacao_disponivel()
        recurso = Recurso.objects.get(id = recurso.id)
        self.assertTrue(recurso.situacao == StatusRecurso.DISPONIVEL.value)
        # Definir como MANUTENÇÃO
        recurso.set_situacao_manutencao()
        recurso = Recurso.objects.get(id = recurso.id)
        self.assertTrue(recurso.situacao == StatusRecurso.MANUTENCAO.value)
        # Definir como AVARIA
        recurso.set_situacao_avaria()
        recurso = Recurso.objects.get(id = recurso.id)
        self.assertTrue(recurso.situacao == StatusRecurso.AVARIADO.value)
        # Definir como EXTRAVIO
        recurso.set_situacao_extravio()
        recurso = Recurso.objects.get(id = recurso.id)
        self.assertTrue(recurso.situacao == StatusRecurso.EXTRAVIO.value)

    def testar_baixa_item_entrega(self):
        filial = Filial.objects.create(nome='FILIAL1')
        marca1 = Marca.objects.create(descricao='Dell')
        marca2 = Marca.objects.create(descricao='Apple')
        finalidade = Finalidade.objects.create(descricao='Aula')
        dispositivo1 = Dispositivo.objects.create(descricao='Notebook', marca=marca1)
        dispositivo2 = Dispositivo.objects.create(descricao='iPad', marca=marca2)    
        
        recurso1 = Recurso.objects.create(identificador='1234', filial=filial, dispositivo=dispositivo1)
        recursos_emprestados = recurso1.entrega_itens.exclude(status__in=[
            StatusCirculacao.DISPONIVEL.value,
            StatusCirculacao.DEVOLVIDO_AVARIA.value
        ]).count() == 0
        recurso_disponivel = recurso1.situacao == StatusRecurso.DISPONIVEL.value
        print(recursos_emprestados, recurso_disponivel)

        self.assertIs(recurso1.is_disponivel(), True)

        recurso2 = Recurso.objects.create(identificador='123456', filial=filial, dispositivo=dispositivo2)
        self.assertIs(recurso2.is_disponivel(), True)
        
        entrega = Entrega.objects.create(
            destinatario = 'Augustus Cliente',
            emitido_em = timezone.now(),
            finalidade = finalidade,
        )
        self.assertIsInstance(entrega, Entrega)

        itens = [ 
            EntregaItem(entrega = entrega,recurso = recurso1),
            EntregaItem(entrega = entrega,recurso = recurso2)
        ]

        create_itens = EntregaItem.objects.bulk_create(itens)
        
        # Recursos devem estar indisponível
        self.assertIs(recurso1.is_disponivel(), False)
        self.assertIs(recurso2.is_disponivel(), False)

        # Existe dois itens na Entrega
        self.assertTrue(Entrega.objects.first().entrega_itens.all().count() == 2)

        # Status da Entrega inicializa como ABERTO
        self.assertIs(entrega.status, StatusEntrega.ABERTO.value)

        # Destinatário não é None
        self.assertIsNot(entrega.destinatario, None)

        # Itens da entrega tem status Emprestado
        self.assertIs(entrega.entrega_itens.filter(status=StatusCirculacao.EMPRESTADO.value).count(), 2)

        # Baixar Item
        recebedor = 'Augustus'

        item1 = EntregaItem.objects.filter(recurso=recurso1).first()
        item1.baixar_normal(recebedor)

        # Registrar nome do recebedor do item na baixa não deve ser None
        self.assertIs(item1.recebedor, recebedor)

        # Status da Entrega deve continuar ABERTO
        self.assertIs(entrega.status, StatusEntrega.ABERTO.value)

        # Item1 da entrega deve constar como DISPONIVEL
        self.assertTrue(entrega.entrega_itens.get(id=item1.id).status == StatusCirculacao.DISPONIVEL.value)

        # Recurso do Item1 deve estar disponível após a baixa dele
        recurso1_disponivel = item1.recurso.is_disponivel()
        self.assertTrue(recurso1_disponivel)

        # Item2 da entrega deve constar como EMPRESTADO
        self.assertTrue(entrega.entrega_itens.exclude(id=item1.id).first().status == StatusCirculacao.EMPRESTADO.value)

        item2 = EntregaItem.objects.filter(recurso=recurso2).first()
        item2.baixar_normal(recebedor)
        
        # Item2 da entrega deve constar como DISPONIVEL
        self.assertTrue(entrega.entrega_itens.get(id=item2.id).status == StatusCirculacao.DISPONIVEL.value)

        # Recurso do Item2 deve estar disponível após a baixa dele
        recurso2_disponivel = item2.recurso.is_disponivel()
        self.assertTrue(recurso2_disponivel)

        # Entrega deve baixar quando não houver mais nenhum item emprestado
        entrega = Entrega.objects.first()
        self.assertTrue(entrega.status == StatusEntrega.FINALIZADO.value)

        if entrega.status == StatusEntrega.FINALIZADO.value:
            # Registrar nome do recebedor da entrega na baixa não deve ser None
            self.assertTrue(entrega.baixado_por == recebedor)

    def testar_baixa_normal_entrega(self):
        filial = Filial.objects.create(nome='FILIAL1')
        marca1 = Marca.objects.create(descricao='Dell')
        marca2 = Marca.objects.create(descricao='Apple')
        finalidade = Finalidade.objects.create(descricao='Aula')
        dispositivo1 = Dispositivo.objects.create(descricao='Notebook', marca=marca1)
        dispositivo2 = Dispositivo.objects.create(descricao='iPad', marca=marca2)    
        recurso1 = Recurso.objects.create(identificador='1234', filial=filial, dispositivo=dispositivo1)
        recurso2 = Recurso.objects.create(identificador='123456', filial=filial, dispositivo=dispositivo2)
        entrega = Entrega.objects.create(
            destinatario = 'Augustus Cliente',
            emitido_em = timezone.now(),
            finalidade = finalidade,
        )
        print('entrega',entrega.__dict__)
        self.assertIsInstance(entrega, Entrega)

        itens = [ 
            EntregaItem(entrega = entrega,recurso = recurso1),
            EntregaItem(entrega = entrega,recurso = recurso2)
        ]
        create_itens = EntregaItem.objects.bulk_create(itens)
        # Existe dois itens na Entrega
        self.assertTrue(Entrega.objects.first().entrega_itens.all().count() == 2)

        # Status da Entrega inicializa como ABERTO
        self.assertIs(entrega.status, StatusEntrega.ABERTO)

        # Destinatário não é None
        self.assertIsNot(entrega.destinatario, None)

        # Itens da entrega tem status Emprestado
        self.assertIs(entrega.entrega_itens.filter(status=StatusCirculacao.EMPRESTADO).count(), 2)

        # Baixar Tudo
        recebedor = 'Augustus'

        entrega.baixar_tudo(recebedor)
        self.assertIs(entrega.status, StatusEntrega.FINALIZADO)

        # Itens da entrega com status disponível após baixado
        self.assertIs(entrega.entrega_itens.filter(status=StatusCirculacao.DISPONIVEL).count(), 2)

        # Registrar nome do recebedor na baixa
        self.assertIs(entrega.baixado_por, recebedor)
        
    def testar_alterar_situacao_recursos(self):
        filial = Filial.objects.create(nome='FILIAL1')
        marca = Marca.objects.create(descricao='Dell')
        dispositivo = Dispositivo.objects.create(descricao='Notebook', marca=marca)
        
        # Criar recurso
        recurso = Recurso.objects.create(
            identificador='123456',
            filial=filial,
            dispositivo=dispositivo
            )
        self.assertIsNot(recurso, None)

        # alterando a situacao do recurso
        # Recurso extraviado
        recurso.set_situacao_extravio()
        self.assertTrue(Recurso.objects.filter(identificador='123456', dispositivo=dispositivo, situacao=StatusRecurso.EXTRAVIO).exists())
        
        #Recurso em manutenção
        recurso.set_situacao_manutencao()
        self.assertTrue(Recurso.objects.filter(identificador='123456', dispositivo=dispositivo, situacao=StatusRecurso.MANUTENCAO).exists())
        
        # Disponibilizando Recurso
        recurso.set_situacao_disponivel()
        self.assertTrue(Recurso.objects.filter(identificador='123456', dispositivo=dispositivo, situacao=StatusRecurso.DISPONIVEL).exists())

        # Listando Recursos por filial
        self.assertTrue(Filial.objects.first().recursos.all().exists())

        # Listando Recursos por dispositivo
        self.assertTrue(Dispositivo.objects.first().recursos.all().exists())

        #Testando valor decimal
        try:
            self.assertTrue(float(recurso.valor) >= 0)
        except:
            print('exc valor',recurso.valor)
            self.assertTrue(1 == 2)

            


    def testar_valor_recursos(self):
        filial = Filial.objects.create(nome='FILIAL1')
        marca = Marca.objects.create(descricao='Dell')
        dispositivo = Dispositivo.objects.create(descricao='Notebook', marca=marca)
        
        # Criar recurso
        recurso = Recurso.objects.create(
            identificador='123456',
            filial=filial,
            dispositivo=dispositivo,
            valor=1
            )
        self.assertIsNot(recurso, None)

        #Testando valor decimal
        try:
            self.assertTrue(float(recurso.valor) >= 0)
        except:
            print('exc valor',recurso.valor)
            self.assertTrue(1 == 1)
        
    def testar_duplicidade_recursos(self):
        filial = Filial.objects.create(nome='FILIAL1')
        marca = Marca.objects.create(descricao='Dell')
        dispositivo = Dispositivo.objects.create(descricao='Notebook', marca=marca)
        
        # Criar recurso
        recurso = Recurso.objects.create(
            identificador='123456',
            filial=filial,
            dispositivo=dispositivo
            )
        self.assertIsNot(recurso, None)
        self.assertIsInstance (recurso, Recurso)

        #tentativa de criar recurso com identificador e dispositivo duplicado (constraints)
        try:
            recurso2 = Recurso.objects.create(
                identificador='123456',
                filial=filial,
                dispositivo=dispositivo
                )
            self.assertIs(recurso2, None)
        except:
            recurso2 = None
            self.assertIs(recurso2,None)

    def testar_crud_de_marcas(self):
        nome_marca = 'Dell'
        create = {'descricao':nome_marca}
        marca = Marca.objects.create(**create)

        self.assertIs(Marca.objects.filter(descricao=nome_marca).exists(), True)

        marca.descricao = 'Apple'
        marca.save()
        self.assertIs(Marca.objects.filter(descricao=nome_marca).exists() , False)
        
        marca.delete()
        self.assertIs(Marca.objects.filter(descricao='Apple').exists() , False)

    def testar_crud_de_finalidade(self):
        desc = 'Aula'
        create = {'descricao':desc}
        obj = Finalidade.objects.create(**create)

        self.assertIs(Finalidade.objects.filter(descricao=desc).exists(), True)

        obj.descricao = 'Apple'
        obj.save()
        self.assertIs(Finalidade.objects.filter(descricao=desc).exists() , False)
        
        obj.delete()
        self.assertIs(Finalidade.objects.filter(descricao='Palestra').exists() , False)

    def testar_crud_de_dispositivo(self):
        novamarca = Marca.objects.create(descricao='Dell')
        self.assertTrue(Marca.objects.filter(descricao='Dell').exists())

        disp = {'descricao': 'Notebook', 'marca': novamarca}
        dispositivo = Dispositivo.objects.create(**disp)

        # Pesquisar pela descrição
        self.assertTrue(Dispositivo.objects.filter(descricao=disp['descricao']).exists(), True)

        # Pesquisar pela Marca
        self.assertTrue(Dispositivo.objects.filter(marca__descricao='Dell').exists())
        
        # Listar Dispositivos pela Marca
        self.assertTrue(Marca.objects.first().dispositivos.all().exists())

        # update
        dispositivo.descricao = 'iPad'
        dispositivo.save()
        self.assertFalse(Dispositivo.objects.filter(descricao='Notebook').exists())
        
        # Campo Marca deve ser None quando FK Marca for excluída
        novamarca.delete()
        self.assertIs(Dispositivo.objects.filter(descricao='iPad').first().marca, None)

        # Excluir dispositivo
        dispositivo.delete()
        self.assertFalse(Dispositivo.objects.filter(descricao='iPad').exists())
'''