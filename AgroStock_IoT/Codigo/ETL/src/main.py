import os
import sys
from dotenv import load_dotenv
from infrastructure.repositories import MysqlTelemetriaRepository
from application.use_cases import ProcessarLeituraUseCase
from infrastructure.mqtt_adapter import MqttConsumer

CAMINHO_SRC = os.path.dirname(os.path.abspath(__file__))
CAMINHO_RAIZ = os.path.dirname(CAMINHO_SRC)
CAMINHO_ENV = os.path.join(CAMINHO_RAIZ, '.env.local')

if os.path.exists(CAMINHO_ENV):
    load_dotenv(CAMINHO_ENV)

if __name__ == "__main__":
    print("==================================================")
    print("🚀 Iniciando Pipeline Cloud-Native com DDD (AgroStock)")
    print("==================================================")
        
    # Configurações do Banco de Dados MySQL
    db_config = {
        'host': os.getenv('MYSQLHOST'), 
        'port': int(os.getenv('MYSQLPORT', 3306)), 
        'user': os.getenv('MYSQLUSER'),  
        'password': os.getenv('MYSQLPASSWORD'), 
        'database': os.getenv('MYSQLDATABASE')  
    }

    # Configurações do MQTT HiveMQ
    mqtt_broker = os.getenv('MQTT_BROKER')
    mqtt_port = int(os.getenv('MQTT_PORT', 8883)) 
    mqtt_user = os.getenv('MQTT_USER')
    mqtt_password = os.getenv('MQTT_PASSWORD')
    mqtt_topic = os.getenv('MQTT_TOPIC')
    
    # Validação de Segurança
    if not all([db_config['host'], db_config['password'], mqtt_broker, mqtt_password]):
        print("💥 Erro de Ambiente: Credenciais ausentes.")
        print("Verifique se TODAS as variáveis (MySQL e MQTT) estão cadastradas na aba 'Variables' do Railway.")
        sys.exit(1)

    print(f"📡 Target Broker: {mqtt_broker}:{mqtt_port} | Tópico: '{mqtt_topic}'")
    print(f"🛢️ Target Database Cloud: {db_config['host']} | DB: {db_config['database']}")

    try:
        repositorio_mysql = MysqlTelemetriaRepository(db_config)
        
        caso_de_uso = ProcessarLeituraUseCase(repository=repositorio_mysql)

        consumidor_mqtt = MqttConsumer(
            broker=mqtt_broker,
            port=mqtt_port,
            topic=mqtt_topic,
            user=mqtt_user,
            password=mqtt_password,
            use_case=caso_de_uso
        )
        
        print("🟢 Pipeline em nuvem pronto e escutando a ESP32...")
        print("--------------------------------------------------")
        consumidor_mqtt.iniciar()

    except KeyboardInterrupt:
        print("\n🛑 Encerrando o Pipeline de Telemetria graciosamente...")
        sys.exit(0)
    except Exception as e:
        print(f"💥 Erro crítico na inicialização do sistema: {e}")
        sys.exit(1)