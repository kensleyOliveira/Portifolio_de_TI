# ATIVIDADE: IMPLEMENTANDO UMA FÁBRICA


### 1. Modelo de Dados: `Funcionario`

Primeiro, definimos quem é o funcionário e suas regras básicas de contrato.

```java
public class Funcionario {
    private String nome;
    private double salarioBase;
    private double valorHoraExtra;

    public Funcionario(String nome, double salarioBase, double valorHoraExtra) {
        this.nome = nome;
        this.salarioBase = salarioBase;
        this.valorHoraExtra = valorHoraExtra;
    }

    // Getters
    public String getNome() { return nome; }
    public double getSalarioBase() { return salarioBase; }
    public double getValorHoraExtra() { return valorHoraExtra; }
}

```

### 2. O Produto: `FolhaPagamento`

Esta classe representa o resultado final com todos os cálculos aplicados.

```java
public class FolhaPagamento {
    private String nomeFuncionario;
    private double totalBruto;
    private double valorImpostos;
    private double totalLiquido;

    public FolhaPagamento(String nome, double bruto, double impostos) {
        this.nomeFuncionario = nome;
        this.totalBruto = bruto;
        this.valorImpostos = impostos;
        this.totalLiquido = bruto - impostos;
    }

    @Override
    public String toString() {
        return String.format("Folha de: %s\n- Bruto: R$ %.2f\n- Impostos: R$ %.2f\n- Líquido: R$ %.2f", 
                nomeFuncionario, totalBruto, valorImpostos, totalLiquido);
    }
}

```

### 3. A Fábrica: `FolhaPagamentoFactory`

Aqui é onde a "mágica" acontece. A fábrica recebe o funcionário e as horas, calcula as extras e os impostos, e devolve a folha pronta.

```java
public class FolhaPagamentoFactory {
    
    // Alíquota de imposto fixa para o exemplo (ex: 15%)
    private static final double ALIQUOTA_IMPOSTO = 0.15;
    private static final int HORAS_MENSAIS_PADRAO = 160;

    public static FolhaPagamento gerarFolha(Funcionario funcionario, int horasTrabalhadas) {
        double salarioBase = funcionario.getSalarioBase();
        double extras = 0;

        // Cálculo de horas extras
        if (horasTrabalhadas > HORAS_MENSAIS_PADRAO) {
            int qtdExtras = horasTrabalhadas - HORAS_MENSAIS_PADRAO;
            extras = qtdExtras * funcionario.getValorHoraExtra();
        }

        double totalBruto = salarioBase + extras;
        double impostos = totalBruto * ALIQUOTA_IMPOSTO;

        return new FolhaPagamento(funcionario.getNome(), totalBruto, impostos);
    }
}

```

---

### Executando o Código (Main)

Para testar a implementação:

```java
public class Main {
    public static void main(String[] args) {
        // 1. Criamos o funcionário
        Funcionario func = new Funcionario("João Silva", 3000.00, 50.00);

        // 2. Usamos a fábrica para gerar a folha (170 horas trabalhadas = 10 extras)
        FolhaPagamento folha = FolhaPagamentoFactory.gerarFolha(func, 170);

        // 3. Resultado
        System.out.println(folha);
    }
}

```

---