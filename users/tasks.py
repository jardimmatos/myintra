from celery import task
from .utils import set_user_logged
from .models import AccessHistory, User
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@task(name="set_user_logged")
def set_user_logged_task(username):
    # not used
    return set_user_logged(username)


@task(name="set_user_access_history")
def set_user_access_history(user_id, origin, access_at, ip):
    """
        Task para registrar histórico de acesso
    """
    try:
        logger.info('running... access history registering')
        user = User.objects.get(id=user_id)
        AccessHistory.objects.create(user=user, origin=origin,
                                     access_at=access_at, ip=ip)
    except Exception as ex:
        print(ex)
    return
