from modules.Lista_Matriz_adjacencia import Mapa

class KruskalAGM: # Algoritmo de Kruskal para Árvore Geradora Mínima
    def __init__(self, mapa: Mapa): # Inicializa o algoritmo com um mapa
        self.mapa = mapa # Armazena o mapa

    def encontrar_agm(self): # Encontra a árvore geradora mínima
        """Executa o algoritmo de Kruskal para encontrar a árvore geradora mínima."""
        # Constrói lista de arestas
        arestas = []
        for origem, vizinhos in self.mapa.locais.items(): # Para cada local no mapa
            for destino, custo in vizinhos: # Para cada vizinho
                if (destino, origem, custo) not in arestas:  # Evita duplicar arestas
                    arestas.append((origem, destino, custo)) # Adiciona aresta

        # Ordena arestas pelo custo
        arestas.sort(key=lambda x: x[2]) # Ordena arestas pelo custo

        pai = {} # Inicializa estrutura de união-find
        def find(v): # Função para encontrar o representante de um conjunto
            while pai[v] != v: # Enquanto o pai de v não for v
                v = pai[v] # Atualiza v para seu pai
            return v # Retorna o representante do conjunto

        def union(v1, v2): # Função para unir dois conjuntos
            raiz1 = find(v1) # Encontra a raiz do conjunto de v1
            raiz2 = find(v2) # Encontra a raiz do conjunto de v2
            pai[raiz2] = raiz1 # Une os conjuntos

        # Inicializa conjuntos disjuntos
        for v in self.mapa.locais: # Para cada local no mapa
            pai[v] = v # Cada local é seu próprio pai

        agm = [] # Inicializa a árvore geradora mínima
        for origem, destino, custo in arestas: # Para cada aresta
            if find(origem) != find(destino): # Se origem e destino não estão na mesma componente
                union(origem, destino) # Une os conjuntos
                agm.append((origem, destino, custo)) # Adiciona aresta à árvore geradora mínima 

        return agm # Retorna a árvore geradora mínima
