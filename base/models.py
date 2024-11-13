import uuid
from django.db import models
from base import enums
from django.conf import settings
from django.core.exceptions import ValidationError
from django_resized import ResizedImageField


class TimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(
        'criado em', auto_now_add=True, auto_now=False, null=True)
    updated_at = models.DateTimeField(
        'alterado em', auto_now_add=False, auto_now=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="%(app_label)s_%(class)s_created_by_related",
        related_query_name="%(app_label)s_%(class)ss_created_by")
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="%(app_label)s_%(class)s_updated_by_related",
        related_query_name="%(app_label)s_%(class)ss_updated_by")

    @property
    def get_created_at(self):
        return self.created_at.strftime(
            enums.FormatDateStringsEnum.DEFAULT_BR_FORMAT_DATETIME.value)

    @property
    def get_updated_at(self):
        return self.updated_at.strftime(
            enums.FormatDateStringsEnum.DEFAULT_BR_FORMAT_DATETIME.value)

    def created_by_object(self):
        return self.created_by

    def updated_by_object(self):
        return self.updated_by

    class Meta:
        abstract = True


class TimeStampedIDModel(TimeStampedModel):
    id = models.BigAutoField(primary_key=True, db_index=True, editable=False)

    class Meta:
        abstract = True


class TeamsChannel(TimeStampedModel):
    titulo = models.CharField(max_length=255, blank=False,
                              null=True, verbose_name="Título do canal")
    webhook = models.URLField(unique=True, blank=False, null=True,
                              verbose_name="Webhook", max_length=255)
    ativo = models.BooleanField(default=True,
                                help_text="Canal está ativo para envio?")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Teams - Canal'
        verbose_name_plural = 'Teams - Canais'


class Arquivo(TimeStampedModel):
    arquivo = models.FileField(
        upload_to='arquivos', null=True, blank=True, verbose_name='Arquivos')
    descricao = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='Descrição')

    def __str__(self):
        return f"{self.descricao}"


class MonitorServico(TimeStampedModel):
    servico = models.CharField(
        max_length=250, verbose_name='Serviço', blank=False, null=True)
    url = models.CharField(
        max_length=250, verbose_name='URL', blank=False, null=True)
    referencia = models.CharField(
        max_length=250, verbose_name='Referência', blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.servico}'

    class Meta:
        verbose_name = 'Monitor - Teste de Serviço'
        verbose_name_plural = 'Monitor - Teste de Serviços'


def path_logo(instance, filename):
    return 'global/logo/%s/%s' % (instance.id, filename)


class GlobalSetting(TimeStampedModel):
    description = models.CharField(
        max_length=100, default="Configuração global padrão", null=True,
        blank=False, verbose_name="Descrição")
    logo = ResizedImageField(
        size=[100, 100], upload_to=path_logo, blank=True, null=True,
        verbose_name="Logo")

    def __str__(self):
        return self.description

    def clean(self):
        setting = GlobalSetting.objects.filter(~models.Q(id=self.id)).count()
        if setting > 0:
            raise ValidationError(
                "Já existe uma configuração global registrada no sistema!")

    class Meta:
        verbose_name = 'Sistema - Configuração global'
        verbose_name_plural = 'Sistema - Configurações globais'
        permissions = (
            (
                'can_resetpassword_global',
                'Redefinir senha Global'),
            (
                'can_gerenciar_containers',
                'Pode Gerenciar Containers na Infraestrutura'),
        )


class LogSistema(models.Model):
    log = models.TextField('Log')
    path = models.TextField('Path')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.path

    class Meta:
        verbose_name = 'Sistema - Log de Sistema'
        verbose_name_plural = 'Sistema - Logs de Sistema'


class SystemParams(TimeStampedIDModel):
    # utilizar modelo de chave "[app.funcao]"
    # Ex: moodle.integra_graduacao
    chave = models.CharField(
        max_length=80, null=True, blank=False, unique=True)
    descricao = models.CharField(max_length=255, null=True, blank=True)
    valor = models.CharField(max_length=255, null=True, blank=False)

    def __str__(self):
        return self.chave

    class Meta:
        verbose_name = 'Sistema - Parâmetro'
        verbose_name_plural = 'Sistema - Parâmetros'
