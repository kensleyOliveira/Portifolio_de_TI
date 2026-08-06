from domain.models import LeituraMicroclima
from domain.exceptions import TelemetriaDomainException
from application.interfaces import ITelemetriaRepository

class ProcessarLeituraUseCase:
    
    def __init__(self, repository: ITelemetriaRepository):
        self.repository = repository

    def executar(self, payload_dict: dict) -> None:
        try:
            # 1. Instancia e valida a entidade de domínio
            leitura = LeituraMicroclima(
                temperatura=payload_dict.get("temperatura"),
                umidade=payload_dict.get("umidade")
            )
            
            # 2. Persiste a entidade válida
            self.repository.salvar(leitura)
            print(f"Sucesso: Leitura {leitura.temperatura}°C / {leitura.umidade}% registrada.")
            
        except TelemetriaDomainException as e:
            # Captura EXCLUSIVAMENTE violações de regras de negócio.
            # Aqui você pode enviar para uma Dead Letter Queue (DLQ) ou gerar logs de anomalia do hardware.
            print(f"⚠️ Alerta de Negócio (Dado Descartado): {e.mensagem}")
            
        except Exception as e:
            # Captura erros inesperados (ex: queda de banco de dados, falha de rede)
            print(f"❌ Erro Crítico de Sistema: {e}")
            raise e # Repassa o erro de infraestrutura para cima