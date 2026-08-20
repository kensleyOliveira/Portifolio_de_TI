# ATIVIDADE: LIMITAÇÕES

A aplicação do **Domain-Driven Design (DDD)** é frequentemente vista como o "santo graal" para sistemas complexos. No entanto, a indústria possui inúmeros casos onde a tentativa de usar DDD resultou em sistemas excessivamente complexos, lentos e difíceis de manter.

Embora empresas raramente publiquem "Nós falhamos com DDD" em comunicados de imprensa, os *post-mortems* técnicos e a literatura de arquitetura de software (como os relatos de Vaughn Vernon e Martin Fowler) identificam padrões claros de fracasso.

Aqui estão três casos arquétipos clássicos de falha na aplicação de DDD, suas causas e as soluções adotadas.

---

### Caso 1: O Excesso de Engenharia em Domínios Simples (CRUD)

Este é o caso mais comum de falha. Uma equipe decide aplicar DDD em um sistema que é, essencialmente, um cadastro simples de dados (ex: um sistema de gerenciamento de conteúdo básico ou aplicações administrativas).

* **O Cenário:** A equipe criou *Aggregates*, *Value Objects*, *Repositories* e camadas de *Application Services* para operações que consistiam apenas em "Salvar um formulário no banco de dados".
* **2. Causas da Falha:**
    * **Complexidade Acidental:** O custo de desenvolver e manter a estrutura do DDD (camadas, abstrações) foi maior do que o valor do negócio.
    * **Ignorar a Regra de Ouro:** O DDD é destinado a **domínios complexos**. Se a lógica de negócio é trivial (apenas ler/escrever dados), o DDD atrapalha mais do que ajuda.
* **3. Alternativa Adotada:**
    * **Transaction Script / Smart UI:** A solução foi remover as camadas táticas do DDD. A equipe migrou para uma arquitetura mais simples, como o padrão **MVC (Model-View-Controller)** tradicional ou **Transaction Script**, onde a lógica reside diretamente no serviço ou controlador, interagindo com objetos de dados simples (DTOs ou Active Records).


---

### Caso 2: O Modelo de Domínio Anêmico (A Ilusão do DDD)

Muitas equipes acreditam estar fazendo DDD porque têm pastas chamadas `Domain`, `Services` e `Repositories`, mas o comportamento do sistema não está onde deveria.

* **O Cenário:** O sistema foi construído com classes de "Entidade", mas elas continham apenas *getters* e *setters* (dados puros). Toda a regra de negócio (validações, cálculos, transições de estado) estava espalhada em "Service Classes" procedurais gigantescas.
* **2. Causas da Falha:**
    * **Foco apenas nos Padrões Táticos:** A equipe copiou a estrutura de pastas do DDD, mas não entendeu a orientação a objetos.
    * **Falta de Linguagem Ubíqua:** O código não refletia a linguagem do negócio, apenas a estrutura do banco de dados. Isso viola o princípio central do DDD: o modelo deve encapsular o comportamento.
* **3. Alternativa Adotada:**
    * **Refatoração para Rich Domain Model:** Mover a lógica dos serviços para dentro das entidades.
    * **OU Aceitação do Anêmico:** Em alguns casos, a equipe percebeu que a abordagem procedural (separar dados de comportamento) era mais familiar e performática para a equipe atual, abandonando a pretensão de DDD e assumindo uma arquitetura de serviços procedurais convencional.

---

### Caso 3: O Monólito Distribuído (Microserviços com Fronteiras Erradas)

Este caso ocorre frequentemente quando equipes tentam usar DDD para quebrar um monólito em microserviços, mas erram na definição dos **Bounded Contexts** (Contextos Delimitados).

* **O Cenário:** A equipe dividiu o sistema baseando-se em "Substantivos" (ex: Serviço de Cliente, Serviço de Produto, Serviço de Pedido) em vez de "Comportamentos" ou "Contextos". Isso gerou um forte acoplamento: para fazer qualquer alteração no "Pedido", era necessário alterar o "Cliente" e o "Produto" simultaneamente.
* **2. Causas da Falha:**
    * **Ignorar o Design Estratégico:** A equipe focou no código (tático) antes de entender os limites do negócio (estratégico).
    * **Modelagem Canônica Unificada:** Tentar criar um modelo único de "Cliente" que servisse para vendas, entregas e cobrança, o que gera conflitos e dependências.
* **3. Alternativa Adotada:**
    * **Modular Monolith (Monólito Modular):** Reverter os microserviços físicos para um único executável bem estruturado para redescobrir as fronteiras corretas.
    * **Redefinição via Event Storming:** Uso de workshops com especialistas de negócio para redefinir as fronteiras baseadas em fluxos de valor, resultando em duplicação proposital de dados (ex: ter um modelo de 'Cliente' no contexto de Vendas e outro modelo diferente de 'Destinatário' no contexto de Entrega).


---

### Resumo Comparativo

| Cenário de Falha | Causa Principal | Alternativa / Solução |
| :--- | :--- | :--- |
| **CRUD Overkill** | Aplicar DDD em problemas simples. | Arquiteturas Data-Driven (MVC, Transaction Script). |
| **Modelo Anêmico** | Classes de domínio sem comportamento; lógica vazada nos serviços. | Enriquecer o modelo (OOP real) ou assumir o modelo procedural. |
| **Fronteiras Erradas** | Divisão baseada em tabelas/dados, não em contextos de negócio. | Modular Monolith ou remapeamento via Event Storming. |

