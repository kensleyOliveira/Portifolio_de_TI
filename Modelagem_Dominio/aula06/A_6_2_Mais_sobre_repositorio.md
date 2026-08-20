# ATIVIDADE: MAIS SOBRE REPOSITÓRIO

### 0. Entidade Base

Antes de tudo, precisamos da classe `Produto`. Ela deve ser serializável para a Implementação 2 e estar mapeada para a Implementação 1.

```java
import jakarta.persistence.*;
import java.io.Serializable;
import java.math.BigDecimal;

@Entity
@NamedQuery(
    name = "Produto.buscarPorFaixaDePreco",
    query = "SELECT p FROM Produto p WHERE p.preco BETWEEN :min AND :max"
)
public class Produto implements Serializable {
    private static final long serialVersionUID = 1L;

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String nome;
    private BigDecimal preco;

    // Construtores, Getters e Setters
}

```

---

### 1. Interface `ProdutoRepositorio`

Esta interface define o contrato que ambas as implementações devem seguir.

```java
import java.math.BigDecimal;
import java.util.List;

public interface ProdutoRepositorio {
    List<Produto> buscarPorFaixaDePreco(BigDecimal min, BigDecimal max);
}

```

---

### 2. Implementação 1: Hibernate com `@NamedQuery`

Aqui, utilizamos o `EntityManager` para executar a consulta que definimos anteriormente na entidade.

```java
import jakarta.persistence.EntityManager;
import jakarta.persistence.TypedQuery;
import java.math.BigDecimal;
import java.util.List;

public class ProdutoRepositorioHibernate implements ProdutoRepositorio {
    private EntityManager em;

    public ProdutoRepositorioHibernate(EntityManager em) {
        this.em = em;
    }

    @Override
    public List<Produto> buscarPorFaixaDePreco(BigDecimal min, BigDecimal max) {
        TypedQuery<Produto> query = em.createNamedQuery("Produto.buscarPorFaixaDePreco", Produto.class);
        query.setParameter("min", min);
        query.setParameter("max", max);
        return query.getResultList();
    }
}

```

---

### 3. Implementação 2: Recuperação via Serialização

Nesta versão, os objetos são lidos de um arquivo binário e filtrados manualmente em memória.

```java
import java.io.*;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class ProdutoRepositorioSerializado implements ProdutoRepositorio {
    private String caminhoArquivo;

    public ProdutoRepositorioSerializado(String caminhoArquivo) {
        this.caminhoArquivo = caminhoArquivo;
    }

    @Override
    @SuppressWarnings("unchecked")
    public List<Produto> buscarPorFaixaDePreco(BigDecimal min, BigDecimal max) {
        List<Produto> todosProdutos = new ArrayList<>();

        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(caminhoArquivo))) {
            todosProdutos = (List<Produto>) ois.readObject();
        } catch (FileNotFoundException e) {
            System.err.println("Arquivo não encontrado, retornando lista vazia.");
        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }

        // Filtra os objetos recuperados por faixa de preço
        return todosProdutos.stream()
                .filter(p -> p.getPreco().compareTo(min) >= 0 && p.getPreco().compareTo(max) <= 0)
                .collect(Collectors.toList());
    }
}

```

---

