from enum import Enum

class StatusItemCirculacao(Enum):
    DEVOLVIDO_AVARIA = "Devolvido com avaria"
    BAIXADO_NORMAL = "Baixado Normal"
    EM_CIRCULACAO = "Em circulação"
    EXTRAVIADO = "Extravio"
    CIRCULACAO_CANCELADA = "Cancelado"

    @property
    def alias(self):
        if self._name_ == 'DEVOLVIDO_AVARIA': return { 'key': self._name_, 'value': 'Devolvido com Avaria', 'color': 'error' }
        if self._name_ == 'BAIXADO_NORMAL': return { 'key': self._name_, 'value': 'Baixa Normal', 'color': 'success' }
        if self._name_ == 'EM_CIRCULACAO': return { 'key': self._name_, 'value': 'Em Circulação', 'color': 'info' }
        if self._name_ == 'EXTRAVIADO': return { 'key': self._name_, 'value': 'Extravio', 'color': 'error' }
        if self._name_ == 'CIRCULACAO_CANCELADA': return { 'key': self._name_, 'value': 'Cancelado', 'color': 'grey' }
        return self._name_


class StatusDispositivo(Enum):
    AVARIADO = "Avariado"
    EXTRAVIO = "Extravio"
    DISPONIVEL = "Disponível"
    MANUTENCAO = "Em Manutenção"
    EM_CIRCULACAO = "Em Circulação"

    @property
    def alias(self):
        if self._name_ == 'AVARIADO': return { 'key': self._name_, 'value': 'Avaria', 'color': 'error' }
        if self._name_ == 'EXTRAVIO': return { 'key': self._name_, 'value': 'Extravio', 'color': 'error' }
        if self._name_ == 'DISPONIVEL': return { 'key': self._name_, 'value': 'Disponível', 'color': 'success' }
        if self._name_ == 'MANUTENCAO': return { 'key': self._name_, 'value': 'Manutenção', 'color': 'warning' }
        if self._name_ == 'EM_CIRCULACAO': return { 'key': self._name_, 'value': 'Em Circulação', 'color': 'info' }
        return self._name_
    

class StatusCirculacao(Enum):
    ABERTO = "Aberto"
    FINALIZADO = "Finalizado"
    CANCELADO = "Cancelado"
    TRANSFERIDO = "Transferido" # Status apenas utilizado em log
    
    @property
    def alias(self):
        if self._name_ == 'ABERTO': return { 'key': self._name_, 'value': 'Aberto', 'color': 'info' }
        if self._name_ == 'FINALIZADO': return { 'key': self._name_, 'value': 'Finalizado', 'color': 'success' }
        if self._name_ == 'CANCELADO': return { 'key': self._name_, 'value': 'Cancelado', 'color': 'grey' }
        if self._name_ == 'TRANSFERIDO': return { 'key': self._name_, 'value': 'Transferido', 'color': 'warning' }
        return self._name_