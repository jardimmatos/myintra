from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import User, ApiRequests
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
# from django.utils.translation import gettext_lazy as _

# created a custom ModelBackend authenticate to auth with only token
class AbstractTokenAuthentication(ModelBackend):

    def authenticate(self, request, token=None):

        try:
            token = request.query_params.get('token')
            auth = get_user_model().objects.exclude(token__isnull=True).get(token = token)
            try:
                # Registrar requisições de API
                if True:
                    data = dict()
                    data['user'] = auth
                    data['token'] = token
                    data['view_data_post'] = str(request.data)
                    data['view_query_params_get'] = str(request.query_params)
                    try:
                        data['view_data_get'] = str(request.parser_context.get('view').get('basename').data)[:5000]
                    except:
                        ...
                    data['view_basename'] = request.parser_context.get('view').basename
                    data['view_action'] = request.parser_context.get('view').action
                    data['view_pk'] = request.parser_context.get('kwargs').get('pk')
                    data['view_method'] = request._request.method
                    ApiRequests.objects.create(**data)
            except Exception as e:
                print('Exceptions on request token Authentication', e)
        except:
            auth = None
        return auth


# create a custom BaseAuthentication to authenticate user with a generated token model field on 
# request with query_param token
class TokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        try:
            auth = User.objects.exclude(token__isnull=True).get(token = request.query_params.get('token'))
        except:
            auth = None

        if not auth:
            msg = 'Token expirado ou não informado'
            raise exceptions.AuthenticationFailed(msg)

        token = auth.token
        backend = AbstractTokenAuthentication()
        user = backend.authenticate(request, token)
        if user is None:
            raise exceptions.AuthenticationFailed('Token inválido.')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('Usuário inativo')

        return (user, None)

