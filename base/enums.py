from enum import Enum
from django.utils.translation import gettext as _


class FormatDateStringsEnum(Enum):
    DEFAULT_BR_FORMAT_DATETIME = '%d/%m/%Y %H:%M:%S'
    DEFAULT_DB_FORMAT_DATETIME = '%Y-%m-%d %H:%M:%S'
    DEFAULT_BR_FORMAT_DATE = '%d/%m/%Y'
    DEFAULT_DB_FORMAT_DATE = '%Y-%m-%d'
    DEFAULT_FORMAT_TIME = '%H:%M'


class DayOfWeekIndexEnum(Enum):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6


class DayOfWeekNameEnum(Enum):
    MON = _('Segunda-feira')
    TUE = _('Terça-feira')
    WED = _('Quarta-feira')
    THU = _('Quinta-feira')
    FRI = _('Sexta-feira')
    SAT = _('Sábado')
    SUN = _('Domingo')


class OriginLogin(Enum):
    # Registrar se o Login foi no Backend (django admin)
    BACKEND = 'Backend'
    # Registrar se o Login foi no Frontend (node)
    FRONTEND = 'Frontend'


class LogTypeEnum(Enum):
    """Apenas para registro de tipos de Logs"""
    DEBUG = 'Debug'
    # Exibir log no front
    VIEW = 'Visualização'
    # Apenas acompanhamento de erro
    ERROR = 'Error'


class ActionEnum(Enum):
    """ Para uso em logs de cruds """
    CREATE = 'Adicionar'
    UPDATE = 'Atualizar'
    DELETE = 'Remover'
    VIEW = 'Visualizar'


class AppEnum(Enum):
    """ Para uso em logs e especificação de APP """
    BASE = 'Base'
    AGENDALABS = 'AgendaLabs'
    COFRE = 'Cofre'
    NOTIFICATIONS = 'Notificações'
    RECURSOS_ATIVOS = 'Recursos'
    REPO_BI = 'Repositórios BI'
    USERS = 'Usuários'


class GlobalChannelsEnum(Enum):
    CREATED = "CREATED"
    CHANGED = "CHANGED"
    DELETED = "DELETED"
    REFRESH = "REFRESH"
    LOADING = "LOADING"
    LOADED = "LOADED"
