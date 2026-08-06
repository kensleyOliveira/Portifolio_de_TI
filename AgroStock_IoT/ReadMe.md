# 🌾 AgroStock - Plataforma IoT de Monitoramento Agrícola

O **AgroStock** é um ecossistema completo de Internet das Coisas (IoT) projetado para o monitoramento de telemetria em tempo real e previsão climática, com foco na precisão de dados para o campo (aplicado inicialmente no contexto agrícola de Monte Carmelo - MG).

O projeto abrange desde a captação de dados no hardware (Edge) até a visualização final em um aplicativo Android nativo, utilizando tecnologias de nuvem e arquiteturas limpas.

---

## 🔄 Fluxo do Sistema

A jornada do dado no AgroStock segue um pipeline estruturado e contínuo:

1. **Captura:** Sensores no campo realizam a leitura de grandezas físicas (Temperatura e Umidade).
2. **Publicação (Edge to Cloud):** O microcontrolador publica esses dados via protocolo leve para um Broker na nuvem.
3. **Extração e Processamento (ETL):** Um script autônomo consome os dados do Broker, realiza a limpeza, transformação e padronização.
4. **Armazenamento e Serviço (Backend):** Os dados processados são salvos em um banco de dados relacional e expostos através de endpoints seguros.
5. **Consumo (Mobile):** O aplicativo Android consome a API, renderizando gráficos de tendência (`AgroSparkline`) e cards informativos em tempo real para o usuário final.


	![Fluxo do Sistema em Arquitetura de três camadas](./Image/Arquitetura_tres_camada_AgroStock.png)

---

## 🏗️ Arquitetura e Paradigmas por Camada

O projeto foi modularizado em quatro pacotes principais, cada um adotando as melhores práticas do seu respectivo ecossistema:

### 1. Hardware / IoT (Arduino/C++)

* **Dispositivos:** Microcontrolador ESP32 integrado a sensores DHT22.
* **Paradigma:** Programação Orientada a Eventos e Procedural.
* **Arquitetura:** Lógica baseada em interrupções e *timers* para otimização de energia e conectividade resiliente de rede.

### 2. Pipeline de Dados (ETL em Python)

* **Tecnologia:** Python (Automação de Scripts).
* **Paradigma:** Funcional e Scripting.
* **Arquitetura:** *Data Pipeline* (Extração, Transformação e Carga). O script atua como um *subscriber* contínuo, tratando dados brutos, lidando com inconsistências e garantindo a integridade antes da persistência.

### 3. Backend e Nuvem

* **Tecnologias:** Next.js (API Routes) + MySQL.
* **Paradigma:** Orientação a Objetos e Funcional.
* **Arquitetura:** RESTful API. O backend é stateless, garantindo escalabilidade. As requisições são estruturadas em endpoints semânticos para telemetria histórica, atual e previsão de 15 dias.

### 4. Aplicativo Android (Mobile)

* **Tecnologias:** Kotlin, Jetpack Compose, Ktor Client, Jetpack Navigation 2.8+ (Type-Safe).
* **Paradigma:** Programação Reativa e Declarativa.
* **Arquitetura:** **MVVM (Model-View-ViewModel)** complementada por princípios de **Clean Architecture** e **Domain-Driven Design (DDD)**.
* A camada de Apresentação (UI) utiliza o *Light Theme* para alta visibilidade no campo.
* Separação rigorosa entre a lógica de negócios (Domínio), gerenciamento de estado (ViewModel) e busca de dados (Repositórios e Serviços).



---

## 🔗 Interligação de Ecossistemas e Nuvem

A comunicação entre os módulos foi desenhada para ser assíncrona, escalável e de baixa latência:

* **Hardware ↔ ETL:** A comunicação é feita através do **HiveMQ**, um Broker MQTT robusto na nuvem. O ESP32 atua como *Publisher* (publicando nos tópicos do sensor), enquanto o script Python atua como *Subscriber*.
* **ETL ↔ Backend:** O script Python consolida os dados e os injeta diretamente no banco de dados **MySQL** hospedado em nuvem.
* **Backend ↔ Mobile:** Todo o ecossistema de servidor e banco de dados está unificado e implantado no **Railway**. O aplicativo Android utiliza o **Ktor Client** para realizar chamadas HTTP/REST, consumindo a API Next.js do Railway.

---

## 🛡️ Privacidade e Conformidade com a LGPD

O AgroStock foi concebido sob o princípio do *Privacy by Design*.

* **Natureza dos Dados:** O sistema gerencia, trafega e armazena **estritamente dados ambientais e de telemetria de máquinas/campo** (temperatura, umidade, ID do hardware e *timestamps*).
* **Conformidade:** Não há coleta, processamento ou compartilhamento de Dados Pessoais Identificáveis (PII) dos operadores ou proprietários rurais no fluxo de telemetria.
* **Segurança:** A transferência de dados entre a API (Railway) e o aplicativo Android ocorre através de protocolos criptografados (HTTPS), e as conexões MQTT utilizam credenciais seguras de autenticação, garantindo a integridade e mitigando interceptações, em total respeito às diretrizes de segurança da informação exigidas pela Legislação Brasileira.

---

## 📱 Mural de Imagens (App em Uso)

	![App em ação](./Image/App.png)
---

**Desenvolvido por:** Kensley Alves de Oliveira | *Bacharelando em Sistemas de Informação*

---
