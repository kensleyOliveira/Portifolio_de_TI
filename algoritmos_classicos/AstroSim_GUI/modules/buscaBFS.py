# Algoritmo BFS para uma leitura através de uma Matriz de Adjacência
from collections import deque

class BFS:
    """
    Uma classe para executar o algoritmo de Busca em Largura (BFS)
    em um grafo representado por uma lista de adjacência.
    """
    def __init__(self, lista_adj, vertices):
        """
        Inicializa a classe com a lista de adjacência e os vértices.
        
        Parâmetros:
        lista_adj (dict): Dicionário representando a lista de adjacência.
                          Ex: {'A': [('B', 1), ('C', 1)]}
        vertices (list): Lista com os nomes de todos os vértices.
        """
        self.lista_adj = lista_adj
        self.vertices = vertices
        self.cor = {}
        self.distancia = {}
        self.pai = {}
        self.Q = deque()
    
    def run(self, s):
        """
        Executa o algoritmo BFS a partir de um vértice de origem 's'.
        
        Parâmetros:
        s (str): O nome do vértice de origem para a busca.
        """
        # Inicialização
        for u in self.vertices: # Para cada vértice
            self.cor[u] = "branco" # Cor inicial
            self.distancia[u] = float("inf") # Distância inicial
            self.pai[u] = None # Pai inicial
        
        # Inicialização do vértice de origem
        self.cor[s] = "cinzento" # Cor do vértice de origem
        self.distancia[s] = 0 # Distância do vértice de origem
        self.pai[s] = None # Pai do vértice de origem

        self.Q.append(s) # Adiciona o vértice de origem à fila

        while self.Q: # Enquanto a fila não estiver vazia
            u = self.Q.popleft() # Remove o primeiro elemento da fila

            # Percorre os vizinhos de 'u'
            for v, _ in self.lista_adj.get(u, []): # Para cada vizinho de 'u'
                if self.cor[v] == "branco": # Se o vizinho for branco
                    self.cor[v] = "cinzento" # Marca o vizinho como cinza
                    self.distancia[v] = self.distancia[u] + 1 # Atualiza a distância do vizinho
                    self.pai[v] = u # Atualiza o pai do vizinho
                    self.Q.append(v) # Adiciona o vizinho à fila

            self.cor[u] = "preto" # Marca o vértice como preto

        return self.cor, self.distancia, self.pai # Retorna as informações de cor, distância e pai
