from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from email.utils import formataddr
from django.template import Template, Context
from django.core.mail import send_mail, EmailMessage


class Email():
    
    def __init__(self, assunto='Notificação Intranet', content='', to=[], bcc=[], cc=[], reply_to=[], template=None, from_email='MyIntranet <jr.jardimmatos@gmail.com>'):
        self.assunto = assunto
        self.content = content
        self.to = to
        self.bcc = bcc
        self.cc = cc
        self.reply_to = reply_to
        self.template = template
        self.from_email = from_email
    
    def enviar(self):
        if self.template == None:
            return
        
        if len(self.to) == 0:
            return
        
        body = render_to_string(self.template, {'content': self.content})
        
        msg = EmailMessage(self.assunto, mark_safe(body), from_email=self.from_email,to=self.to,bcc=self.bcc,cc=self.cc, reply_to=self.reply_to)
        msg.content_subtype = 'html'
        msg.send()

def send_template_email(assunto, corpo, para, contexto):
    # Renderizando o corpo do email
    template = Template(corpo)
    context = Context(contexto)
    body = template.render(context)
    from_email = formataddr(('intranet ', 'jr.jardimmatos@gmail.com'))
    email = EmailMessage(
        subject=assunto,
        body=body,
        from_email=from_email,
        to=para,
        bcc=['jr.jardimmatos@gmail.com'], # acompanhamento de testes em cópia oculta
    )
    
    # Enviando o email
    email.send()
