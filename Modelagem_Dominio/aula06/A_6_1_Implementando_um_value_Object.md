# ATIVIDADE: IMPLEMENTANDO UM VALUE OBJECT

## 1. Implementação Clássica (Java Class)

Para garantir que o objeto seja um Value Object autêntico, utilizamos o modificador `final` na classe e nos atributos (imutabilidade) e validamos o estado no construtor.

```java
public final class Cpf {
    private final String numero;

    public Cpf(String numero) {
        if (numero == null || numero.replaceAll("\\D", "").length() != 11) {
            throw new IllegalArgumentException("O CPF deve conter exatamente 11 dígitos.");
        }
        // Armazenamos apenas os números para manter a consistência
        this.numero = numero.replaceAll("\\D", "");
    }

    public String getNumero() {
        return numero;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Cpf cpf = (Cpf) o;
        return numero.equals(cpf.numero);
    }

    @Override
    public int hashCode() {
        return numero.hashCode();
    }

    @Override
    public String toString() {
        return numero;
    }
}

```

---

## 2. Implementação Moderna (Java Record)

Os **Records** (introduzidos no Java 14/16) são perfeitos para Value Objects, pois já são imutáveis por padrão e implementam `equals`, `hashCode` e `toString` automaticamente.

```java
public record Cpf(String numero) {
    
    // Construtor compacto para validação
    public Cpf {
        if (numero == null) {
            throw new IllegalArgumentException("O número do CPF não pode ser nulo.");
        }
        
        // Remove caracteres não numéricos para validar o tamanho
        String apenasNumeros = numero.replaceAll("\\D", "");
        
        if (apenasNumeros.length() != 11) {
            throw new IllegalArgumentException("O CPF deve conter exatamente 11 dígitos.");
        }
        
        // Reatribui apenas os dígitos ao componente do record
        numero = apenasNumeros;
    }
}

```

### Principais Diferenças e Benefícios:

* **Imutabilidade:** Em ambos os casos, uma vez que o `Cpf` é criado, seu valor não pode ser alterado.
* **Validação:** O objeto "se protege". É impossível ter uma instância de `Cpf` no seu sistema que seja inválida (com 5 ou 12 dígitos, por exemplo).
* **Concisão:** Note como o `record` reduz drasticamente o "boilerplate" (código repetitivo), mantendo a mesma segurança da classe clássica.
