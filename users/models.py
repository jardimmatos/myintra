import secrets
import string
from django.contrib.auth.models import AbstractUser
from django.db import models
from base.enums import FormatDateStringsEnum, OriginLogin
from django.utils.translation import gettext as _
from base.models import TimeStampedModel
# from django.contrib.admin.models import LogEntry
# from django.core.exceptions import ValidationError
# from django.urls import reverse
# from django_resized import ResizedImageField
# from django.utils.html import format_html


def path_photo(instance, filename):
    return 'profile/photo/%s/%s' % (instance.id, filename)


class User(AbstractUser, TimeStampedModel):
    token = models.CharField(verbose_name='Token', null=True, blank=True,
                             editable=False, max_length=30)

    def __str__(self):
        return f'{self.username} - {self.first_name}'

    @property
    def is_atendente(self):
        try:
            return self.atendente and self.atendente.ativo
        except Exception as ex:
            print(ex)
            return False

    def generate_token(self):
        alphabet = string.ascii_letters + string.digits
        token = ''.join(secrets.choice(alphabet) for i in range(30))
        return token

    @property
    def user_count_bis(self):
        return self.repo_set.exists()

    @property
    def get_created_at(self):
        return self.created_at.strftime(
            FormatDateStringsEnum.DEFAULT_BR_FORMAT_DATETIME.value)

    @property
    def get_updated_at(self):
        return self.updated_at.strftime(
            FormatDateStringsEnum.DEFAULT_BR_FORMAT_DATETIME.value)

    # def get_rud_url(self):
    #     return reverse('api:users_rud', args=(self.id,))
    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'Usuário'
        # permissions = (
        #     ('generate_token', 'Gerar Token de usuário'),
        # )


class AccessHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Usuário')
    access_at = models.DateTimeField(verbose_name='Acessou em')
    ip = models.CharField(max_length=20, verbose_name='IP',
                          blank=True, null=True)
    origin = models.CharField(max_length=255, null=True, blank=True,
                              default=OriginLogin.BACKEND.name,
                              choices=[(i.name, i.value) for i in OriginLogin])

    def __str__(self):
        to_format_br = str(self.access_at.strftime(
            FormatDateStringsEnum.DEFAULT_BR_FORMAT_DATETIME.value))
        return f"{self.user} - {to_format_br}"

    class Meta:
        verbose_name = 'Histórico de Acesso'
        verbose_name_plural = 'Históricos de Acesso'


class ApiRequests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Usuário')
    token = models.CharField(max_length=255, null=True, blank=True,
                             editable=False)
    view_data_post = models.TextField(max_length=5000, null=True, blank=True,
                                      editable=False, verbose_name='Data Post')
    view_data_get = models.TextField(max_length=5000, null=True, blank=True,
                                     editable=False, verbose_name='Data Get')
    view_query_params_get = models.TextField(max_length=5000, null=True,
                                             blank=True, editable=False,
                                             verbose_name='Url Params')
    view_basename = models.CharField(max_length=100, null=True, blank=True,
                                     editable=False)
    view_action = models.CharField(
        max_length=100, null=True, blank=True, editable=False,
        verbose_name='Action da view')
    view_pk = models.CharField(max_length=100, null=True,
                               blank=True, editable=False,
                               verbose_name='Chave Primária')
    view_method = models.CharField(max_length=10, null=True, blank=True,
                                   editable=False, verbose_name='Verbo Http')
    requested_at = models.DateTimeField(auto_now_add=True,
                                        verbose_name='Requisição em')

    def __str__(self):
        to_format_br = str(self.requested_at.strftime(
            FormatDateStringsEnum.DEFAULT_BR_FORMAT_DATETIME.value))
        return f"{self.user} - {to_format_br}"

    class Meta:
        verbose_name = 'Requisição de API'
        verbose_name_plural = 'Requisições de API'


class LoggedUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Usuário')
    logged_at = models.DateTimeField(auto_now_add=True,
                                     verbose_name='Logado desde')

    def __str__(self):
        to_format_br = str(self.logged_at.strftime(
            FormatDateStringsEnum.DEFAULT_BR_FORMAT_DATETIME.value))
        return f"{self.user} - {to_format_br}"

    class Meta:
        verbose_name = _('Usuário Logado')
        verbose_name_plural = _('Usuários logados')


# class CustomLogEntry(LogEntry):
#
#    def type(self):
#        if self.is_addition():
#            return _("Adicionado")
#        elif self.is_change():
#            return _("Modificado")
#        elif self.is_deletion():
#            return _("Deletado")
#        else:
#            return '-'
#
#    type.short_description = _('Tipo de alteração')
#    type.allow_tags = True
#
#    class Meta:
#        verbose_name = _('custom log entry')
#        verbose_name_plural = _('custom log entries')
#        db_table = 'django_admin_custom_log'
#        ordering = ['-action_time']
