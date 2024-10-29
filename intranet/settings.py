import os
import datetime
from pathlib import Path
from celery.schedules import crontab


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django--x@cpstc-5)lde=zrc^r^&l=7n8j7h+=ex%4y!rp#&t#yy)_4q*'

DEBUG = False

ALLOWED_HOSTS = []

DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MY_LIBS = [
    'drf_yasg',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'import_export',
    'channels',
    'django_quill'
]

MY_APPS = [
    'base',
    'users',
    'cofre',
    'repositoriobi',
    'agenda',
    'notifications',
    'wiki',
    'infraestrutura',
    'atendimento',
]

INSTALLED_APPS = DEFAULT_APPS + MY_LIBS + MY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'intranet.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

CORS_ALLOWED_ORIGINS = []

# CELERY/REDIS
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Fortaleza'

# parâmetro de upload do Django
# DATA_UPLOAD_MAX_MEMORY_SIZE = 29360128
# FILE_UPLOAD_MAX_MEMORY_SIZE = 29360128

#WSGI_APPLICATION = 'intranet.wsgi.application'
# Channels

ASGI_APPLICATION = 'intranet.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('localhost', 6379)],
        },
    },
    'ROUTING': 'base.base_routing.application',
}

AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
    # { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    # { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    # { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    # { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 54000

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = "America/Fortaleza"
USE_I18N = True
USE_L10N = True
USE_TZ = False
USE_TZ = True
STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static_root') ]

# STATIC_ROOT = 'var/static_root/'
# STATICFILES_DIRS = ['static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'users.authentications_mixins.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'base.utils.CustomParamPagination', #customized with url parameter page_size=?
    'PAGE_SIZE': 10,
    'PAGINATE_BY_PARAM': 'page_size',
    
    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle',
    # ],
    # Habilitar restrição de limite de requisições de API
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '50/min',
    #     'user': '1000/day',
    # },
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',

)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SIMPLE_JWT = {
    # especifica por quanto tempo os tokens de acesso são válidos. 
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(hours=4),

    # especifica por quanto tempo os tokens de atualização são válidos. 
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(hours=24),
    
    #Quando definido como True, se um token de atualização for enviado para o TokenRefreshView, um novo token de atualização será retornado junto com o novo token de acesso. Esse novo token de atualização será fornecido por meio de uma chave “refresh” na resposta JSON. Os novos tokens de atualização terão um tempo de expiração renovado que é determinado pela adição do timedelta na REFRESH_TOKEN_LIFETIME configuração à hora atual quando a solicitação é feita. Se o aplicativo de lista negra estiver em uso e a BLACKLIST_AFTER_ROTATIONconfiguração estiver definida como True, os tokens de atualização enviados para a visualização de atualização serão adicionados à lista negra.
    'ROTATE_REFRESH_TOKENS': True,
    
    #Quando definido como True, faz com que os tokens de atualização enviados para o TokenRefreshView sejam adicionados à lista negra se o aplicativo da lista negra estiver em uso e a ROTATE_REFRESH_TOKENS configuração estiver definida como True. Você precisa adicionar 'rest_framework_simplejwt.token_blacklist',ao seu INSTALLED_APPSarquivo de configurações para usar essa configuração.
    'BLACKLIST_AFTER_ROTATION': False,

    #O algoritmo da biblioteca PyJWT que será usado para realizar operações de assinatura/verificação em tokens. Para usar assinatura e verificação HMAC simétrica, os seguintes algoritmos podem ser usados: 'HS256', 'HS384', 'HS512'. Quando um algoritmo HMAC é escolhido, a SIGNING_KEYconfiguração será usada tanto como chave de assinatura quanto como chave de verificação. Nesse caso, a VERIFYING_KEYconfiguração será ignorada. Para usar assinatura e verificação RSA assimétrica, os seguintes algoritmos podem ser usados: 'RS256', 'RS384', 'RS512'. Quando um algoritmo RSA é escolhido, a SIGNING_KEYconfiguração deve ser definida como uma string que contém uma chave privada RSA. Da mesma forma, a VERIFYING_KEYconfiguração deve ser definida como uma string que contém uma chave pública RSA.
    'ALGORITHM': 'HS256',

    #A chave de assinatura que é usada para assinar o conteúdo dos tokens gerados. Para assinatura HMAC, deve ser uma string aleatória com pelo menos tantos bits de dados quantos forem exigidos pelo protocolo de assinatura. Para assinatura RSA, deve ser uma string que contenha uma chave privada RSA de 2048 bits ou mais. Como o Simple JWT usa como padrão a assinatura HMAC de 256 bits, a SIGNING_KEYconfiguração padrão é o valor da SECRET_KEYconfiguração do seu projeto django. Embora esse seja o padrão mais razoável que o Simple JWT pode fornecer, é recomendável que os desenvolvedores alterem essa configuração para um valor independente da chave secreta do projeto django. Isso facilitará a alteração da chave de assinatura usada para tokens caso ela seja comprometida.
    'SIGNING_KEY': SECRET_KEY,
    
    #Quando definido como True, o campo last_login na tabela auth_user é atualizado no login (TokenObtainPairView).
    #Aviso: A atualização do last_login aumentará drasticamente o número de transações do banco de dados. As pessoas que abusam das visualizações podem tornar o servidor lento e isso pode ser uma vulnerabilidade de segurança. Se você realmente quer isso, estrangule o endpoint com DRF, no mínimo.
    'UPDATE_LAST_LOGIN': False,

    #A chave de verificação que é usada para verificar o conteúdo dos tokens gerados. Se um algoritmo HMAC tiver sido especificado pela ALGORITHMconfiguração, a VERIFYING_KEYconfiguração será ignorada e o valor da SIGNING_KEY configuração será usado. Se um algoritmo RSA tiver sido especificado pela ALGORITHMconfiguração, a VERIFYING_KEYconfiguração deverá ser definida como uma string que contenha uma chave pública RSA.
    'VERIFYING_KEY': None,

    #O público afirma estar incluído em tokens gerados e/ou validado em tokens decodificados. Quando definido como None, esse campo é excluído dos tokens e não é validado.
    'AUDIENCE': None,

    #O emissor afirma ser incluído em tokens gerados e/ou validado em tokens decodificados. Quando definido como None, esse campo é excluído dos tokens e não é validado.
    'ISSUER': None,

    #O JWK_URL é usado para resolver dinamicamente as chaves públicas necessárias para verificar a assinatura de tokens. Ao usar Auth0, por exemplo, você pode definir isso como ' https://yourdomain.auth0.com/.well-known/jwks.json '. Quando definido como None, esse campo é excluído do back-end do token e não é usado durante a validação.
    'JWK_URL': None,

    #Leeway é usado para dar alguma margem ao tempo de expiração. Isso pode ser um número inteiro por segundos ou um datetime.timedelta. Consulte https://pyjwt.readthedocs.io/en/latest/usage.html#expiration-time-claim-exp para obter mais informações.
    'LEEWAY': 0,

    #Os tipos de cabeçalho de autorização que serão aceitos para visualizações que exigem autenticação. Por exemplo, um valor de 'Bearer'significa que as exibições que exigem autenticação procurariam um cabeçalho com o seguinte formato: . Essa configuração também pode conter uma lista ou tupla de tipos de cabeçalho possíveis (por exemplo , ). Se uma lista ou tupla for usada dessa maneira e a autenticação falhar, o primeiro item da coleção será usado para construir o cabeçalho “WWW-Authenticate” na resposta.Authorization: Bearer <token>('Bearer', 'JWT')
    'AUTH_HEADER_TYPES': ('Bearer',),

    #O nome do cabeçalho de autorização a ser usado para autenticação. O padrão é HTTP_AUTHORIZATIONque aceitará o Authorizationcabeçalho na solicitação. Por exemplo, se você quiser usar X_Access_Tokenno cabeçalho de suas solicitações, especifique o AUTH_HEADER_NAMEque está HTTP_X_ACCESS_TOKENem suas configurações.
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',

    #O campo do banco de dados do modelo de usuário que será incluído nos tokens gerados para identificar os usuários. Recomenda-se que o valor dessa configuração especifique um campo que normalmente não muda depois que seu valor inicial é escolhido. Por exemplo, especificar um campo “nome de usuário” ou “e-mail” seria uma má escolha, pois o nome de usuário ou e-mail de uma conta pode mudar dependendo de como o gerenciamento de contas em um determinado serviço é projetado. Isso pode permitir que uma nova conta seja criada com um nome de usuário antigo enquanto um token existente ainda é válido, que usa esse nome de usuário como identificador de usuário.
    'USER_ID_FIELD': 'id',

    #A declaração em tokens gerados que serão usados ​​para armazenar identificadores de usuário. Por exemplo, um valor de configuração de 'user_id'significaria que os tokens gerados incluem uma declaração “user_id” que contém o identificador do usuário.
    'USER_ID_CLAIM': 'user_id',

    #Chamável para determinar se o usuário tem permissão para autenticar. Essa regra é aplicada depois que um token válido é processado. O objeto de usuário é passado para o callable como um argumento. A regra padrão é verificar se o is_active sinalizador ainda está True. O callable deve retornar um booleano, Truese autorizado, Falsecaso contrário, resultando em um código de status 401.
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    #Uma lista de caminhos de ponto para classes que especificam os tipos de token que têm permissão para provar a autenticação. Mais sobre isso na seção "Tipos de token" abaixo.
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),

    #O nome da declaração que é usado para armazenar o tipo de um token. Mais sobre isso na seção "Tipos de token" abaixo.
    'TOKEN_TYPE_CLAIM': 'token_type',

    #TOKEN_USER_CLASS
    #Um objeto de usuário sem estado que é apoiado por um token validado. Usado apenas para o back-end de autenticação JWTStatelessUserAuthentication. O valor é um caminho pontilhado para sua subclasse de rest_framework_simplejwt.models.TokenUser, que também é o padrão.
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    #O nome da declaração que é usado para armazenar o identificador exclusivo de um token. Esse identificador é usado para identificar tokens revogados no aplicativo de lista negra. Pode ser necessário, em alguns casos, usar outra declaração além da declaração padrão “jti” para armazenar tal valor.
    'JTI_CLAIM': 'jti',

    #O nome da declaração que é usado para armazenar o tempo de expiração do período de atualização de um token deslizante. Mais sobre isso na seção "Tokens deslizantes" abaixo.
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    
    #Um datetime.timedeltaobjeto que especifica por quanto tempo os tokens deslizantes são válidos para provar a autenticação. Esse timedeltavalor é adicionado à hora UTC atual durante a geração do token para obter o valor de declaração “exp” padrão do token. Mais sobre isso na seção "Tokens deslizantes" abaixo.
    'SLIDING_TOKEN_LIFETIME': datetime.timedelta(minutes=5),
    
    #Um datetime.timedeltaobjeto que especifica por quanto tempo os tokens deslizantes são válidos para serem atualizados. Esse timedeltavalor é adicionado à hora UTC atual durante a geração do token para obter o valor de declaração “exp” padrão do token. Mais sobre isso na seção "Tokens deslizantes" abaixo.
    'SLIDING_TOKEN_REFRESH_LIFETIME': datetime.timedelta(days=1),
}

# Parametrização de Logs
#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': True,
#    'formatters': {
#        'simple': {
#            'format': '%(levelname)s %(message)s',
#             'datefmt': '%y %b %d, %H:%M:%S',
#            },
#        },
#    'handlers': {
#        'console': {
#            'level': 'DEBUG',
#            'class': 'logging.StreamHandler',
#            'formatter': 'simple'
#        },
#        'celery': {
#            'level': 'DEBUG',
#            'class': 'logging.handlers.RotatingFileHandler',
#            'filename': 'celery.log',
#            'formatter': 'simple',
#            'maxBytes': 1024 * 1024 * 500,  # 500 mb
#        },
#    },
#    'loggers': {
#        'celery': {
#            'handlers': ['celery', 'console'],
#            'level': 'DEBUG',
#        },
#    }
#}

try:
    from .local_settings import *
except:
    print('Erro ao carregar env')
    pass
