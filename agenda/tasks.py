from intranet.celery import app
# from celery import task
from celery.utils.log import get_task_logger
from base.mail import Email
from .models import Reserva, LogAgenda
from base.enums import ActionEnum, LogTypeEnum, AppEnum
from datetime import datetime

logger = get_task_logger(__name__)

# @task(name="agenda_notificar_email")
@app.task
def agenda_notificar_email(params):
    try:
        """
            Task para enviar e-mail no módulo de agenda
        """
        logger.info(f'running... sendind e-mail Agenda')

        e = Email(
            assunto=params.get('assunto', 'Notificação Agendalabs'),
            content=params.get('content', ''),
            to=params.get('to', []),
            bcc=params.get('bcc', []),
            cc=params.get('cc', []),
            reply_to=params.get('reply_to', []),
            template=params.get('template', None) # 'email/agenda/agenda_abertura.html')
        )
        e.enviar()
    except Exception as ex:
        print('Falha ao enviar e-mail de reserva em task agenda_notificar_email', params, ex)
    return

@app.task
def agenda_registra_log(params):
    """
        Task para registrar log de agenda
    """
    logger.info(f'running... registering log Agenda')
    try:
        reserva = Reserva.objects.get(id=params.get('log_reserva'))
    except:
        return
    try:
        params_log = {
            'log':          params.get('log','Mensagem de log não informada'), 
            'log_action':   params.get('log_action', ActionEnum.VIEW.name), 
            'log_at':       params.get('log_at', f'{datetime.now()}'), 
            'log_type':     params.get('log_type', LogTypeEnum.VIEW.name),
            'log_app':      params.get('log_app', AppEnum.AGENDALABS.name),
            'log_model':    params.get('log_model', 'LogAgenda'), 
            'log_reserva':  reserva, 
        }
        LogAgenda.objects.create(**params_log)
    except: 
        print('Falha ao registrar log de reserva em task agenda_registra_log', params)
    return
