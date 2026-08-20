#ATIVIDADE: IDENTIFICAR E CALSSIFICAR SUBDOMÍNIOS (1)


## 1. Domínio de Negócios da Gigmaster

O Domínio de Negócios da Gigmaster é a **Venda e Distribuição de Ingressos para Eventos Musicais e a Geração de Recomendações Personalizadas**.

## 2. Identificação e Classificação dos Subdomínios

Ao aplicar os princípios do Design Orientado pelo Domínio (DDD), os subdomínios são classificados com base em sua importância estratégica e no diferencial competitivo que oferecem:

| Subdomínio | Classificação | Justificativa |
| :--- | :--- | :--- |
| **Algoritmo de Recomendação e Análise de Perfil** | **Domínio Central (*Core Domain*)** | É o principal diferencial competitivo da Gigmaster. O talento e a complexidade do negócio residem na capacidade de analisar bibliotecas musicais, serviços de *streaming* e redes sociais para identificar shows de interesse. Este é o foco da inovação e do investimento estratégico. |
| **Venda e Distribuição de Ingressos** | **Domínio Central (*Core Domain*) ou de Suporte Estratégico** | Embora o diferencial seja a recomendação, a venda e distribuição de ingressos é o núcleo comercial e a principal fonte de receita. Ele define o propósito primário do negócio (venda de ingressos), sendo, portanto, um Domínio Central ou um Domínio de Suporte Estratégico. |
| **Gestão de Dados Pessoais e Anonimização** | **Domínio de Suporte Crítico** | Este subdomínio lida com a **regra de negócio** de que "toda informação pessoal é criptografada" e o algoritmo "trabalha exclusivamente com dados anônimos." A **privacidade é uma restrição de negócio crucial e um pilar de confiança**. Embora a criptografia básica seja genérica, a **manutenção da conformidade de anonimato** do algoritmo é vital para a operação do Core Domain e, portanto, exige atenção estratégica, classificando-o como Suporte Crítico ao Core. |
| **Processamento de Pagamentos** | **Domínio Genérico (*Generic Subdomain*)** | Lidar com a transação financeira (cobrança e repasse) é essencial, mas não é o diferencial competitivo da empresa. É uma área de baixa complexidade exclusiva do negócio, geralmente resolvida por soluções prontas (*off-the-shelf*). |
| **Localização de Eventos e Proximidade** | **Domínio Genérico (*Generic Subdomain*)** | A funcionalidade de identificar eventos "nas proximidades" utiliza serviços de geolocalização e mapeamento, que são serviços de apoio comuns e facilmente adquiríveis, não exigindo investimento estratégico exclusivo no seu desenvolvimento. |

## 3. Decisões de Design que Podem ser Consideradas

As decisões de design, tanto estratégicas quanto táticas, devem ser tomadas para proteger o Domínio Central (o Algoritmo de Recomendação) e impor a restrição de privacidade:

#### **A) Design Estratégico**

1.  **Definição de Contextos Delimitados (*Bounded Contexts*):**
    É crucial separar o sistema em diferentes contextos para resolver a complexidade da privacidade.
    *   **Contexto de Recomendação Anônima (Core):** Conteria o algoritmo e trabalharia exclusivamente com **dados anônimos**.
    *   **Contexto de Identidade e Criptografia (Suporte Crítico):** Conteria os dados pessoais brutos (criptografados) e seria responsável por garantir que apenas as informações anonimizadas necessárias sejam expostas ao Contexto de Recomendação.

2.  **Linguagem Ubíqua (*Ubiquitous Language*):**
    A linguagem deve ser rigorosamente definida em cada contexto para evitar ambiguidades, especialmente em relação ao tratamento de dados. No Contexto de Recomendação, termos como "**Perfil de Preferência**" seriam usados, mas o termo "**Usuário Registrado**" só seria conhecido no Contexto de Identidade/Venda, garantindo que o algoritmo central não saiba quem é o usuário que está sendo processado.

#### **B) Design Tático**

1.  **Entidades e Agregados (*Aggregates*):**
    O **Design Tático** deve ser aplicado para garantir o isolamento físico dos dados. É fundamental que os dados pessoais (Entidade "Usuário", "Conta de Streaming") e os dados de recomendação (Entidade "Perfil de Preferência Anônimo") pertençam a **Agregados separados**.
    *   O **Agregado de Usuário** (no contexto de Identidade) conteria a informação pessoal criptografada.
    *   O **Agregado de Perfil Anônimo** (no contexto de Recomendação) conteria apenas vetores de preferência sem identificadores pessoais.

2.  **Eventos de Domínio (*Domain Events*):**
    Eventos de Domínio podem ser usados para comunicar a alteração nas preferências musicais do usuário (ex: "*PreferenciaMusicalAtualizada*") entre o contexto de entrada de dados e o contexto de anonimização. Essa comunicação deve garantir que, antes de ser enviada ao Core Domain, a informação passe pela etapa de anonimização.

Em resumo, a arquitetura da Gigmaster deve ser projetada para que o componente estratégico (o algoritmo de recomendação) possa inovar rapidamente, ao mesmo tempo em que a regra de negócio mais crítica (o anonimato dos dados) seja rigorosamente imposta pelas fronteiras entre os Contextos Delimitados.