from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status, serializers as drf_serializers
from . import forms, models, enums, serializers as serializer_apps
from rest_framework.permissions import AllowAny
from django.urls import reverse
from . import tasks
from django.conf import settings
from django.db import transaction
from django.views.generic import DetailView, UpdateView, TemplateView
from django.http import Http404


class Painel(TemplateView):
    """
        Template utilizada para Chamada de Painel de Atendimento
    """
    template_name = 'atendimento/painel.html'

    def get_context_data(self, **kwargs):
        context = super(Painel, self).get_context_data(**kwargs)
        context['host_backend'] = 'localhost:8000' if settings.DEBUG \
            else 'meuservidor.dev.br'
        return context


class Acompanhamento(DetailView, UpdateView):
    """
        Acompanhamento de Senha de atendimento
    """
    model = models.Atendimento
    form_class = forms.AvaliacaoForm
    queryset = model.objects.all()
    template_name = 'atendimento/acompanhamento.html'
    context_object_name = 'atendimento'

    def get_context_data(self, **kwargs):
        context = super(Acompanhamento, self).get_context_data(**kwargs)
        context['senha'] = self.kwargs.get('senha')
        context['pk'] = self.kwargs.get('pk')
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(sigla_senha=self.kwargs.get('senha'))
        return qs

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            # Renderize um template alternativo quando o
            # objeto não for encontrado
            return None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super(Acompanhamento, self).form_valid(form)

    def get_success_url(self):
        obj = models.Atendimento.objects.get(pk=self.object.pk)
        return reverse('atendimento:acompanhamento', kwargs={
            'pk': self.object.pk,
            'senha': obj.sigla_senha
        })


class AtendimentoViewSet(viewsets.ViewSet):

    def get_authenticators(self):
        # não exigir authentication_classes para a view de unidades, que é
        # utilizada no painel (independerá de autenticação)
        if self.action_map.get('get', None) == 'list_unidades_atendimento':
            return []

        return super().get_authenticators()

    def get_permissions(self):
        # não exigir permissão para a view de unidades, que é utilizada no
        # painel (independerá de autenticação)
        if self.action == 'list_unidades_atendimento':
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=["GET"])
    def list_unidades_atendimento(self, request):
        """
            Listagem de Unidades de Atendimento
        """
        unidades = models.Unidade.objects.filter(ativo=True).order_by('nome')
        serializer = serializer_apps.UnidadeSerializer(unidades, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def list_servicos(self, request):
        """
            Listagem de Serviços
            Payload representa o argumento de filtros do queryset
            payload: {
                unidade: int ID
                serial: simple|full - especifica qual serializador utilizar
            }
        """
        serial = request.query_params.get(
            'serial', enums.TypeSerials.simple.name)
        unidade_id = request.data.get('unidade')
        servicos = []
        try:
            servicos = models.Servico.objects \
                                    .filter(unidade_id=unidade_id) \
                                    .filter(ativo=True) \
                                    .order_by('nome')
            if serial == enums.TypeSerials.simple.name:
                serializer = serializer_apps.ServicoSimpleSerializer(
                    servicos, many=True)
            else:
                serializer = serializer_apps.ServicoSerializer(
                    servicos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({
                "error": "Falha ao listar serviços: "+str(ex)
                }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    def list_prioridades(self, request):
        """
            Listagem de Prioridades
            Payload representa o argumento de filtros do queryset
            payload: {
                unidade: int ID
            }
        """
        filtro = request.data
        prioridades = []
        try:
            prioridades = models.Prioridade.objects.filter(**filtro)
            serializer = serializer_apps.PrioridadeSerializer(
                prioridades, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({
                "error": "Falha ao listar prioridades: "+str(ex)
                }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    def list_locais(self, request):
        """
            Listagem de Locais
            Payload representa o argumento de filtros do queryset
            payload: {
                unidade: int ID
            }
        """
        filtro = request.data
        result = []
        try:
            result = models.Local.objects.filter(**filtro)
            serializer = serializer_apps.LocalSerializer(result, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({
                "error": "Falha ao listar locais: "+str(ex)
                }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["POST"])
    def triagem_senha(self, request):
        """
            View responsável pela triagem de Senhas
            payload = {
                prioridade: PRIORIDADE_ID,
                unidade: UNIDADE_ID,
                servico: SERVICO_ID,
                atendente_tri: ATENDENTE_ID
                cliente(Opcional): {
                    matricula: MATRICULA,
                    nome: NOME
                    email: EMAIL
                    celular: CELULAR
                }
            }
        """
        novo_atendimento = models.Atendimento()
        args = request.data
        try:
            obj = novo_atendimento.triagem_senha(args)

            # Atualiza lista de senhas no frontend
            self.fila_senhas(
                obj.unidade.id,
                enums.OriginCallFilaSenha.triagem_senha.name)
            self.triagem_notifica_atendente(obj.unidade.id, obj.servico.id)
        except Exception as ex:
            return Response(
                {"error": "Falha na triagem de senha: " + str(ex)},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = serializer_apps.AtendimentoFullSerializer(obj, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def proxima_senha(self, request):
        """
            View responsável por chamar a próxima senha na fila
        """
        args = request.data
        try:
            atendente = models.Atendente.objects.get(
                usuario=request.user, ativo=True)
        except models.Atendente.DoesNotExist:
            return Response({
                "error": "Atendente ativo não disponível para chamada de\
                     senha!"
                }, status=status.HTTP_404_NOT_FOUND)

        args['atendente'] = atendente

        # Chamada Manual (quando há parâmetro atendimento_id)
        if args.get('atendimento_id', False):
            # Se Chamado manualmente via ATENDER
            atendimento = self.executa_chamada_manual(args)

        # Chamada automática da fila
        else:
            atendimento = self.executa_chamada_automatica(args)

        serializer = serializer_apps.PainelSenhaSerializer(
            atendimento.painelsenha, many=False)
        # Atualiza lista de senhas no frontend
        self.fila_senhas(
            atendimento.unidade.id,
            enums.OriginCallFilaSenha.proxima_senha.name)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def chamar_senha_novamente(self, request, pk):
        """ pk painel senha """
        try:
            painel = models.PainelSenha.objects.get(pk=pk)
            p = painel.chamar_senha_painel()
        except models.PainelSenha.DoesNotExist:
            return Response({
                "error": "Senha não encontrada",
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({
                "error": "Falha ao chamar senha novamente!"+str(ex),
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(p, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def iniciar_atendimento(self, request, pk):
        """ pk painel """

        try:
            painel = models.PainelSenha.objects.get(pk=pk)
            painel.atendimento.iniciar_atendimento()
            painel = models.PainelSenha.objects.get(pk=pk)
            serializer = serializer_apps.PainelSenhaSerializer(
                painel, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except models.PainelSenha.DoesNotExist:
            return Response({
                "error": "Atendimento não encontrado",
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({
                "error": "Falha ao iniciar atendimento: "+str(ex)
                }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST"])
    def redirecionar_atendimento(self, request, pk):
        """
            Redireciona o atendimento para outro serviço
            pk = painel.id
            payload: {
                servico: ID (ID servico para o qual está sendo redirecionado)
            }
        """
        args = request.data
        try:
            with transaction.atomic():
                painel = models.PainelSenha.objects.get(pk=pk)
                atendimento = models.Atendimento.objects.get(
                    pk=painel.atendimento.pk)
                atendimento.redirecionar_atendimento(args)
                painel.delete()
                self.fila_senhas(
                    atendimento.unidade.id,
                    enums.OriginCallFilaSenha.redirecionar.name)
        except models.PainelSenha.DoesNotExist:
            return Response({"error": "Atendimento não encontrado!"},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response(
                {"error": "Falha ao redirecionar atendimento! Erro: "+str(ex)},
                status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def encerrar_atendimento(self, request, pk):
        """ pk painel """

        args = request.data
        try:
            painel = models.PainelSenha.objects.get(pk=pk)
            painel.atendimento.encerrar_atendimento(args)
            painel = models.PainelSenha.objects.get(pk=pk)
            # Atualiza lista de senhas no frontend
            self.fila_senhas(
                painel.atendimento.unidade.id,
                enums.OriginCallFilaSenha.encerrar.name)
            return Response(status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({
                "error": "Falha ao encerrar atendimento: "+str(ex),
                }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST"])
    def nao_compareceu_atendimento(self, request, pk):
        """ pk painel """

        try:
            painel = models.PainelSenha.objects.get(pk=pk)
            painel.atendimento.nao_compareceu_atendimento()
            painel = models.PainelSenha.objects.get(pk=pk)
            serializer = serializer_apps.PainelSenhaSerializer(
                painel, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Atendimento.DoesNotExist:
            return Response({
                "error": "Atendimento não encontrado!",
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({
                "error": "Falha ao finalizar atendimento: "+str(ex)
                }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST"])
    def avaliar_atendimento(self, request, pk):
        """ pk atendimento """

        args = request.data
        try:
            atendimento = models.Atendimento.objects.get(pk=pk)
            atendimento.avaliar_atendimento(args)
        except models.Atendimento.DoesNotExist:
            return Response({
                "error": "Atendimento não encontrado"
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({
                "error": "Falha ao avaliar atendimento: "+str(ex)
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"])
    def get_unidade_atendimento(self, request, pk):
        try:
            unidade = models.Unidade.objects.get(pk=pk)
            serializer = serializer_apps.UnidadeSerializer(unidade, many=False)
        except models.Unidade.DoesNotExist:
            return Response({
                "error": "Unidade de atendimento não encontrada"
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({
                "error": "Falha ao obter unidade de atendimento: "+str(ex)
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def get_painel_atual_atendente(self, request):
        """
            Recupera o atendente a partir de um atendimento do usuário que já
            foi chamado ou iniciado (que está em andamento)
        """
        try:
            painel_do_atendente = models.PainelSenha.objects.get(
                atendimento__atendente__usuario=request.user,
                atendimento__status_atendimento__in=[
                        enums.StatusAtendimento.chamado.name,
                        enums.StatusAtendimento.iniciado.name,
                    ])
            serializer = serializer_apps.PainelSenhaSerializer(
                painel_do_atendente, many=False)
            # Atualiza lista de senhas no frontend
            self.fila_senhas(
                request.user.atendente.unidade.id,
                enums.OriginCallFilaSenha.atual_atendente.name)
        except models.PainelSenha.DoesNotExist:
            # Não precisa retornar erro
            return Response({}, status=status.HTTP_200_OK)

        except Exception as ex:
            return Response({
                "error": "Falha ao obter atendimento atual: "+str(ex)
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def get_atendente_logado(self, request):
        try:
            atendente = models.Atendente.objects.get(
                usuario=request.user, ativo=True)
            serializer = serializer_apps.AtendenteSerializer(
                atendente, many=False)
            # Atualiza lista de senhas no frontend
            self.fila_senhas(
                atendente.unidade.id,
                enums.OriginCallFilaSenha.atendente_logado.name)
        except models.Atendente.DoesNotExist:
            return Response({
                "error": "Atendente ativo não encontrado!"
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({
                "error": "Falha ao obter atendente: "+str(ex)
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def alterar_atendente(self, request):
        try:
            numero_local = request.data.get('numero_local', None)
            local = request.data.get('local', None)
            prioridade = request.data.get('prioridade', None)
            servicos = request.data.get('servicos', None)
            unidade = request.data.get('unidade', None)
            atendente = models.Atendente.objects.get(
                usuario=request.user, ativo=True)

            if numero_local:
                atendente.numero_local = numero_local
            if local:
                try:
                    atendente.local = models.Local.objects.get(pk=local)
                except models.Local.DoesNotExist:
                    return Response({
                        "error": "Local não encontrado!"
                        }, status=status.HTTP_404_NOT_FOUND)
            if unidade:
                try:
                    u = models.Unidade.objects.get(pk=unidade)
                    atendente.unidade = u
                except models.Unidade.DoesNotExist:
                    return Response({
                        "error": "Unidade não encontrada!"
                        }, status=status.HTTP_404_NOT_FOUND)
            if prioridade is not None:
                if prioridade == 0:
                    atendente.prioridade = None
                else:
                    try:
                        p = models.Prioridade.objects.get(pk=prioridade)
                        atendente.prioridade = p
                    except models.Prioridade.DoesNotExist:
                        return Response({
                            "error": "Prioridade não encontrada!"
                            }, status=status.HTTP_404_NOT_FOUND)
            if isinstance(type(servicos), type([])):
                try:
                    atendente.servicos.set(servicos)
                except Exception as ex:
                    return Response({
                        "error": "Falha ao atualizar serviços: "+str(ex)
                        }, status=status.HTTP_404_NOT_FOUND)
            atendente.save()
            serializer = serializer_apps.AtendenteSerializer(
                atendente, many=False)
        except models.Atendente.DoesNotExist:
            return Response({
                "error": "Atendente ativo não encontrado!"
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({
                "error": "Falha ao atualizar atendente: "+str(ex)
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"])
    def adicionar_comentario(self, request, pk):
        data = request.data
        if not data.get('comentario'):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        comentario = models.AtendimentoComentario()
        comentario.atendimento_id = pk
        comentario.comentario = data.get('comentario')
        comentario.created_by = request.user
        comentario.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"])
    def listar_comentarios(self, request, pk):
        """ pk: Atendimento"""
        comentarios = models.AtendimentoComentario.objects.filter(
            atendimento=pk)
        serializer = serializer_apps.AtendimentoComentarioSerializer(
            comentarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def fila_senhas(self, unidade_id, origin_trigger):
        """ Execução do Celery necessária """
        tasks.atendimento_fila_senhas.delay(
            {'unidade_id': unidade_id, 'origin': origin_trigger})

    def triagem_notifica_atendente(self, unidade_id, servico_id):
        """ Execução do Celery necessária """
        tasks.atendimento_triagem_notifica_atendente.delay(
            {'unidade_id': unidade_id, 'servico_id': servico_id})

    def executa_chamada_manual(self, args):
        # Se Chamado manualmente via ATENDER
        try:
            atd = models.Atendimento.objects \
                .exclude(
                    status_atendimento__in=[
                        enums.StatusAtendimento.chamado.name,
                        enums.StatusAtendimento.iniciado.name
                    ]
                ).get(
                    atendente__isnull=True,
                    id=args.get('atendimento_id')
                )
            atendimento = atd.proxima_senha(args)
        except models.Atendimento.DoesNotExist:
            raise drf_serializers.ValidationError(
                'Atendimento não encontrado')
        except Exception as ex:
            print(ex)
            raise drf_serializers.ValidationError(
                'Falha ao chamar a senha manualmente!'+str(ex))

        return atendimento

    def executa_chamada_automatica(self, args):
        atendente = args.get('atendente')
        peso_convencional = models.Prioridade.objects.filter(
            nome__in=['Convencional', 'Normal']).first().peso or 1
        peso_prioridade = models.Prioridade.objects.filter(
            nome='Prioridade').first().peso or 2

        existe_atendimento_aberto_do_usuario = models.Atendimento.objects\
            .filter(
                atendente=atendente,
                status_atendimento__in=[
                    enums.StatusAtendimento.chamado.name,
                    enums.StatusAtendimento.iniciado.name
                    ]).exists()

        if existe_atendimento_aberto_do_usuario:
            raise drf_serializers.ValidationError(
                'Existe atendimento em andamento!')

        atendimento = models.Atendimento.objects \
            .filter(servico__in=atendente.servicos.all()) \
            .filter(atendente__isnull=True) \
            .filter(unidade=atendente.unidade) \
            .filter(status_atendimento__in=[
                enums.StatusAtendimento.emitido.name,
                enums.StatusAtendimento.transferido.name
                ]
            ).filter(historico=False).order_by(
                '-redirecionado_por', 'data_chegada')
        if not len(atendimento):
            raise drf_serializers.ValidationError('Nenhuma senha na fila')

        limite_convencionais = peso_prioridade - peso_convencional + 1
        existe_prioridade_length = [
            a.id for a in atendimento[:limite_convencionais]
            if a.prioridade.peso == peso_prioridade
            ]
        if len(existe_prioridade_length):
            atendimento = atendimento.filter(
                id=existe_prioridade_length[0]).first()
        else:
            atendimento = atendimento.first()
        try:
            atendimento = atendimento.proxima_senha(args)
        except Exception as ex:
            raise drf_serializers.ValidationError(
                "Falha ao chamar senha!"+str(ex))
        return atendimento
