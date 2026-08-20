# ATIVIDADE: IMPLEMENTANDO UM EVENTO


### 1. O Evento de Domínio: `ReservaConfirmada`

Eventos de domínio devem ser **imutáveis**, pois representam algo que já aconteceu no passado.

```java
import java.time.LocalDate;
import java.time.LocalDateTime;

public final class ReservaConfirmada {
    private final String reservaId;
    private final String clienteId;
    private final LocalDate dataEntrada;
    private final LocalDate dataSaida;
    private final double custoTotal;
    private final LocalDateTime ocorridoEm;

    public ReservaConfirmada(String reservaId, String clienteId, LocalDate dataEntrada, 
                            LocalDate dataSaida, double custoTotal) {
        this.reservaId = reservaId;
        this.clienteId = clienteId;
        this.dataEntrada = dataEntrada;
        this.dataSaida = dataSaida;
        this.custoTotal = custoTotal;
        this.ocorridoEm = LocalDateTime.now();
    }

    // Getters (Apenas leitura para garantir imutabilidade)
    public String getReservaId() { return reservaId; }
    public String getClienteId() { return clienteId; }
    public LocalDate getDataEntrada() { return dataEntrada; }
    public LocalDate getDataSaida() { return dataSaida; }
    public double getCustoTotal() { return custoTotal; }
    public LocalDateTime getOcorridoEm() { return ocorridoEm; }
}

```

---

### 2. O Agregado: `Reserva`

O agregado é responsável por validar as regras de negócio e disparar o evento quando o estado da reserva mudar para "Confirmada".

```java
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

public class Reserva {
    private String id;
    private String clienteId;
    private LocalDate dataEntrada;
    private LocalDate dataSaida;
    private double custoTotal;
    private String status; // Ex: PENDENTE, CONFIRMADA, CANCELADA

    // Lista interna para armazenar eventos gerados pelo agregado
    private final List<Object> eventosDeDominio = new ArrayList<>();

    public Reserva(String id, String clienteId, LocalDate entrada, LocalDate saida, double custo) {
        this.id = id;
        this.clienteId = clienteId;
        this.dataEntrada = entrada;
        this.dataSaida = saida;
        this.custoTotal = custo;
        this.status = "PENDENTE";
    }

    // Funcionalidade para gerar a confirmação de reserva
    public void confirmar() {
        if ("CONFIRMADA".equals(this.status)) {
            throw new IllegalStateException("A reserva já está confirmada.");
        }

        this.status = "CONFIRMADA";

        // Gerando o evento de domínio
        ReservaConfirmada evento = new ReservaConfirmada(
            this.id, 
            this.clienteId, 
            this.dataEntrada, 
            this.dataSaida, 
            this.custoTotal
        );

        this.eventosDeDominio.add(evento);
        
        System.out.println("Reserva " + id + " confirmada com sucesso!");
    }

    public List<Object> getEventosDeDominio() {
        return new ArrayList<>(eventosDeDominio);
    }
}

```

---

### Resumo da Solução

* **Encapsulamento:** Os dados da reserva e o evento estão protegidos contra modificações externas indevidas.
* **Rastreabilidade:** O evento `ReservaConfirmada` captura o estado exato do sistema no momento da confirmação (Data, ID, Valores).
* **Desacoplamento:** No mundo real, esse evento seria capturado por um "Dispatcher" para enviar um e-mail ao cliente ou notificar o setor financeiro sem que a classe `Reserva` precise conhecer esses serviços.
