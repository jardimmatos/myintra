from django.core.management import BaseCommand
from base.tasks import testando


class Command(BaseCommand):
    help = 'Teste Command'

    def add_arguments(self, parser):
        parser.add_argument('--params', nargs='+', help='Parâmetros(separados por vírgula)')

    def teste_ws_na_execucao_de_tasks(self):
        """
            TESTANDO WEBSOCKET DURANTE TASK DO CELERY - TUDO CERTO
        """
        testando.delay()

    def handle(self, *args, **options):
        """
        Execução da rotina
        """
        self.teste_ws_na_execucao_de_tasks()


