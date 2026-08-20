# Análise de Modelagem e Funcionamento: Netflix e Uber

Este documento apresenta uma análise detalhada sobre o funcionamento das plataformas Netflix e Uber, fundamentada nos princípios de modelagem de domínio, modelos mentais e arquitetura de sistemas conforme exposto no material de referência.

1. Fundamentos da Modelagem Aplicados a Grandes Plataformas

A compreensão de sistemas complexos como Netflix e Uber exige o uso de modelos, que são representações simplificadas e abstratas da realidade. Segundo o material, a modelagem cumpre papéis fundamentais:

* Abstração: Isolamento dos aspectos mais relevantes (como a conexão entre motorista e passageiro no Uber), ignorando detalhes irrelevantes para o contexto.
* Entendimento Compartilhado: Garante que todos os envolvidos compreendam conceitos e situações da mesma forma, evitando falhas de comunicação.
* Modelos Mentais: Extração do conhecimento tácito sobre como usuários e especialistas acreditam que o sistema funciona para criar representações eficazes.


--------------------------------------------------------------------------------


2. Análise da Netflix

A Netflix é analisada sob múltiplas perspectivas de modelagem, demonstrando que um sistema complexo não pode ser compreendido por apenas um único diagrama. O funcionamento da plataforma é decomposto em três pilares principais:

Perspectivas de Modelagem da Netflix

Perspectiva	Foco Principal	Propósito
Arquitetura do Sistema	Estrutura técnica e componentes de software.	Compreender a entrega do streaming, armazenamento e processamento de dados.
Modelo de Negócios	Lógica de criação e captura de valor.	Entender como a plataforma gera receita e se sustenta comercialmente.
Ecossistema	Interações entre diversos agentes e o ambiente.	Mapear a relação entre produtores de conteúdo, dispositivos, usuários e a plataforma.

Insights sobre a Netflix

O material destaca que a explicação do funcionamento de uma plataforma de streaming exige síntese e expressão de entendimento por meio de modelos (muitas vezes iniciados em papel). A análise indica que o "melhor" modelo depende do público-alvo: desenvolvedores focarão na arquitetura, enquanto gestores focarão no modelo de negócios.


--------------------------------------------------------------------------------


3. Análise da Uber

O funcionamento do Uber é explorado prioritariamente através de sua Arquitetura de Alto Nível e da identificação dos elementos centrais do seu domínio de negócio.

Elementos do Domínio Uber

Com base na teoria de modelagem de domínio, o funcionamento do Uber pode ser segmentado em:

1. Atores: Usuários (passageiros) e motoristas parceiros.
2. Entidades e Produtos: A viagem (corrida), o veículo e o sistema de pagamento.
3. Ações e Operações: Solicitação de viagem, aceitação pelo motorista, rastreamento em tempo real e processamento de pagamento.
4. Relacionamentos: A conexão dinâmica entre a localização do usuário e a disponibilidade dos motoristas próximos.

Arquitetura de Alto Nível

Diferente de um modelo de negócios focado em lucro, o modelo funcional do Uber enfatiza a infraestrutura que permite a orquestração em tempo real. Isso envolve:

* Processamento de dados de geolocalização.
* Algoritmos de correspondência (matching) entre oferta e demanda.
* Interfaces distintas para diferentes tipos de usuários (motorista vs. passageiro).


--------------------------------------------------------------------------------


4. Comparativo de Propósitos e Representações

A análise dessas plataformas demonstra que a modelagem serve para diferentes fins dentro do ciclo de vida de um sistema computacional:

Finalidades da Modelagem nestes Contextos

* Análise e Projeto: Focar no essencial e validar hipóteses antes da implementação, como testar novos cenários de entrega no Uber.
* Comunicação Eficaz: Utilizar uma linguagem comum (como diagramas UML ou mapas mentais) para alinhar expectativas entre as áreas de negócio e tecnologia.
* Documentação: Registrar o racional por trás das decisões arquiteturais da Netflix para futuras manutenções ou substituições de componentes.

Ferramentas de Representação Sugeridas

Para expressar como esses sistemas funcionam, o material indica o uso de ferramentas específicas:

* Mapas Mentais: GitMind, XMind, FreeMind (para extrair o racional inicial).
* Diagramas Gerais e UML: Miro, Canva, Draw.io e PlantUML (para representações técnicas e arquiteturais).


--------------------------------------------------------------------------------


5. Conclusão da Análise

Tanto a Netflix quanto o Uber operam sobre o que o material denomina "Coração de um Sistema Bem Projetado": um domínio bem entendido e modelado. A eficácia dessas plataformas não reside apenas no código, mas na capacidade de seus modelos em refletir processos de negócio complexos, gerir o conhecimento de especialistas e manter um entendimento compartilhado entre todos os stakeholders.
