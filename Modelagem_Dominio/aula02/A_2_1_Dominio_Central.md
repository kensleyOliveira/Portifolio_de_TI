# ATIVIDADE: DOMÍNIO CENTRAL

O Domain-Driven Design (DDD) Estratégico exige que o desenvolvimento se concentre no **Domínio Principal** (*Core Domain*), que é o **ativo comercial real** e a fonte da **vantagem competitiva** da organização. Ao mesmo tempo, deve-se identificar e isolar os **Subdomínios Genéricos**, que, embora essenciais para a operação do sistema, não são o foco do projeto.

Abaixo estão os conceitos centrais e os de suporte para um serviço de entrega de comidas, no contexto do DDD:

### 1. Conceitos do Domínio Principal (Core Domain)

O Domínio Principal de um serviço de entrega de comidas reside na **orquestração logística** e no gerenciamento da relação entre a preparação do pedido (restaurante) e a entrega (cliente).

| Conceito | Justificativa |
| :--- | :--- |
| **Logística e *Fulfillment* da Entrega** | Este é o **diferencial competitivo** da plataforma. A capacidade de **entregar o pedido no tempo correto** e com eficiência define a qualidade do serviço. Portanto, todos os **cálculos de tempo real** e o **acompanhamento de percursos** (trajetórias) para coordenar a retirada e o *drop-off* fazem parte do Núcleo. |
| **Modelagem do Pedido (Entidade) e seu *Lifecycle*** | A Entidade **Pedido** é a essência do negócio. A forma como ele é estruturado para ser transmitido ao restaurante, rastreado em tempo real e evoluir de *“Em Preparação”* para *“Em Rota”* é única para o domínio e altamente especializada. |
| **Modelagem de Disponibilidade do Restaurante e Cardápio** | O *Core Domain* deve incluir a lógica complexa de **gerenciamento de produtos**, como a interface do cardápio em tempo real e as regras de alteração de preços ou tempo de preparo. Isso afeta diretamente a promessa de entrega e, portanto, a experiência do cliente. |
| **Modelagem da Tarifa e Previsão de Custos** | As **Políticas para Cálculo e Previsão de Custos de Viagem** (e taxas de serviço) são cruciais para a lucratividade e o valor oferecido. A lógica de negócio para calcular a tarifa final (incluindo taxas e bônus) é um ativo central. |


### 3. Conceitos Fora do Domínio Principal (Subdomínios Genéricos)

Estes elementos são vitais para o sistema, mas não são a especialidade do negócio. Eles devem ser tratados como **Subdomínios Genéricos** e serem **fatorados** em Módulos separados.

| Conceito | Justificativa para Exclusão (Subdomínio Genérico) |
| :--- | :--- |
| **Processamento de Pagamentos e Faturamento** | Embora essencial, a lógica de pagamento é um **subdomínio genérico**. A melhor estratégia é **considerar soluções prontas** (*off-the-shelf*) ou **terceirização**. O sistema deve integrar-se com serviços de pagamento (como cartões ou PIX), mas não deve ser responsável por toda a complexidade regulatória e técnica do processamento financeiro. No exemplo de transporte automotivo (domínio similar), **Processar Pagamentos** ficou de fora do Núcleo. |
| **Gestão de Usuários e Autenticação** | O registro, *login* e gerenciamento de permissões (*Autorização/Autenticação*) são funcionalidades comuns a **qualquer** aplicação de *software*. É mais eficiente **reutilizar** ou comprar uma solução para este subdomínio genérico, permitindo que a equipe foque no *fulfillment*. |
| **Mapeamento de Rotas e Localização (APIs)** | O ato de **Traçar Rotas e Mapas** é uma dependência de serviços externos (Google Maps, Waze). O *Core* usa os dados destas APIs para sua logística e otimização, mas a **criação e o gerenciamento desses dados** são genéricos e não fazem parte do valor único do negócio. |
| **Serviços de Notificação (E-mail/Push)** | O envio de notificações por *e-mail* ou *push* (para confirmar pedidos ou status) é uma funcionalidade de **infraestrutura**. O *Domain Layer* deve invocar um **Serviço** que está isolado na *Infrastructure Layer*, mantendo a lógica de negócio pura e desacoplada. |

A estratégia para esses Subdomínios Genéricos é clara: eles devem ser **fatorados em Módulos separados** e receber **prioridade menor** de desenvolvimento, liberando o tempo dos desenvolvedores mais talentosos para o Domínio Principal.