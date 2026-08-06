from abc import ABC, abstractmethod
from domain.models import LeituraMicroclima

class ITelemetriaRepository(ABC):
    """Contrato que qualquer banco de dados precisará respeitar"""
    @abstractmethod
    def salvar(self, leitura: LeituraMicroclima) -> None:
        pass