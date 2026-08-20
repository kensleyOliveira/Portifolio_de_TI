# ATIVIDADE: IMPLEMENTANDO UM AGREGADO

### 1. Entidades e Objetos de Valor

Primeiro, definimos o **Voo** e o **Passageiro**. Para simplificar, trataremos o `Voo` como uma entidade que contém a lógica de ocupação.

```java
import java.util.UUID;

// Entidade Voo
class Voo {
    private UUID id;
    private int capacidadeTotal;
    private int assentosOcupados;

    public Voo(UUID id, int capacidadeTotal) {
        this.id = id;
        this.capacidadeTotal = capacidadeTotal;
        this.assentosOcupados = 0;
    }

    public boolean temVaga() {
        return assentosOcupados < capacidadeTotal;
    }

    public void ocuparAssento() {
        if (!temVaga()) throw new IllegalStateException("Voo lotado!");
        this.assentosOcupados++;
    }

    // Getters...
    public UUID getId() { return id; }
}

// Entidade Passageiro
class Passageiro {
    private String cpf;
    private String nome;

    public Passageiro(String cpf, String nome) {
        this.cpf = cpf;
        this.nome = nome;
    }
    // Getters...
}

```

---

### 2. O Agregado: Reserva (Aggregate Root)

A `Reserva` é a raiz. Ela controla o estado e garante que a regra de "não confirmar se o voo estiver lotado" seja respeitada.

```java
enum StatusReserva { PENDENTE, CONFIRMADA, CANCELADA }

public class Reserva {
    private UUID id;
    private Passageiro passageiro;
    private Voo voo;
    private StatusReserva status;

    public Reserva(Passageiro passageiro, Voo voo) {
        this.id = UUID.randomUUID();
        this.passageiro = passageiro;
        this.voo = voo;
        this.status = StatusReserva.PENDENTE;
    }

    /**
     * Regra de Negócio: A reserva só pode ser confirmada se houver vaga.
     */
    public void confirmar() {
        if (this.status != StatusReserva.PENDENTE) {
            throw new IllegalStateException("Apenas reservas pendentes podem ser confirmadas.");
        }

        if (!voo.temVaga()) {
            throw new IllegalStateException("Não é possível confirmar: O voo está lotado.");
        }

        this.voo.ocuparAssento();
        this.status = StatusReserva.CONFIRMADA;
        System.out.println("Reserva " + id + " confirmada com sucesso!");
    }

    public StatusReserva getStatus() { return status; }
}

```

---

### 3. Exemplo de Uso (Testando a Regra)

```java
public class Main {
    public static void main(String[] args) {
        // Criamos um voo com apenas 1 vaga
        Voo vooGOL = new Voo(UUID.randomUUID(), 1);
        Passageiro p1 = new Passageiro("123", "Alice");
        Passageiro p2 = new Passageiro("456", "Bob");

        // Primeira reserva
        Reserva reserva1 = new Reserva(p1, vooGOL);
        reserva1.confirmar(); // Sucesso

        // Segunda reserva (Tentativa de lotar o voo)
        try {
            Reserva reserva2 = new Reserva(p2, vooGOL);
            reserva2.confirmar(); 
        } catch (IllegalStateException e) {
            System.err.println("Erro esperado: " + e.getMessage());
        }
    }
}

```

---

### Pontos Chave da Solução:

* **Encapsulamento:** O status da reserva não pode ser alterado diretamente de fora; ele depende do método `confirmar()`.
* **Consistência:** A regra de ocupação é verificada no momento exato da transição de estado.
* **Identidade:** Usamos `UUID` para garantir que cada reserva e voo sejam únicos no sistema.
