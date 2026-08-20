# ATIVIDADE: MAIS SOBRE OBJETOS DE VALOR (2)

### 4. Temperatura (Slide 2)

Implementação da lógica de Zero Absoluto e conversão para Fahrenheit.
A fórmula utilizada é $F = C \times 1.8 + 32$.

```java
public record Temperatura(double celsius) {
    public Temperatura {
        if (celsius < -273.15) {
            throw new IllegalArgumentException("Temperatura abaixo do zero absoluto!");
        }
    }

    public double toFahrenheit() {
        return (celsius * 1.8) + 32;
    }
}

```


### Por que isso é bom?

1. **Validação na Porta:** O objeto só passa a existir se for válido.
2. **Sem Efeitos Colaterais:** Como são imutáveis, você pode passar esses objetos para qualquer parte do código sem medo de que o valor mude.
3. **Conciso:** O que levaria dezenas de linhas com classes comuns foi resolvido com poucas linhas usando `record`.

