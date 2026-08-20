# ATIVIDADE: C/S, SW E SK (1)


## 1. Qual é a principal diferença entre os padrões C/S, SW e SK?

A principal diferença reside no **nível de dependência e cooperação** entre as equipes e os modelos de domínio.

| Padrão | Tradução | Dinâmica Principal |
| --- | --- | --- |
| **C/S (Customer/Supplier)** | Cliente/Fornecedor | Existe uma dependência clara. O **Supplier (Fornecedor)** fornece dados/serviços, e o **Customer (Cliente)** os consome. O fornecedor planeja suas entregas levando em conta as necessidades do cliente. |
| **SW (Shared Kernel)** | Núcleo Compartilhado | Duas equipes compartilham um subconjunto do modelo de domínio (código, banco de dados, bibliotecas). Qualquer mudança nesse "núcleo" exige coordenação total entre as duas equipes. |
| **SK (Separate Ways)** | Caminhos Independentes | Não há integração. As equipes decidem que o custo de integrar é maior que o benefício, então cada uma desenvolve sua própria solução de forma totalmente isolada. |

---

## 2. Em que situações é benéfico usar cada padrão?

* **C/S (Customer/Supplier):** Quando um contexto precisa de dados de outro, mas as equipes podem colaborar. É ideal quando o sucesso do "Cliente" depende da qualidade do que o "Fornecedor" entrega, criando um fluxo de trabalho priorizado.
* **SW (Shared Kernel):** Quando duas equipes trabalham em domínios muito próximos e a duplicação de lógica seria muito custosa. É benéfico para manter a **consistência** técnica, mas exige alta maturidade de comunicação para não "quebrar" o sistema do outro.
* **SK (Separate Ways):** Quando a integração é muito complexa, as tecnologias são incompatíveis ou as equipes não conseguem se alinhar. É a melhor escolha para garantir **agilidade total** e autonomia, aceitando que haverá duplicação de esforço.

---

## 3. É possível combiná-los em um mesmo mapa de contexto? Explique.

Um **Mapa de Contexto (Context Map)** é uma visão macro de todo o ecossistema de um software. Em um sistema complexo (como um E-commerce), você terá múltiplos contextos interagindo de formas diferentes simultaneamente:

* O contexto de **Vendas** pode ter um **Shared Kernel** com o contexto de **Estoque** (para validar produtos).
* O mesmo contexto de **Vendas** pode ser um **Customer** do contexto de **Pagamentos** (que age como Supplier).
* Enquanto isso, o sistema de **Marketing** pode seguir **Separate Ways** em relação ao sistema de **Logística**, pois não possuem pontos de contato que justifiquem o custo de integração.

