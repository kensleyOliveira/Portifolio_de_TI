class TelemetriaDomainException(Exception):
    """Classe base para todas as exceções de domínio do sistema de telemetria."""
    pass

class LeituraIncompletaException(TelemetriaDomainException):
    """Lançada quando dados obrigatórios (temperatura ou umidade) estão ausentes."""
    def __init__(self, mensagem="Temperatura e umidade são campos obrigatórios."):
        self.mensagem = mensagem
        super().__init__(self.mensagem)

class TemperaturaInvalidaException(TelemetriaDomainException):
    """Lançada quando a temperatura reportada pelo sensor está fora do limite físico aceitável."""
    def __init__(self, temperatura, mensagem="Temperatura fora dos limites aceitáveis para o microclima."):
        self.temperatura = temperatura
        self.mensagem = f"{mensagem} Valor lido: {temperatura}°C"
        super().__init__(self.mensagem)

class UmidadeInvalidaException(TelemetriaDomainException):
    """Lançada quando a umidade está fora do limite percentual (0 a 100)."""
    def __init__(self, umidade, mensagem="Umidade deve estar entre 0% e 100%."):
        self.umidade = umidade
        self.mensagem = f"{mensagem} Valor lido: {umidade}%"
        super().__init__(self.mensagem)