import json
import ssl
import certifi
import paho.mqtt.client as mqtt
from application.use_cases import ProcessarLeituraUseCase

class MqttConsumer:
    """Consumidor MQTT que atua como porta de entrada (Driver) seguro para o HiveMQ Cloud"""
    
    def __init__(self, broker: str, port: int, topic: str, user: str, password: str, use_case: ProcessarLeituraUseCase):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.use_case = use_case
        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
        self.client.username_pw_set(user, password)
    
        self.client.tls_set(
            ca_certs=certifi.where(),
            tls_version=ssl.PROTOCOL_TLS_CLIENT, # Força o handshake seguro como cliente
            cert_reqs=ssl.CERT_REQUIRED
        )
        
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"🔒 Conexão TLS estabelecida com HiveMQ Cloud! Assinando: {self.topic}")
            client.subscribe(self.topic)
        else:
            print(f"❌ Falha na conexão com o Broker. Código de retorno: {rc}")

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode('utf-8'))
            self.use_case.executar(payload)
        except json.JSONDecodeError:
            print("⚠️ Erro de Infraestrutura: Falha ao decodificar JSON.")
        except Exception as e:
            print(f"⚠️ Erro inesperado ao processar mensagem MQTT: {e}")

    def iniciar(self):
        print(f"📡 Estabelecendo túnel seguro com {self.broker}:{self.port}...")
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_forever() 