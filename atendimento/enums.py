from enum import Enum
from django.utils.translation import gettext as _

class StatusAtendimento(Enum):
    iniciado = 'Iniciado'
    encerrado = 'Encerrado'
    nao_compareceu = 'Não Compareceu'
    chamado = 'Chamado'
    emitido = 'Emitido'
    transferido = 'Transferido'

class ResolucaoAtendimento(Enum):
    pendente = 'Pendente'
    resolvido = 'Resolvido'

class TypeSerials(Enum):
    simple = 'Serializador Simples'
    full = 'Serializador Completo'

class OriginCallFilaSenha(Enum):
    triagem_senha = 0
    proxima_senha = 1
    redirecionar = 2
    encerrar = 3
    atual_atendente = 4
    atendente_logado = 5