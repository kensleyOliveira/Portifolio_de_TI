# **REFLEXÃO - 1**

No contexto do desenvolvimento de um Modelo de Domínio usando *Domain-Driven Design* (DDD), o crescimento excessivo do modelo, devido ao excesso de novos requisitos, pode levar a uma série de problemas, principalmente a perda de **integridade do modelo** e o surgimento de **anti-padrões** de design.
As principais armadilhas ao lidar com o crescimento de um Modelo de Domínio no DDD estão relacionadas à falta de rigor na **definição de limites** e na **gestão da complexidade**.

Um modelo de domínio cresce demasiadamente, devido ao excesso de novos requisitos, apresenta o risco de **desvio dos conceitos originais** associados a projetos Scrum.

Em um contexto de desenvolvimento de sistemas de gestão de projetos Scrum, o Modelo de Domínio inicial é naturalmente construído em torno de conceitos centrais como **Produtos**, **Itens de Backlog**, **Lançamentos** e **Sprints**.

O que pode ocorrer, conforme a complexidade do sistema aumenta, e novos requisitos são introduzidos (como adicionar funcionalidades de usuários, discussões, locatários, pagamentos, planos de suporte e rastreamento de horários), é que o modelo começa a se expandir de forma descontrolada.

Neste cenário, a proliferação de conceitos não relacionados pode levar a um desvio por diversas razões:

1.  **Perda de Foco:** O modelo original, focado na essência da metodologia Scrum, é obscurecido pela massa de modelos e códigos de suporte, o que dificulta o entendimento de **quais elementos são realmente essenciais** para o domínio Scrum.
2.  **Diluição dos Conceitos Centrais:** Conceitos como *Produto*, *Item de Backlog* ou *Sprint* podem se tornar acoplados a funcionalidades externas (como pagamentos ou gerenciamento de recursos humanos). Essa mistura de conceitos dilui o significado da **Linguagem Ubíqua** e a consistência interna do modelo, tornando-o confunso, inconsistente e possível falha de funcionalidade.
3.  **Surgimento da "Grande Bola de Lama" (*Big Ball of Mud*):** A falha em preservar a **integridade do modelo** e a inclusão de elementos de suporte e funcionalidades genéricas levam o sistema a se tornar um anti-padrão conhecido como "Grande Bola de Lama". Nessa situação, os limites se tornam confusos, múltiplos modelos se misturam e a manutenção se torna extremamente difícil.

## Como lidar com este problema?

O *Domain-Driven Design* oferece ferramentas de **Design Estratégico** para resolver esse problema, evitando o desvio dos conceitos originais do Scrum ao impor limites claros:

*   **Domínio Principal (*Core Domain*):** Os conceitos Scrum originais (Produtos, Sprints, Itens de Backlog) devem ser identificados como o **Domínio Principal** do negócio.
*   **Subdomínios:** As funcionalidades adicionadas, como processamento de pagamentos ou gerenciamento de calendários/recursos humanos, devem ser segregadas em **Subdomínios Genéricos**.
*   **Contextos Delimitados (*Bounded Contexts*):** Ao definir explicitamente os **Contextos Delimitados**, é possível garantir que a **Linguagem Ubíqua** e o modelo dos elementos Scrum permaneçam **estritamente consistentes e unificados** dentro de seu contexto, isolados da complexidade trazida pelos outros subdomínios.

Ao aplicar corretamente o DDD, a equipe evita que o modelo entre em colapso e garante que os conceitos Scrum originais sejam preservados em um *design* coeso.

