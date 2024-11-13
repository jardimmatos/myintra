from intranet.celery import app
from celery.utils.log import get_task_logger
from . import models, enums, serializers as serializer_apps
from base.utils import call_ws
import time
from datetime import timedelta, date

logger = get_task_logger(__name__)


@app.task
def atendimento_fila_senhas(params):
    """
        Task para atualizar lista de fila de senhas
    """
    time.sleep(1)
    unidade_id = params.get('unidade_id')
    atendimentos = models.Atendimento.objects\
        .filter(unidade__id=unidade_id) \
        .filter(historico=False) \
        .filter(status_atendimento__in=[
            enums.StatusAtendimento.emitido.name,
            enums.StatusAtendimento.transferido.name,
        ]) \
        .order_by('-redirecionado_por', 'data_chegada')

    serializer = serializer_apps.AtendimentoFullSerializer(
        atendimentos, many=True)
    data = serializer.data
    call_ws(f'room_channel_painel_atendimento_{unidade_id}', '',
            'LIST-TICKET', data, notify=False)

    qs_atendimentos_dia_anterior = models.Atendimento.objects\
        .filter(unidade__id=unidade_id) \
        .filter(historico=False) \
        .filter(data_chegada__date__lte=(
            date.today() - timedelta(days=1)))
    historico = qs_atendimentos_dia_anterior.filter(status_atendimento__in=[
        enums.StatusAtendimento.encerrado.name,
        enums.StatusAtendimento.nao_compareceu.name])
    if historico.exists():
        # print('Alterar para historico', len(historico))
        # historico.update(**{'historico': True})
        for h in historico:
            # print(h.sigla_senha)
            h.historico = True
            h.save()
    return


@app.task
def atendimento_triagem_notifica_atendente(params):
    """
        Task para notificar os atendentes quando na emissão de senha
    """
    time.sleep(1)
    unidade_id = params.get('unidade_id')
    data = params
    call_ws(f'room_channel_painel_atendimento_{unidade_id}', '',
            'PRINTED-TICKET', data, notify=True)
    return
