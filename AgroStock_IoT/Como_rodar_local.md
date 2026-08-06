## 🚀 Como Rodar o Projeto Localmente

Se você deseja clonar e testar o ecossistema AgroStock em sua própria máquina, siga as instruções abaixo para configurar cada um dos ambientes.

### 🛠️ Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas:

* **Android Studio** (versão mais recente recomendada) para compilar e rodar o aplicativo.
* **Python 3.x** para rodar o script de extração e transformação (ETL).
* **Node.js** (opcional, apenas se desejar rodar a API Next.js localmente ao invés de consumir a de produção no Railway).
* Uma conta gratuita no **HiveMQ Cloud** (ou outro broker MQTT) para simular o tráfego dos sensores.

### ⚙️ Passo a Passo

**1. Clonar o Repositório**

```bash
git clone https://github.com/seu-usuario/AgroStock.git
cd AgroStock

```

**2. Configurando o Aplicativo Android**

* Abra a pasta correspondente ao aplicativo no **Android Studio**.
* Aguarde o Gradle baixar as dependências e realizar a sincronização (Sync).
* Abra o arquivo `AgroApiService.kt` (na camada de dados) e verifique se a URL base da API está apontando para o servidor correto (Railway ou localhost).
* Conecte um emulador ou smartphone físico e clique em **Run** (`Shift + F10`).

**3. Configurando o Pipeline de Dados (ETL em Python)**

* Navegue até o diretório do script ETL via terminal.
* Instale as bibliotecas necessárias:

```bash
pip install paho-mqtt mysql-connector-python python-dotenv

```

* Crie um arquivo `.env` na raiz da pasta do script contendo as credenciais de acesso ao seu broker HiveMQ e ao banco de dados MySQL hospedado no Railway.
* Execute o script em segundo plano para começar a escutar os sensores:

```bash
python etl_agrostock.py

```

**4. Simulando o Hardware (ESP32)**
Caso não tenha o microcontrolador ESP32 montado com o sensor DHT22 no momento, você pode testar o fluxo completo utilizando um cliente MQTT (como o *MQTT Explorer* ou *MQTTX*).

* Conecte-se ao seu broker HiveMQ.
* Publique um *payload* JSON no formato abaixo no tópico configurado:

```json
{
  "temperatura": 26.5,
  "umidade": 60.2,
  "sensor_id": "simulador_01"
}

```

* Ao publicar, o script Python capturará o dado, enviará para o banco, e o aplicativo Android atualizará a interface (Dashboard e Gráficos) refletindo a nova leitura.

---

Basta copiar este conteúdo, ajustar as partes como a URL do repositório ou o nome exato do arquivo Python (se for diferente), e colar no final do documento que criamos anteriormente. Seu portfólio ficará com uma apresentação técnica impecável!