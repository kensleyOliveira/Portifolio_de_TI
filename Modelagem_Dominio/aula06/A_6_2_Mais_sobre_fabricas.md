# ATIVIDADE: MAIS SOBRE FÁBRICAS

### 1. A Classe de Modelo (`Item` e `NotaFiscal`)

Primeiro, precisamos das classes que representam os dados.

```java
import java.util.List;

class Item {
    private String nome;
    private double valor;

    public Item(String nome, double valor) {
        this.nome = nome;
        this.valor = valor;
    }

    public double getValor() { return valor; }
}

class NotaFiscal {
    private List<Item> itens;
    private double impostos;
    private double valorTotal;

    // O construtor é protegido para garantir que apenas a Fábrica o utilize
    protected NotaFiscal(List<Item> itens, double impostos, double valorTotal) {
        this.itens = itens;
        this.impostos = impostos;
        this.valorTotal = valorTotal;
    }

    @Override
    public String toString() {
        return "Nota Fiscal [Itens: " + itens.size() + ", Impostos: R$" + impostos + ", Total: R$" + valorTotal + "]";
    }
}

```

---

### 2. A Fábrica (`NotaFiscalFabrica`)

Esta classe centraliza a lógica de criação e as regras de negócio solicitadas.

```java
import java.util.List;

public class NotaFiscalFabrica {

    public NotaFiscal criar(List<Item> itens) {
        // Regra 1: Validação - Itens não podem ser vazios
        if (itens == null || itens.isEmpty()) {
            throw new IllegalArgumentException("A nota fiscal deve conter pelo menos um item.");
        }

        // Regra 2: Calcule impostos automaticamente
        double valorBruto = 0;
        for (Item item : itens) {
            valorBruto += item.getValor();
        }

        // Exemplo: Imposto fixo de 10%
        double impostos = valorBruto * 0.10;
        double valorTotal = valorBruto + impostos;

        return new NotaFiscal(itens, impostos, valorTotal);
    }
}

```

---

### 3. Exemplo de Uso (Main)

```java
import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        NotaFiscalFabrica fabrica = new NotaFiscalFabrica();

        try {
            // Criando itens
            Item i1 = new Item("Notebook", 3000.0);
            Item i2 = new Item("Mouse", 100.0);

            // Gerando a Nota via Fábrica
            NotaFiscal nf = fabrica.criar(Arrays.asList(i1, i2));

            System.out.println("Nota gerada com sucesso!");
            System.out.println(nf);

        } catch (IllegalArgumentException e) {
            System.err.println("Erro na criação: " + e.getMessage());
        }
    }
}

```

---

### Por que usar essa estrutura?

* **Encapsulamento:** A lógica de quanto cobrar de imposto não fica espalhada pelo código; se a alíquota mudar, você altera apenas na `NotaFiscalFabrica`.
* **Segurança:** Ao validar a lista de itens na fábrica, você impede que o sistema processe notas fiscais inválidas (vazias).
* **Facilidade:** O desenvolvedor que usa a classe não precisa saber como calcular o imposto, ele apenas fornece os itens e recebe o objeto pronto.

---