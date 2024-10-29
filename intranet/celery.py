from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab, crontab_parser
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intranet.settings')
app = Celery('intranet')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Teste Request Celery Task: {self.request!r}')

# # @app.on_after_configure.connect
# @app.connection()
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(30.0, test.s('world'), expires=10)

#     # # Executes every Monday morning at 7:30 a.m.
#     # sender.add_periodic_task(
#     #     crontab(hour=7, minute=30, day_of_week=1),
#     #     test.s('Happy Mondays!'),
#     # )

# @app.task
# def test(arg):
#     print(arg)

# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))

# Run command prompt to console in background, adicionando -B para rodar os beat (periodic tasks)
# $ celery -A intranet worker -B -l info


# Crontab parser
# >>># minute="*/17"
# >>>crontab_parser(60).parse("*/17")
# {0, 17, 34, 51}
# >>># hour="*/3,6-18"
# >>>crontab_parser(23, 0).parse("*/3,6-18")
# {0, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21}
