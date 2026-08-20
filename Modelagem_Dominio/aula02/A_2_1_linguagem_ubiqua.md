O conceito de **Voo** (Flight), no contexto de uma empresa de transporte aéreo, é um excelente exemplo de como um termo pode ter **significados distintos e específicos em diferentes áreas de negócio**, o que, sob a ótica do *Domain-Driven Design* (DDD), leva à necessidade de definir uma **Linguagem Ubíqua** em *Contextos Delimitados*,.

A complexidade crítica de um projeto de software reside na **compreensão do domínio**. Para que o software se ajuste harmoniosamente ao domínio, ele deve refletir o domínio. Portanto, o modelo do termo "Voo" deve ser uma **abstração rigorosamente organizada e seletiva** do conhecimento do domínio,.

### 1. Definição e Caracterização dos Usos do Termo "Voo"

O termo "Voo" será usado de maneira diferente, dependendo do *Contexto Delimitado* (área ou subsistema):

| Área de Negócio | Significado/Conceito de Voo | Caracterização e Foco |
| :--- | :--- | :--- |
| **Controle de Tráfego** | O **evento operacional** e o **movimento tridimensional** da aeronave. | O foco está na **segurança**, no monitoramento do **movimento em tempo real**, na adesão à **rota**,, e na prevenção de **colisão**. O conceito central pode envolver a **trajetória** (caminho quadridimensional que o avião viajará no tempo), bem como os pontos fixos da **rota** no solo,. |
| **Aquisição de Passagens** | Um **produto** ou **oferta de serviço**, representando uma viagem programada. | O foco está na **disponibilidade** (capacidade), no **agendamento** (horários de partida e chegada) e nas características comerciais, como classe de serviço. O Voo é um item no **inventário de vendas**. |
| **Faturamento** | Uma **unidade de serviço entregue** ou **unidade de receita**. | O foco é financeiro, envolvendo a **taxa de câmbio**, **preço**, **impostos** e o **status da execução** do serviço (se o voo ocorreu ou foi cancelado). O Voo é uma peça de dados utilizada para **processar pagamentos**. |
| **Manutenção** | Uma **ocorrência operacional** associada a um ativo físico (a aeronave e seus componentes). | O foco está no **ciclo de vida** da aeronave, no **tempo de voo** (horas/ciclos), nos **registros** de estimativas, e na **previsão de falhas**. |

### 2. Possíveis Domínios e Contextos Delimitados

A definição de múltiplos *Contextos Delimitados* é a estratégia para preservar a **integridade do modelo** em projetos grandes.

Os domínios para a empresa de transporte aéreo poderiam ser segregados da seguinte forma, onde o significado de "Voo" varia:

#### Domínio Principal (Core Domain)

O **Domínio Principal** é a iniciativa estratégica chave da organização, geradora de diferencial competitivo, onde se deve aplicar o **talento superior** e o **maior esforço de design**,.

*   **Operações e Controle de Voo:** Foco na segurança e na eficiência da aeronave em movimento (ex: cálculo de trajetória ideal, gestão de rotas em tempo real).

#### Subdomínios Genéricos e de Apoio (Generic Subdomains/Supporting Contexts)

Estes subdomínios adicionam complexidade, mas **não são a motivação central** do projeto,.

*   **Vendas e Agendamento (Sales and Scheduling):** Lida com o inventário de assentos, preços e emissão de passagens. Embora essencial, o modelo de agendamento pode ser mais genérico do que o de controle de tráfego, por exemplo.
*   **Gestão de Frotas e Manutenção (Fleet and Maintenance Management):** Gerencia os ativos físicos (aeronaves, peças) e o registro de suas condições operacionais.
*   **Faturamento e Finanças:** Lida com a contabilidade da empresa. Conceitos como dinheiro, taxas de câmbio e contabilidade são **subdomínios genéricos** (aplicáveis a muitos domínios),,.
*   **Gerenciamento de Tripulação (Crew Management):** Lida com a alocação de pessoal e seus horários de trabalho, sendo um **elemento de apoio**.

![Imagem da linguagem Ubíqua](imagem/A_2_1_linguagem_ubiqua.png)

A separação em *Contextos Delimitados* permite que cada um desses modelos **evolua de forma independente**,. Por exemplo, as regras de negócio de **Faturamento** (que podem ser complexas em si) não precisam ser misturadas com os conceitos de **Manutenção**, onde o significado do termo "Voo" é completamente diferente,.
