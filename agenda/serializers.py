from .tasks import agenda_notificar_email, agenda_registra_log
from base.tasks import task_send_teams_channel, TeamsTemplates
from .mail_templates import template_abertura_reserva
from datetime import datetime
from django.utils.translation import gettext as _
from rest_framework import serializers
from . import models
from django.db import transaction
from users.serializers import UserSimpleSerializer
from base.enums import ActionEnum, LogTypeEnum, AppEnum, FormatDateStringsEnum
from rest_framework.validators import UniqueTogetherValidator
from base.utils import call_ws, register_gateway

class FinalidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Finalidade
        exclude = ('created_at','updated_at','created_by', 'updated_by',)

    def create(self, validated_data):
        with transaction.atomic():
            if not validated_data.get('descricao', None):
                raise serializers.ValidationError(_('Descrição é obrigatório'))

            # Stamps
            validated_data['created_by'] = self.context.get('request').user
            validated_data['created_at'] = datetime.now()

            obj = self.Meta.model(**validated_data)
            obj.save()

            return obj

    def update(self, instance, validated_data):
        with transaction.atomic():
            validated_data['updated_by'] = self.context.get('request').user or instance.updated_by
            validated_data['updated_at'] = datetime.now()
            
            self.Meta.model.objects.filter(pk=instance.pk).update(**validated_data)
            instance = self.Meta.model.objects.get(pk=instance.pk)

            return instance


class TipoEspacoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TipoEspaco
        exclude = ('created_at','updated_at','created_by', 'updated_by',)

    def create(self, validated_data):
        with transaction.atomic():
            if not validated_data.get('descricao', None):
                raise serializers.ValidationError(_('Descrição é obrigatório'))

            # Stamps
            validated_data['created_by'] = self.context.get('request').user
            validated_data['created_at'] = datetime.now()

            obj = self.Meta.model(**validated_data)
            obj.save()

            return obj

    def update(self, instance, validated_data):
        with transaction.atomic():
            validated_data['updated_by'] = self.context.get('request').user or instance.updated_by
            validated_data['updated_at'] = datetime.now()
            
            self.Meta.model.objects.filter(pk=instance.pk).update(**validated_data)
            instance = self.Meta.model.objects.get(pk=instance.pk)

            return instance


class RegraWeekdayEnumSerializer(serializers.ModelSerializer):
    weekday_enums = serializers.SerializerMethodField()

    def get_weekday_enums(self, obj):
        return obj.weekday_enums()

    class Meta:
        model = models.Regra
        fields = ('weekday_enums',)
        read_only_fields = ['weekday_enums']


class RegraSerializer(serializers.ModelSerializer):
    week_day_name = serializers.SerializerMethodField()

    def get_week_day_name(self, obj):
        return obj.week_day_name 

    class Meta:
        model = models.Regra
        validators = [
            UniqueTogetherValidator(
                message="Já existe uma restrição com os parâmetros informados. ",
                queryset=model.objects.all(),
                fields=['week_day', 'start_time', 'end_time']
            )
        ]

        #fields = '__all__'
        exclude = ('created_at','updated_at','created_by', 'updated_by',)
        read_only_fields = ['week_day_name']

    def create(self, validated_data):
        if validated_data.get('week_day', None) == None:
            raise serializers.ValidationError(_('Dia da semana não informado'))
        
        if not validated_data.get('start_time', None):
            raise serializers.ValidationError(_('Horário início não informado'))
        
        if not validated_data.get('end_time', None):
            raise serializers.ValidationError(_('Horário final não informado'))

        # Stamps
        validated_data['created_by'] = self.context.get('request').user
        validated_data['created_at'] = datetime.now()

        obj = self.Meta.model(**validated_data)
        obj.save()

        return obj

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context.get('request').user or instance.updated_by
        validated_data['updated_at'] = datetime.now()
        
        self.Meta.model.objects.filter(pk=instance.pk).update(**validated_data)
        return instance


class EspacoSerializer(serializers.ModelSerializer):
    tipo_espaco_object = TipoEspacoSerializer(many=False, read_only=True)
    gestores_objects = UserSimpleSerializer(many=True, read_only=True)
    admins_objects = UserSimpleSerializer(many=True, read_only=True)
    regras_objects = RegraSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.Espaco
        fields = '__all__'
        
        read_only_fields = [
            'gestores_objects', 'admins_objects', 'regras_objects', 'tipo_espaco_object'
        ]
    
    def create(self, validated_data):
        with transaction.atomic():
            # Tipo de Espaço obrigatório
            if not validated_data.get('gestores', None):
                raise serializers.ValidationError(_('Gestor(es) não informado(s)'))

            if not validated_data.get('tipo_espaco', None):
                raise serializers.ValidationError(_('Tipo de espaço não informado'))
            
            # Stamps
            request = self.context.get('request')
            validated_data['created_by'] = self.context.get('request').user
            validated_data['created_at'] = datetime.now()

            # m2m
            regras = validated_data.pop('regras', [])
            gestores = validated_data.pop('gestores', [])
            admins = validated_data.pop('admins', [])

            obj = self.Meta.model(**validated_data)
            obj.save()

            # set m2m
            obj.regras.set(regras)
            obj.gestores.set(gestores)
            obj.admins.set(admins)
            by = self.context.get('request').user
        msg = '{0} criou um novo espaço {1}'.format( by.get_full_name(), obj.descricao )
        agenda_registra_log.delay({
            'log':          msg, 
            'log_action':   ActionEnum.CREATE.name, 
            'log_at':       f'{datetime.now()}', 
            'log_type':     LogTypeEnum.DEBUG.name,
            'log_app':      AppEnum.AGENDALABS.name,
            'log_model':    'Espaco', 
        })
        register_gateway(request, msg, 'AgendaLabs')

        
        return obj

    def update(self, instance, validated_data):
        with transaction.atomic():
            # print('espaco update validated_data', validated_data)
            request = self.context.get('request')
            validated_data['updated_by'] = self.context.get('request').user or instance.updated_by
            validated_data['updated_at'] = datetime.now()
            
            # m2m
            regras = validated_data.pop('regras', None)
            gestores = validated_data.pop('gestores', None)
            admins = validated_data.pop('admins', None)

            # update fields
            self.Meta.model.objects.filter(pk=instance.pk).update(**validated_data)
            
            instance = self.Meta.model.objects.get(pk=instance.pk)

            if regras:
                instance.regras.set(regras)

            if gestores:
                instance.gestores.set(gestores)

            if admins:
                instance.admins.set(admins)
            
            instance.save()
            # agenda_notificar_email.delay({'teste':'testando'})
            by = self.context.get("request").user
            msg = '{0} alterou o espaço {1}'.format(
                by.username + ' - ' + by.get_full_name(),
                instance.descricao
            )
            agenda_registra_log.delay({
                'log':          msg,
                'log_action':   ActionEnum.UPDATE.name, 
                'log_at':       f'{datetime.now()}', 
                'log_type':     LogTypeEnum.DEBUG.name,
                'log_app':      AppEnum.AGENDALABS.name,
                'log_model':    'Espaco', 
                'log_reserva':  instance.id.hex
            })
            register_gateway(request, msg, 'AgendaLabs')

            return instance


class EspacoSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Espaco
        fields = (
            'id',
            'descricao',
            'color',
            "instrucoes_espaco",
        )


class ReservaSerializer(serializers.ModelSerializer):
    date_start_end = serializers.SerializerMethodField()
    espaco_object = EspacoSimpleSerializer(many=False, read_only=True)
    finalidade_object = FinalidadeSerializer(many=False, read_only=True)
    status_color_hexadecimal = serializers.SerializerMethodField()
    status_color_classname = serializers.SerializerMethodField()
    status_andamento = serializers.SerializerMethodField()

    def get_status_andamento(self, obj):
        return obj.status_andamento

    def get_status_color_hexadecimal(self, obj):
        return obj.status_color_hexadecimal
    
    def get_status_color_classname(self, obj):
        return obj.status_color_classname

    def get_date_start_end(self, obj):
        return obj.date_start_end

    class Meta:
        model = models.Reserva
        fields = [
            'id',
            'responsavel',
            'titulo',
            'espaco',
            'finalidade',
            'date',
            'start',
            'end',
            'participantes',
            'arquivos',
            'observacao',
            'status_reserva',
            'status_descricao',
            'date_start_end',
            'espaco_object',
            'finalidade_object',
            'status_andamento', 
            'status_color_hexadecimal',
            'status_color_classname',
        ]
        read_only_fields = [
            'created_by','updated_by',
            'status_andamento', 
            'status_color_hexadecimal',
            'status_color_classname',
            'date_start_end'
            ]
    
    def create(self, validated_data):
        with transaction.atomic():
            # print('validated_data Reserva',validated_data)
            
            # Tipo de Finalidade obrigatória
            if not validated_data.get('finalidade', None):
                raise serializers.ValidationError(_('Finalidade não informada!'))
            
            # Tipo de Espaço obrigatório
            if not validated_data.get('espaco', None):
                raise serializers.ValidationError(_('Espaço não informado!'))
            
            # Stamps
            request = self.context.get('request')
            validated_data['created_by'] = self.context.get('request').user
            validated_data['created_at'] = datetime.now()
            
            # Set Format DB DATE
            #date = validated_data.pop('date', None)
            #if date:
            #    validated_data['date'] = datetime.strptime(date, FormatDateStringsEnum.DEFAULT_DB_FORMAT_DATE.value).date()

            arquivos = validated_data.pop('arquivos', [])

            obj = self.Meta.model(**validated_data)
            obj.status_reserva = None
            try:
                obj.clean()
            except Exception as v:
                # print('v',v)
                try:
                    # obter as keys do objeto message_dict
                    indexes = list(v.message_dict.keys())
                    # se existir key
                    if len(indexes):
                        # exibir a mensagem do primeiro erro ([0]))
                        msg = v.message_dict[indexes[0]]
                        raise serializers.ValidationError(msg, code=400)
                except Exception as ex:
                        msg = str(v)
                        raise serializers.ValidationError(msg, code=400)
                
            obj.save()
            user = validated_data.get('created_by')
            espaco = validated_data.get('espaco')
            data = validated_data.get('date').strftime(FormatDateStringsEnum.DEFAULT_BR_FORMAT_DATE.value)
            start = validated_data.get('start')

            msg = 'Nova reserva registrada no Espaço {0} para {1} às {2} por {3}'.format(
                                    espaco.descricao, 
                                    data, 
                                    start, 
                                    user.first_name)
            register_gateway(request, msg, 'AgendaLabs')
            call_ws('room_channel_reservas', msg, 'RESERVA-CREATED', notify=True)
            if arquivos:
                obj.arquivos.set(arquivos)

        # TASK LOG
        agenda_registra_log.delay({
            'log':          '{0} registrou uma reserva no espaço {1} para o dia {2}'.format(
                                obj.responsavel,
                                obj.espaco.descricao,
                                obj.date_start_end
                            ), 
            'log_action':   ActionEnum.CREATE.name, 
            'log_at':       f'{datetime.now()}', 
            'log_type':     LogTypeEnum.VIEW.name,
            'log_app':      AppEnum.AGENDALABS.name,
            'log_model':    'Reserva', 
            'log_reserva':  obj.id.hex
        })

        # TASK NOTIFICAÇÃO - EMAIL
        if obj.espaco.enviar_notificacao:
            params = template_abertura_reserva(obj)
            agenda_notificar_email.delay(params)

        # TASK NOTIFICAÇÃO - TEAMS
        channels = obj.espaco.teams.filter(ativo=True)
        for channel in channels:
            options = {
                'template': TeamsTemplates.TEMPLATE_FACTS, 
                'channel': channel.webhook, 
                'color': obj.status_color_hexadecimal.replace('#', ''), 
                'title': obj.espaco.__str__(), 
                'subtitle': obj.titulo, 
                'messages': [
                    [f'Responsável', obj.responsavel],
                    ['Data/hora', obj.date_start_end],
                    ['Finalidade', obj.finalidade.descricao],
                    ['Situação', obj.get_status()],
                    ['Observações', obj.observacao],
                    ['Identificador', obj.id.hex],
                ]
            }
            
            task_send_teams_channel.delay(options) # envio imediato
            # task_send_teams_channel.apply_async(
            #     eta= espaco.inicio, 
            #     kwargs= {'options':options}
            # )

        return obj

    def update(self, instance, validated_data):
        with transaction.atomic():
            request = self.context.get('request')
            validated_data['updated_by'] = self.context.get('request').user or instance.updated_by
            validated_data['updated_at'] = datetime.now()
            
            validated_data.pop('date', None)
            validated_data.pop('start', None)
            validated_data.pop('end', None)
            validated_data.pop('status_reserva', None)
            # m2m
            arquivos = validated_data.pop('arquivos', None)

            # update fields
            self.Meta.model.objects.filter(pk=instance.pk).update(**validated_data)
            
            instance = self.Meta.model.objects.get(pk=instance.pk)

            # set m2m
            if arquivos:
                instance.arquivos.set(arquivos)
            
            by = self.context.get('request').user
            # print('register log UPDATE SERIALIZER')
            msg = '{0} atualizou uma reserva no espaço {1} do dia {2}'.format(
                                        by.username +' - ' + by.get_full_name(),
                                        instance.espaco.descricao,
                                        instance.date_start_end
                                )
            agenda_registra_log.delay({
                'log':          msg,
                'log_action':   ActionEnum.UPDATE.name, 
                'log_at':       f'{datetime.now()}', 
                'log_type':     LogTypeEnum.VIEW.name,
                'log_app':      AppEnum.AGENDALABS.name,
                'log_model':    'Reserva', 
                'log_reserva':  instance.id.hex
            })
            register_gateway(request, msg, 'AgendaLabs')
            return instance


class ReservaDetalheSerializer(serializers.ModelSerializer):
    status_andamento = serializers.SerializerMethodField()
    espaco = EspacoSerializer(many=False, read_only=True)
    finalidade = FinalidadeSerializer(many=False, read_only=True)
    # arquivos = ArquivoSerializer(many=True, read_only=True)
    created_by = UserSimpleSerializer(many=False, read_only=True)
    updated_by = UserSimpleSerializer(many=False, read_only=True)
    date_start_end = serializers.SerializerMethodField()
    status_color_hexadecimal = serializers.SerializerMethodField()
    status_color_classname = serializers.SerializerMethodField()

    def get_status_andamento(self, obj):
        return obj.status_andamento
    
    def get_status_color_hexadecimal(self, obj):
        return obj.status_color_hexadecimal
    
    def get_status_color_classname(self, obj):
        return obj.status_color_classname
    
    def get_date_start_end(self, obj):
        return obj.date_start_end

    class Meta:
        model = models.Reserva
        fields = '__all__'
        read_only_fields = ['created_at','updated_at','created_by','updated_by',
            'status_atual',
            'status_color_hexadecimal',
            'status_color_classname'
        ]


class LogAgendaSerializer(serializers.ModelSerializer):
    reserva_object = ReservaDetalheSerializer(many=False, read_only=True)

    class Meta:
        model = models.LogAgenda
        fields = '__all__'
        read_only_fields = ('reserva_object',)