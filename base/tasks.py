from intranet.celery import app
from celery import task
from .teams import TeamsTemplates
from base.utils import call_ws
from base.enums import GlobalChannelsEnum
from time import sleep

# from celery import task, app
#from celery.schedules import crontab

# disable UTC so that Celery can use local time
#app.conf.enable_utc = False


@app.task
def testando():
    room = 'room_channel_monitor'
    call_ws(
        channel_name=room,
        msg="Executando A...", 
        tag=GlobalChannelsEnum.REFRESH.value,
        notify=True
    )
    sleep(2)
    call_ws(
        channel_name=room,
        msg="Executando B...", 
        tag=GlobalChannelsEnum.REFRESH.value,
        notify=True
    )
    sleep(2)
    call_ws(
        channel_name=room,
        msg="Executando C...", 
        tag=GlobalChannelsEnum.REFRESH.value,
        notify=True
    )
    sleep(2)
    call_ws(
        channel_name=room,
        msg="Processamento finalizado...", 
        tag=GlobalChannelsEnum.LOADED.value,
        notify=True
    )

@app.task
def task_send_teams_channel(options):
    return TeamsTemplates(options).send()
