# ATIVIDADE: IMPLEMENTANDO UM REPOSITÓRIO

## 1. A Entidade de Domínio (`ContaBancaria`)

Primeiro, definimos nossa classe de modelo com as anotações do JPA.

```java
import jakarta.persistence.*;
import java.math.BigDecimal;

@Entity
@Table(name = "contas_bancarias")
public class ContaBancaria {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String numeroConta;
    private String titular;
    private BigDecimal saldo;

    // Construtores, Getters e Setters
    public ContaBancaria() {}

    public ContaBancaria(String numeroConta, String titular, BigDecimal saldo) {
        this.numeroConta = numeroConta;
        this.titular = titular;
        this.saldo = saldo;
    }

    // Getters e Setters omitidos por brevidade...
}

```

---

## 2. Interface do Repositório

No DDD, a interface reside na camada de domínio para definir o contrato.

```java
import java.util.List;

public interface ContaBancariaRepositorio {
    void salvar(ContaBancaria conta);
    ContaBancaria buscarPorId(Long id);
    // Operação solicitada no exercício
    List<ContaBancaria> buscarContasComSaldoNegativo();
}

```

---

## 3. Implementação com Hibernate (JPA)

Aqui está a implementação técnica que utiliza o `EntityManager` para realizar as consultas no banco de dados. Note o uso de **JPQL** para a busca de saldos negativos.

```java
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import java.math.BigDecimal;
import java.util.List;

public class ContaBancariaRepositorioImpl implements ContaBancariaRepositorio {

    @PersistenceContext
    private EntityManager entityManager;

    @Override
    public void salvar(ContaBancaria conta) {
        if (conta.getId() == null) {
            entityManager.persist(conta);
        } else {
            entityManager.merge(conta);
        }
    }

    @Override
    public ContaBancaria buscarPorId(Long id) {
        return entityManager.find(ContaBancaria.class, id);
    }

    /**
     * Destaque: Operação de busca para contas com saldo negativo
     */
    @Override
    public List<ContaBancaria> buscarContasComSaldoNegativo() {
        String jpql = "SELECT c FROM ContaBancaria c WHERE c.saldo < :zero";
        return entityManager.createQuery(jpql, ContaBancaria.class)
                            .setParameter("zero", BigDecimal.ZERO)
                            .getResultList();
    }
}

```

---

### Explicação dos Pontos Chave:

* **Abstração:** A interface permite que o restante do sistema não dependa diretamente do Hibernate. Se você mudar para o MongoDB no futuro, o domínio não sofre impacto.
* **A Consulta de Saldo Negativo:** Utilizamos `:zero` como parâmetro para garantir que a comparação seja feita corretamente com `BigDecimal.ZERO`, evitando problemas de precisão numérica.
* **Persistência:** O método `salvar` decide entre `persist` (novo registro) ou `merge` (atualização), mantendo o ciclo de vida do objeto gerenciado.

---