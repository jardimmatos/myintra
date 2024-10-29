from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from . import models
from datetime import datetime
from users.tasks import set_user_access_history
from base.enums import OriginLogin

@receiver(user_logged_in)
def on_login(sender, user, request, **kwargs):
    # Log de Login Backend
    try: ip = request.META.get('REMOTE_ADDR')
    except: ip = ''

    acesso_em = f'{datetime.now()}'
    set_user_access_history.delay(user.id.hex, OriginLogin.BACKEND.name, acesso_em, ip)
