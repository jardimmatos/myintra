from datetime import datetime
from rest_framework_simplejwt import serializers, tokens
from rest_framework import exceptions
# from rest_framework import serializers as drf_serializer
from base.enums import OriginLogin
# from base.models import LogSistema
from users.tasks import set_user_access_history
from users.serializers import UserFullSerializer
from django.contrib.auth import authenticate


# API Login
class MyTokenObtainPairSerializer(serializers.TokenObtainSerializer):

    def autenticar_com_terceiro(self, username, password):
        usuario = None
        # TODO: Lógica aqui
        raise exceptions.ValidationError("Sem autenticação de terceiros")
        return usuario

    @classmethod
    def get_token(cls, user):
        return tokens.RefreshToken.for_user(user)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        try:
            ip = self.context.get('request').META.get('REMOTE_ADDR')
        except Exception:
            ip = ''

        usuario = None
        try:
            usuario = self.autenticar_com_terceiro(username, password)
        except Exception:
            # Em caso de registro de logs sobre a autenticação de terceiros
            # log = LogSistema(
            #     path='intranet > base > token_pair_serializers >
            # MyTokenObtainPairSerializer > validate',
            #     log = f'Usuário {str(usuario.username)} acessou quando
            # houve falha de terceiro: {str(ex)}'
            # )
            # log.save()
            usuario = authenticate(username=username, password=password)

        if not usuario:
            raise exceptions.ValidationError('Usuário não identificado')

        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        acesso_em = f'{datetime.now()}'

        set_user_access_history.delay(
            self.user.id.hex,
            OriginLogin.FRONTEND.name, acesso_em, ip)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # incluir usuário junto ao token
        user_auth = UserFullSerializer(usuario)
        data['auth'] = user_auth.data
        return data
