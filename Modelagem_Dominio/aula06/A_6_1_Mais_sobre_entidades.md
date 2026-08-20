# ATIVIDADE: MAIS SOBRE ENTIDADES

## 1. Implementação da Entidade `ReservaHotel`

Para esta implementação, utilizarei uma abordagem de **Domain-Driven Design (DDD)** simples, garantindo que a regra de negócio (não cancelar após check-in) seja protegida pela própria entidade.

```java
import java.util.UUID;

public class ReservaHotel {
    private final UUID id;
    private boolean checkInRealizado;
    private StatusReserva status;

    public ReservaHotel() {
        this.id = UUID.randomUUID();
        this.status = StatusReserva.CONFIRMADA;
        this.checkInRealizado = false;
    }

    public void realizarCheckIn() {
        this.checkInRealizado = true;
    }

    public void cancelar() {
        // Regra de Negócio: Não pode ser cancelada após check-in
        if (this.checkInRealizado) {
            throw new IllegalStateException("Não é possível cancelar uma reserva após o check-in.");
        }
        this.status = StatusReserva.CANCELADA;
    }

    // Getters para fins de consulta
    public UUID getId() { return id; }
    public boolean isCheckInRealizado() { return checkInRealizado; }
    public StatusReserva getStatus() { return status; }
}

enum StatusReserva {
    CONFIRMADA, CANCELADA
}

```

---

## 2. Análise de Identificadores Acadêmicos e Digitais

No design de sistemas, esses códigos funcionam como **identificadores únicos naturais** ou de negócio. Eles garantem que a identidade de um objeto seja preservada mesmo que os dados mudem.

### Comparação de Identificadores

| Código | Nome Completo | Foco Principal | Exemplo de Entidade |
| --- | --- | --- | --- |
| **ISBN** | International Standard Book Number | Livros e edições específicas. | `Livro`, `Ebook` |
| **ISSN** | International Standard Serial Number | Publicações seriadas (revistas, jornais). | `RevistaCientifica`, `Periodico` |
| **DOI** | Digital Object Identifier | Objetos digitais específicos (artigos, datasets). | `ArtigoCientifico`, `Dataset` |

### Exemplos Práticos de Implementação

#### A. Entidade `Livro` usando **ISBN**

O ISBN é perfeito para evitar duplicidade em um catálogo de biblioteca. Se você tem duas edições diferentes do mesmo livro, cada uma terá um ISBN único, tratando-as como entidades distintas.

* **Uso:** Chave primária de negócio ou campo de busca única.

#### B. Entidade `ArtigoCientifico` usando **DOI**

O DOI é um link persistente. Diferente de uma URL comum que pode quebrar, o DOI identifica o artigo "para sempre".

* **Uso:** Em uma entidade `Publicacao`, o DOI serve como a identidade que permite rastrear citações e métricas de impacto de forma global.

#### C. Entidade `RevistaCientifica` usando **ISSN**

Útil para agrupar diversas edições sob uma mesma identidade de "série".

* **Uso:** Ao implementar um sistema de submissão, o ISSN garante que o autor está enviando o trabalho para a publicação correta, independentemente do volume ou ano.

---

