# ATIVIDADE: MAIS SOBRE AGREGADOS 


## 1. Agregado de Sistema Bancário

Aqui, a `ContaBancaria` controla o estado do saldo. O ponto principal é que o método `sacar` impede que o saldo fique negativo, protegendo a regra de negócio.

```java
public class ContaBancaria {
    private String numeroConta;
    private double saldo;

    public ContaBancaria(String numeroConta, double saldoInicial) {
        if (saldoInicial < 0) {
            throw new IllegalArgumentException("Saldo inicial não pode ser negativo.");
        }
        this.numeroConta = numeroConta;
        this.saldo = saldoInicial;
    }

    public void depositar(double valor) {
        if (valor <= 0) {
            throw new IllegalArgumentException("O valor do depósito deve ser positivo.");
        }
        this.saldo += valor;
    }

    public void sacar(double valor) {
        if (valor <= 0) {
            throw new IllegalArgumentException("O valor do saque deve ser positivo.");
        }
        // Validação da Invariante: saldo nunca pode ser negativo
        if (this.saldo - valor < 0) {
            throw new IllegalStateException("Saldo insuficiente para realizar o saque.");
        }
        this.saldo -= valor;
    }

    public double getSaldo() {
        return saldo;
    }
}

```

---

## 2. Agregado de Sistema de Biblioteca

Neste exemplo, utilizamos um **Value Object** para o `ISBN`. A entidade `Livro` é interna, ou seja, ninguém de fora do agregado pode alterar o status de empréstimo do livro sem passar pela `Biblioteca`.

### Value Object: ISBN

```java
// Imutável por definição
public final class ISBN {
    private final String codigo;

    public ISBN(String codigo) {
        if (codigo == null || codigo.isEmpty()) {
            throw new IllegalArgumentException("ISBN inválido.");
        }
        this.codigo = codigo;
    }

    public String getCodigo() { return codigo; }

    // Value Objects devem implementar equals e hashCode
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof ISBN)) return false;
        return codigo.equals(((ISBN) o).codigo);
    }
}

```

### Entidade Interna: Livro

```java
class Livro {
    private final ISBN isbn;
    private boolean emprestado;

    // Construtor com visibilidade de pacote (apenas a Biblioteca acessa)
    Livro(ISBN isbn) {
        this.isbn = isbn;
        this.emprestado = false;
    }

    void setEmprestado(boolean status) {
        this.emprestado = status;
    }

    public ISBN getIsbn() { return isbn; }
    public boolean isEmprestado() { return emprestado; }
}

```

### Raiz do Agregado: Biblioteca

```java
import java.util.ArrayList;
import java.util.List;

public class Biblioteca {
    private List<Livro> livros = new ArrayList<>();

    public void adicionarLivro(ISBN isbn) {
        livros.add(new Livro(isbn));
    }

    // A regra de negócio exige que o empréstimo seja feito via Raiz
    public void emprestarLivro(ISBN isbn) {
        Livro livro = livros.stream()
                .filter(l -> l.getIsbn().equals(isbn))
                .findFirst()
                .orElseThrow(() -> new RuntimeException("Livro não encontrado."));

        if (livro.isEmprestado()) {
            throw new IllegalStateException("Este livro já está emprestado.");
        }

        livro.setEmprestado(true);
        System.out.println("Livro " + isbn.getCodigo() + " emprestado com sucesso!");
    }
}

```

---