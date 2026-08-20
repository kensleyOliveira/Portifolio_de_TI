# ATIVIDADE: MAIS SOBRE SERVIÇOS

## 1. Serviço de Conversor de Moeda

Este serviço utiliza um objeto de taxas de câmbio para realizar o cálculo. Em um cenário real, essas taxas viriam de uma API externa.

```javascript
class ConversorMoeda {
  // Taxas de câmbio fictícias tendo como base 1 Unidade da Moeda A
  private taxas: Record<string, number> = {
    "USD_BRL": 5.0, // 1 Dólar = 5 Reais
    "BRL_USD": 0.2, // 1 Real = 0.20 Dólares
    "EUR_BRL": 5.4, // 1 Euro = 5.40 Reais
  };

  converter(valor: number, moedaOrigem: string, moedaDestino: string): number {
    const chave = `${moedaOrigem}_${moedaDestino}`;
    const taxa = this.taxas[chave];

    if (!taxa) {
      throw new Error("Taxa de câmbio não encontrada para este par de moedas.");
    }

    return valor * taxa;
  }
}

// Exemplo de uso:
const conversor = new ConversorMoeda();
console.log(`R$ 100,00 em USD: $${conversor.converter(100, "BRL", "USD")}`);

```

---

## 2. Serviço de Análise de Crédito

Este serviço aplica uma lógica de decisão baseada nos critérios solicitados (histórico, dívidas, salário e valor solicitado).

```javascript
class AnaliseCredito {
  avaliar(cliente: any, valorEmprestimo: number): { aprovado: boolean, motivo: string } {
    const { historicoCompras, dividasAtivas, salario } = cliente;

    // Regra 1: Verificação de Dívidas
    if (dividasAtivas > 0) {
      return { aprovado: false, motivo: "Cliente possui dívidas ativas pendentes." };
    }

    // Regra 2: Comprometimento de Renda (Parcela não pode exceder 30% do salário)
    // Simulando um empréstimo em 12x para o cálculo da parcela
    const parcelaEstimada = valorEmprestimo / 12;
    if (parcelaEstimada > salario * 0.3) {
      return { aprovado: false, motivo: "Valor da parcela excede 30% da renda mensal." };
    }

    // Regra 3: Histórico de Compras (Exemplo: mínimo de 5 compras realizadas)
    if (historicoCompras < 5) {
      return { aprovado: false, motivo: "Histórico de compras insuficiente para análise." };
    }

    return { aprovado: true, motivo: "Crédito pré-aprovado com sucesso!" };
  }
}

// Exemplo de uso:
const analista = new AnaliseCredito();
const clienteExemplo = { historicoCompras: 10, dividasAtivas: 0, salario: 5000 };
const resultado = analista.avaliar(clienteExemplo, 10000);

console.log(resultado.aprovado ? "✅" : "❌", resultado.motivo);

```

---

### O que esses serviços resolvem:

* **Encapsulamento:** A lógica de negócio (cálculo de câmbio e regras de crédito) fica isolada, facilitando a manutenção.
* **Reutilização:** Você pode chamar esses métodos de qualquer parte do seu sistema (um controlador de API, uma interface web, etc.).
