# ATIVIDADE: ACL, OHS E PL (1)


### 1. Qual é a principal diferença entre os padrões PL e OHS?

Ambos são padrões de integração entre contextos delimitados (Bounded Contexts), mas a "responsabilidade" da adaptação muda de lado:

* **PL (Published Language):** É um **modelo de intercâmbio comum**. Em vez de um sistema traduzir diretamente para o modelo do outro, ambos concordam em usar uma linguagem ou formato padronizado (como um esquema XML, JSON Schema ou um conjunto de DTOs compartilhado). É focado na **comunicação universal** entre vários contextos.
* **OHS (Open Host Service):** É um protocolo de acesso definido pelo **provedor do serviço**. O provedor expõe um conjunto de serviços (uma API) e permite que qualquer um o consuma. O provedor mantém essa interface estável para que os consumidores não precisem mudar sempre que a implementação interna do provedor mudar.

> **Em resumo:** PL foca no **formato do dado** compartilhado, enquanto OHS foca na **interface de serviço** disponibilizada pelo fornecedor.

---

### 2. A ACL pode ser usada em conjunto com esses padrões? Explique.

**Sim, com certeza.** Na verdade, é uma prática recomendada para garantir a integridade do sistema.

A **ACL (Anticorruption Layer)** é uma camada de tradução que fica do lado do **consumidor**. Quando um sistema consome um serviço via **OHS** ou recebe dados em uma **PL**, ele utiliza a ACL para converter esses dados externos para o seu próprio modelo de domínio interno.

Isso evita que conceitos externos "contaminem" a lógica de negócio do sistema receptor. A ACL isola a complexidade da tradução na borda da aplicação.

---

### 3. Quais são os benefícios e os riscos de combinar esses padrões?

Combinar esses padrões cria uma arquitetura robusta, mas exige equilíbrio:

#### **Benefícios**

* **Desacoplamento:** As mudanças internas em um sistema não quebram obrigatoriamente os outros.
* **Manutenibilidade:** A ACL permite que o domínio interno evolua independentemente das APIs externas.
* **Escalabilidade de Equipes:** Times diferentes podem trabalhar em ritmos diferentes, desde que respeitem o contrato (OHS/PL).
* **Integridade do Modelo:** O domínio principal permanece "limpo" de termos técnicos ou legados de outros sistemas.

#### **Riscos**

* **Complexidade Adicional:** Introduzir camadas de tradução (ACL) e contratos formais (PL) aumenta o esforço inicial de desenvolvimento.
* **Latência:** Cada camada de tradução e transformação de dados consome processamento, o que pode impactar levemente a performance em sistemas de tempo real.
* **Overhead de Manutenção:** Se o contrato (OHS) mudar drasticamente, a ACL precisará ser atualizada, o que exige coordenação entre as equipes.

