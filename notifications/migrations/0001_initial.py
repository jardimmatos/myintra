# Generated by Django 3.2.14 on 2024-10-27 20:36

from django.db import migrations, models
import django_quill.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notificacao',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='alterado em')),
                ('titulo', models.CharField(blank=True, max_length=255, null=True, verbose_name='Título')),
                ('text', models.TextField(blank=True, null=True)),
                ('html', models.TextField(blank=True, null=True)),
                ('mensagem', django_quill.fields.QuillField(null=True)),
                ('inicio', models.DateTimeField(null=True, verbose_name='Início')),
                ('fim', models.DateTimeField(blank=True, null=True, verbose_name='Fim')),
            ],
            options={
                'verbose_name': 'Notificação',
                'verbose_name_plural': 'Notificações',
            },
        ),
    ]
