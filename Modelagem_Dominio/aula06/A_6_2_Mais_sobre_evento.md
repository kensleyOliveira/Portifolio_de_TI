# ATIVIDADE: MAIS SOBRE EVENTO


### 1. A Classe de Dados: `EstoqueBaixoEvent`

Esta classe encapsula as informações exigidas no exercício: `produtoId`, `quantidadeAtual` e `quantidadeMinima`.

```java
public class EstoqueBaixoEvent {
    private final String produtoId;
    private final int quantidadeAtual;
    private final int quantidadeMinima;

    public EstoqueBaixoEvent(String produtoId, int quantidadeAtual, int quantidadeMinima) {
        this.produtoId = produtoId;
        this.quantidadeAtual = quantidadeAtual;
        this.quantidadeMinima = quantidadeMinima;
    }

    // Getters para acessar os dados no momento do disparo
    public String getProdutoId() { return produtoId; }
    public int getQuantidadeAtual() { return quantidadeAtual; }
    public int getQuantidadeMinima() { return quantidadeMinima; }
}

```

### 2. A Interface do Ouvinte: `EstoqueListener`

Qualquer classe que queira "reagir" quando o estoque baixar (ex: enviar um e-mail ou fazer um pedido de compra) deve implementar esta interface.

```java
public interface EstoqueListener {
    void onEstoqueAbaixoDoMinimo(EstoqueBaixoEvent event);
}

```

### 3. A Classe Principal: `Produto`

Aqui é onde a **Regra de Negócio** solicitada na imagem é aplicada: o evento só dispara se `quantidadeAtual < quantidadeMinima`.

```java
import java.util.ArrayList;
import java.util.List;

public class Produto {
    private String id;
    private int quantidade;
    private int estoqueMinimo;
    private List<EstoqueListener> listeners = new ArrayList<>();

    public Produto(String id, int quantidadeInicial, int estoqueMinimo) {
        this.id = id;
        this.quantidade = quantidadeInicial;
        this.estoqueMinimo = estoqueMinimo;
    }

    public void registrarListener(EstoqueListener listener) {
        listeners.add(listener);
    }

    public void setQuantidade(int novaQuantidade) {
        this.quantidade = novaQuantidade;
        
        // REGRA: Disparar apenas quando quantidadeAtual < quantidadeMinima
        if (this.quantidade < this.estoqueMinimo) {
            dispararEvento();
        }
    }

    private void dispararEvento() {
        EstoqueBaixoEvent evento = new EstoqueBaixoEvent(id, quantidade, estoqueMinimo);
        for (EstoqueListener listener : listeners) {
            listener.onEstoqueAbaixoDoMinimo(evento);
        }
    }
}

```

---

### Exemplo de Uso (Teste)

Para ver o código funcionando, você pode rodar este bloco:

```java
public class Main {
    public static void main(String[] args) {
        Produto p1 = new Produto("PROD-001", 50, 10);

        // Criando um "ouvinte" que avisa no console
        p1.registrarListener(event -> {
            System.out.println("ALERTA: O produto " + event.getProdutoId() + " está com estoque baixo!");
            System.out.println("Atual: " + event.getQuantidadeAtual() + " | Mínimo: " + event.getQuantidadeMinima());
        });

        // Testando a regra
        System.out.println("Alterando para 15...");
        p1.setQuantidade(15); // Não dispara nada

        System.out.println("Alterando para 5...");
        p1.setQuantidade(5);  // DISPARA O EVENTO!
    }
}

```
