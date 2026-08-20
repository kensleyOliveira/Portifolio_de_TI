
class DFS: # Classe para busca em profundidade (Depth-First Search)
    def __init__(self, grafo, dirigido=False):
        """
        grafo: dict de adjacência.
          Aceita:
            - {'A': ['B','C']}  (sem pesos)
            - {'A': [('B',1), ('C',3)]}  (com pesos)
        """
        self.grafo = grafo # Grafo representado como um dicionário de adjacência
        self.dirigido = dirigido # Indica se o grafo é dirigido

    # --- utilitário: itera vizinhos sempre como (v, peso) ---
    def _vizinhos(self, v):
        for item in self.grafo.get(v, []): # Itera sobre os vizinhos do nó v
            if isinstance(item, tuple): # Verifica se o item é uma tupla (com peso)
                # ('B', 1) -> ('B', 1)
                if len(item) == 1: # Se a tupla tem apenas um elemento
                    yield item[0], 1 #  Se não houver peso, assume peso 1
                else:
                    yield item[0], item[1] # Se houver peso, usa o peso fornecido
            else:
                # 'B' -> ('B', 1)
                yield item, 1 # Se não houver peso, assume peso 1

    # --- DFS para encontrar caminho origem->destino ---
    def buscar(self, origem, destino):
        """
        Retorna lista [(no, pai, custo_acumulado), ...]
        ou [] se não houver caminho.
        """
        if origem not in self.grafo or destino not in self.grafo:
            # ainda assim pode existir nó isolado; trate com get
            pass

        visitado = set() # Conjunto de nós visitados
        pai = {} # Dicionário para armazenar o pai de cada nó
        custo = {} # Dicionário para armazenar o custo acumulado de cada nó

        visitado.add(origem) # Marca o nó de origem como visitado
        pai[origem] = None # O pai do nó de origem é None
        custo[origem] = 0 # Custo acumulado do nó de origem é 0

        achou = [False]  # usar lista para fechar sobre a variável no nested def

        def dfs(u): # Função recursiva para busca em profundidade
            if u == destino: # Se o nó atual é o destino
                achou[0] = True # Marca que o destino foi encontrado
                return True # Retorna True para indicar que o destino foi encontrado
            for v, w in self._vizinhos(u): # Itera sobre os vizinhos do nó atual
                if v not in visitado: # Se o vizinho ainda não foi visitado
                    visitado.add(v) # Marca o vizinho como visitado
                    pai[v] = u # O pai do vizinho é o nó atual
                    custo[v] = custo[u] + w # Atualiza o custo acumulado do vizinho
                    if dfs(v): # Chama a função recursiva para o vizinho
                        return True # Retorna True se o destino for encontrado
            return False # Retorna False se o destino não for encontrado

        dfs(origem) # Inicia a busca a partir do nó de origem

        if not achou[0]: # Se o destino não foi encontrado
            return [] # Retorna lista vazia

        # reconstrói a trilha (destino -> origem) e inverte
        trilha = [] # Lista para armazenar a trilha do caminho
        v = destino # Nó atual
        while v is not None: # Enquanto houver um nó atual
            trilha.append((v, pai.get(v), custo.get(v, 0))) # Adiciona o nó atual, seu pai e o custo acumulado à trilha
            v = pai.get(v) # Atualiza o nó atual para o pai
        trilha.reverse() # Inverte a trilha para ficar na ordem correta (origem -> destino)
        return trilha # Retorna a trilha encontrada