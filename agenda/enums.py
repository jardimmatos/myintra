from enum import Enum
from django.utils.translation import gettext as _

class StatusReservaEnum(Enum):
    """"""
    OPENED = _('Aberto')
    PENDING = _('Pendente')
    CANCELLED = _('Cancelado')