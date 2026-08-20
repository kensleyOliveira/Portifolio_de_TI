from dataclasses import dataclass 
from typing import List, Tuple

# --- Definição da Estrutura de Dados ---
@dataclass
class Intervalo:
    id_missao: int
    inicio: int
    fim: int
    valor: float   # recompensa

# --- Função Auxiliar de Máximo ---
def maximo(a: int, b: int) -> int:
    return a if a > b else b

# --- Função do Algoritmo de Escalonamento ---
def calcular_escalonamento_dp(intervalos: List[Intervalo]) -> Tuple[float, List[Intervalo]]:
    N = len(intervalos)
    # PASSO 1: Ordenar intervalos pelo campo 'fim'
    intervalos.sort(key=lambda x: x.fim)

    # Vetores internos para o cálculo da DP
    DP = [0] * (N + 1)
    P = [0] * (N + 1)

    # PASSO 2: Pré-computação do vetor P
    for i in range(1, N + 1):
        P[i] = 0
        for j in range(i - 1, 0, -1):
            if intervalos[j - 1].fim <= intervalos[i - 1].inicio:
                P[i] = j
                break

    # PASSO 3: Programação Dinâmica
    DP[0] = 0
    for i in range(1, N + 1):
        valor_incluindo = intervalos[i - 1].valor + DP[P[i]]
        valor_nao_incluindo = DP[i - 1]
        DP[i] = maximo(valor_incluindo, valor_nao_incluindo)

    # PASSO 4: Reconstrução da solução
    res = []
    i = N
    while i > 0:
        if intervalos[i-1].valor + DP[P[i]] > DP[i-1]:
            res.append(intervalos[i-1])
            i = P[i]
        else:
            i -= 1

    return DP[N], list(reversed(res))
