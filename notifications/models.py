from django.db import models
from base.models import TimeStampedModel, TeamsChannel
from django_quill.fields import QuillField


class Notificacao(TimeStampedModel):
    titulo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Título")
    text = models.TextField(blank=True, null=True)
    html = models.TextField(blank=True, null=True)
    mensagem = QuillField(blank=False, null=True)
    inicio = models.DateTimeField(blank=False, null=True, verbose_name="Início")
    fim = models.DateTimeField(blank=True, null=True, verbose_name="Fim")
    # canais_teams = models.ManyToManyField(TeamsChannel, blank=True, verbose_name='Integrar Canal Teams', help_text='Selecionar canais do Teams para disparo de notificação')
    # locais = models.ManyToManyField(Local, verbose_name="Locais", help_text="Locais dos Usuários", blank=True)

    def __str__(self):
        return f'{self.titulo}'
    
    def mist(self):
        # print(dir(self.mensagem))
        return f'\n#3 {self.mensagem.delta} \n#4 {self.mensagem.field} \n#5 {self.mensagem.instance} \n#6 {self.mensagem.json_string} \n#7 {self.mensagem.quill.__dict__}'

    def clean(self):
        self.text = self.mensagem.plain
        self.html = self.mensagem.html
    
    def save(self, *args, **kwargs):
        self.clean()
        #self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'