#include <WiFi.h>
#include <WiFiClientSecure.h> // Biblioteca necessária para conexões seguras (SSL/TLS)
#include <PubSubClient.h>
#include "DHT.h"

// ====================================================================
// CONFIGURAÇÕES DE REDE E SERVIDOR (HIVEMQ CLOUD)
// ====================================================================
const char* ssid        = "MegaWiFiAna Paula";       // Seu Wi-Fi residencial
const char* password    = "apff1974";               // Sua senha do Wi-Fi
const char* mqtt_server = "16faa5db8a444e2188dc03acb0032661.s1.eu.hivemq.cloud"; // Host Privado
const int mqtt_port     = 8883;                     // Porta MQTTS (Segura) exigida pelo HiveMQ Cloud

// Credenciais criadas no painel do HiveMQ Cloud
const char* mqtt_user   = "agrostock";       
const char* mqtt_pass   = "Jatoba@1972"; // ATENÇÃO: Cuidado ao compartilhar código com senhas reais!

// Tópico de telemetria para o AgroStock
const char* mqtt_topic  = "kensley/fazenda/soja/telemetria";

// ====================================================================
// CONFIGURAÇÕES DO SENSOR DHT22
// ====================================================================
#define DHTPIN 14          // GPIO 14
#define DHTTYPE DHT22      
DHT dht(DHTPIN, DHTTYPE);

// Instanciação do cliente de rede segura e MQTT
WiFiClientSecure espClient;
PubSubClient client(espClient);
unsigned long ultimoEnvio = 0;

// ====================================================================
// FUNÇÕES DE CONEXÃO E RESILIÊNCIA WI-FI
// ====================================================================
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando-se a: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi conectado com sucesso!");
  Serial.print("Endereço IP da ESP32: ");
  Serial.println(WiFi.localIP());
}

void check_wifi() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Conexão Wi-Fi perdida. Tentando reconectar...");
    WiFi.disconnect();
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    Serial.println("\nWi-Fi restabelecido!");
  }
}

// ====================================================================
// FUNÇÃO DE CONEXÃO/RECONEXÃO AO BROKER MQTT
// ====================================================================
void reconnect() {
  while (!client.connected()) {
    // 1º Passo: Garantir que o Wi-Fi está funcionando antes de tentar o MQTT
    check_wifi(); 

    Serial.print("Tentando conectar ao Broker HiveMQ Cloud Seguro...");
    
    String clientId = "ESP32_Soja_Client-";
    clientId += String(random(0xffff), HEX);
    
    // 2º Passo: Conecta passando o ID do cliente, usuário e senha
    if (client.connect(clientId.c_str(), mqtt_user, mqtt_pass)) {
      Serial.println(" conectado com sucesso via TLS!");
    } else {
      Serial.print(" falhou, rc=");
      Serial.print(client.state());
      Serial.println(". Tentando novamente em 5 segundos...");
      delay(5000); // Aguarda antes de tentar novamente
    }
  }
}

// ====================================================================
// CONFIGURAÇÃO INICIAL (SETUP)
// ====================================================================
void setup() {
  Serial.begin(115200);
  
  dht.begin();
  setup_wifi();
  
  // Ignora a validação estrita da cadeia de certificados para facilitar o setup inicial.
  // Nota Arquitetural: Para o ambiente de produção definitivo, o ideal é usar 
  // espClient.setCACert(root_ca) passando o certificado Let's Encrypt para evitar ataques Man-in-the-Middle.
  espClient.setInsecure(); 
  
  client.setServer(mqtt_server, mqtt_port);

  client.setBufferSize(512);

}

// ====================================================================
// LAÇO PRINCIPAL (LOOP)
// ====================================================================
void loop() {
  // Mantém a estabilidade das conexões a cada iteração
  if (!client.connected()) {
    reconnect();
  }
  client.loop(); // Essencial para manter o Keep-Alive com o broker

  unsigned long agora = millis();
  if (agora - ultimoEnvio > 10000) { // Envio de telemetria a cada 10 segundos
    ultimoEnvio = agora;

    float umidade = dht.readHumidity();
    float temperatura = dht.readTemperature();

    if (isnan(umidade) || isnan(temperatura)) {
      Serial.println("Erro: Falha ao ler dados do sensor DHT22!");
      return;
    }

    // Estrutura o payload JSON
    String payload = "{";
    payload += "\"sensor_id\":\"ESP32_BLOCO_A\",";
    payload += "\"temperatura\":" + String(temperatura, 1) + ",";
    payload += "\"umidade\":" + String(umidade, 1);
    payload += "}";

    Serial.print("Enviando para o HiveMQ Seguro -> ");
    Serial.println(payload);
    
    // Publica no tópico configurado
    client.publish(mqtt_topic, payload.c_str());
  }
}