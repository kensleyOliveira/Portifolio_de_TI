# ATIVIDADE: CF E ACL (1)

## Atividade 3: Conformista (CF) e Camada Anticorrupção (ACL)

### 1. Principal Diferença

* **Conformista (Conformist):** O contexto "Downstream" aceita o modelo do "Upstream" como ele é, sem adaptações. Ele se adapta totalmente ao fornecedor.
* **ACL (Anticorruption Layer):** O contexto "Downstream" cria uma camada de tradução para converter o modelo externo em seu próprio modelo interno, protegendo sua integridade semântica.

### 2. Situações de Uso

* **Conformista:** Quando o modelo do fornecedor é excelente, amplamente padronizado ou quando a equipe não tem recursos para criar traduções.
* **ACL:** Ao integrar com sistemas legados, APIs de terceiros com designs ruins ou quando o seu domínio interno é muito rico e não deve ser "poluído" por conceitos externos.

### 3. Benefícios e Riscos

* **Benefícios:** A **ACL** garante total autonomia e isolamento do modelo; o **Conformista** simplifica a integração e reduz o esforço inicial de codificação.
* **Riscos:** A **ACL** tem alto custo de desenvolvimento e manutenção; o **Conformista** deixa você vulnerável a mudanças drásticas feitas pelo fornecedor que podem quebrar seu sistema.

---

