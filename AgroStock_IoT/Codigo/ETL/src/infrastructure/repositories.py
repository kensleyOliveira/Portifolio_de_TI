import time
import mysql.connector
from domain.models import LeituraMicroclima
from application.interfaces import ITelemetriaRepository

class MysqlTelemetriaRepository(ITelemetriaRepository):
       
    def __init__(self, db_config: dict):
        self.config = db_config

    def salvar(self, leitura: LeituraMicroclima) -> None:
        conexao = None
        tentativas = 5
        intervalo = 3 
        
        for tentativa in range(tentativas):
            try:
                # Conecta ao MySQL do Railway
                conexao = mysql.connector.connect(**self.config)
                cursor = conexao.cursor()
                
                # Query adaptada para a estrutura do banco (usando a coluna 'h')
                sql = """
                    INSERT INTO telemetria_microclima (temperatura, h, data_hora) 
                    VALUES (%s, %s, %s);
                """
                valores = (leitura.temperatura, leitura.umidade, leitura.data_hora)
                
                cursor.execute(sql, valores)
                conexao.commit()
                cursor.close()
                break
                
            except Exception as err:
                print(f"⚠️ [Infra] Tentativa {tentativa + 1}/{tentativas} falhou ao conectar ao MySQL no Railway...")
                if tentativa == tentativas - 1:
                    print(f"❌ Erro definitivo de Infraestrutura (MySQL): {err}")
                    raise err
                time.sleep(intervalo) 
                
            finally:
                if conexao and conexao.is_connected():
                    conexao.close()