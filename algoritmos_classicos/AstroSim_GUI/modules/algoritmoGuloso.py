
class Item:
    def __init__(self, nome, valor, peso):
        self.nome = nome
        self.valor = float(valor)
        self.peso = float(peso)
        # Calcula a razão valor/peso
        self.ratio = self.valor / self.peso if self.peso > 0 else 0
    def __repr__(self):
        return f"{self.nome}(valor={self.valor}, peso={self.peso}, ratio={self.ratio:.2f})"

def selecionar_melhor_candidato(candidatos, chave=lambda x: x):
    return max(candidatos, key=chave) if candidatos else None

def eh_viavel(capacidade_restante, peso_item):
    return peso_item <= capacidade_restante

def ordenar_por(lista, chave, reverso=False):
    return sorted(lista, key=chave, reverse=reverso)

def algoritmo_guloso(candidatos, capacidade, chave=lambda x: x.ratio):
    """ Resolve o Problema da Mochila 0/1 (heurística gulosa) """
    solucao = []
    capacidade_restante = capacidade
    candidatos = candidatos.copy()
    while candidatos and capacidade_restante > 0:
        item = selecionar_melhor_candidato(candidatos, chave)
        candidatos.remove(item)
        if eh_viavel(capacidade_restante, item.peso):
            solucao.append(item)
            capacidade_restante -= item.peso
    return solucao

# ---------------------------
# NOVA FUNÇÃO: Mochila Fracionária (greedy ótimo)
# ---------------------------
def algoritmo_guloso_fracionario(candidatos, capacidade):
    """
    Resolve o Problema da Mochila Fracionária usando um algoritmo guloso.
    'candidatos' é uma lista de objetos 'Item' (ou similar)
    que devem ter .peso, .valor, e .ratio.
    'capacidade' é o peso máximo da mochila.

    Retorna uma lista de tuplas: (item_original, peso_coletado)
    """
    solucao_final = []
    capacidade_restante = float(capacidade)
    
    # Ordenar candidatos pela melhor razão (valor/peso), decrescente
    candidatos_ordenados = sorted(candidatos, key=lambda x: x.ratio, reverse=True)
    
    for item in candidatos_ordenados:
        if capacidade_restante <= 0:
            break # Mochila cheia

        # O 'item.peso' é o peso *total disponível* da amostra
        # Determina quanto pegar: ou tudo, ou o que resta de capacidade
        peso_a_coletar = min(item.peso, capacidade_restante)
        
        if peso_a_coletar > 0:
            solucao_final.append((item, peso_a_coletar))
            capacidade_restante -= peso_a_coletar
            
    return solucao_final

# ---------------------------
# FUNÇÃO EXISTENTE: Escalonamento de intervalos (greedy)
# ---------------------------
def escalonar_missoes(missoes):
    """
    Recebe 'missoes' como lista de dicts com chaves:
      'id_missao', 'nome_missao', 'planeta_alvo', 'data_missao',
      'tempo_inicio', 'tempo_fim', 'recompensa_valor'
    Retorna a lista de missões selecionadas (ordem por tempo_fim asc) que
    maximizam o número de missões sem sobreposição (algoritmo guloso clássico).
    """
    # ordenar por tempo_fim (e por tempo_inicio como tie-breaker)
    sorted_m = sorted(missoes, key=lambda m: (m["data_missao"], int(m["tempo_fim"]), int(m["tempo_inicio"])))
    selecionadas = []
    ultimo_fim_por_data = {}  # key = data_missao, value = ultimo fim selecionado

    for m in sorted_m:
        data = m["data_missao"]
        inicio = int(m["tempo_inicio"])
        fim = int(m["tempo_fim"])
        ultimo_fim = ultimo_fim_por_data.get(data, None)
        if ultimo_fim is None or inicio >= ultimo_fim:
            selecionadas.append(m)
            ultimo_fim_por_data[data] = fim

    return selecionadas