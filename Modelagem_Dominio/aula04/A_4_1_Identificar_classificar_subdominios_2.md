# ATIVIDADE: IDENTIFICAR E CLASSIFICAR SUBDOMÍNIOS (2)

A análise da BusVNext, uma empresa de transporte público sob demanda (bus-hailing), deve ser baseada nos princípios de Design Orientado pelo Domínio (DDD), classificando as áreas de negócio conforme sua complexidade e diferencial estratégico.

### 1. Domínio de Negócios da BusVNext

O Domínio de Negócios da BusVNext é o **Transporte Público Flexível e Otimizado por Rota Dinâmica**, com o objetivo de oferecer viagens de ônibus tão confortáveis quanto pegar um táxi.

### 2. Identificação e Classificação dos Subdomínios

A classificação dos subdomínios é baseada em onde reside o diferencial competitivo (Domínio Central), onde há regras críticas (Suporte) e o que pode ser resolvido com soluções prontas (Genérico).

| Subdomínio | Classificação | Justificativa |
| :--- | :--- | :--- |
| **Algoritmo de Roteamento Dinâmico e Otimização** | **Domínio Central (*Core Domain*)** | É o principal desafio da empresa e seu maior diferencial. A complexidade de implementar o algoritmo, que é uma variante do "problema do caixeiro-viajante" e exige ajustes contínuos (priorizando partidas rápidas sobre chegadas pontuais), torna esta a área de **inovação e investimento estratégico** da BusVNext. |
| **Gestão e Administração da Frota/Motoristas** | **Domínio Central (*Core Domain*) ou de Suporte Estratégico** | Gerenciar o status, localização e capacidade dos ônibus para que a rota possa ser ajustada em tempo real é uma parte crucial da promessa de serviço. Embora a administração básica seja comum, a **integração em tempo real** com o algoritmo de roteamento a torna estratégica. |
| **Recomendação e Aplicação de Descontos/Tarifas Dinâmicas** | **Domínio de Suporte Crítico** | Este subdomínio lida com a atração de consumidores e o **equilíbrio de demandas** em horários de pico e fora de pico, afetando diretamente a viabilidade econômica do serviço e a otimização de rotas.
| **Integração com Provedores Terceirizados (Trânsito/Alerta)** | **Domínio de Suporte** | É necessário para otimizar o roteamento (Core Domain) com informações de trânsito em tempo real. No entanto, o desenvolvimento do *software* de integração é menos complexo do que o algoritmo de roteamento em si.
| **Interação com Usuário (Pedido de Viagem via App)** | **Domínio de Suporte** | O processo de um cliente pedir uma viagem é essencial, mas não é o diferencial competitivo. O desafio reside na complexidade do roteamento por trás do pedido, e não na interface do aplicativo em si.
| **Processamento de Pagamentos e Faturamento** | **Domínio Genérico (*Generic Subdomain*)** | Lidar com as transações financeiras e cobranças é essencial, mas é um problema de negócio comum, geralmente resolvido com soluções prontas.

### 3. Decisões de Design que Podem ser Consideradas

As decisões de design devem ser tomadas para proteger o Domínio Central (Roteamento Dinâmico), garantindo que ele tenha a máxima flexibilidade e possa iterar rapidamente, delegando tarefas de suporte.

1.  **Definição de Contextos Delimitados (*Bounded Contexts*):**
    *   **Contexto de Otimização de Rota (Core Domain):** Este contexto seria isolado e conteria toda a complexidade do algoritmo de roteamento (a variante do problema do caixeiro-viajante), focando apenas na lógica de otimização de tempo e na priorização de partidas.
    *   **Contexto de Informações Geográficas (Suporte):** Seria responsável por receber dados de provedores externos (trânsito em tempo real, rotas fixas, localização GPS), expondo apenas dados limpos para o Contexto de Otimização de Rota.
    *   **Contexto de Gestão de Frota (Suporte):** Conteria a Entidade "Ônibus" e suas informações de capacidade e *status*, fornecendo ao Core Domain os recursos disponíveis para roteamento.

2.  **Mapeamento de Contextos (*Context Mapping*):**
    O **Contexto de Otimização de Rota** deve ter uma relação de **Cliente/Fornecedor (*Customer/Supplier*)** com o **Contexto de Informações Geográficas**, garantindo que as necessidades do Core Domain (Cliente) conduzam a qualidade e o formato dos dados de trânsito recebidos (Fornecedor).
