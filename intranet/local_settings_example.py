import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Utilizando banco de dados MySQL em container
DATABASES = {
    'default': {
        "ENGINE": 'django.db.backends.mysql',
        "NAME": 'myintra',
        "USER": 'myintra',
        "PASSWORD": 'myintra_pwd!',
        "HOST": '127.0.0.1',
        "PORT": 3326,
    },
}

DEBUG = False

ALLOWED_HOSTS = []

CORS_ALLOWED_ORIGINS = []

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # send via console
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # send via SMTP
EMAIL_SUBJECT_PREFIX = 'Minha Intranet'
EMAIL_HOST = ''
EMAIL_PORT = ''
EMAIL_HOST_USER = ''
DEFAULT_FROM_EMAIL = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True



