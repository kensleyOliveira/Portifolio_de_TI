import math

class Dijkstra:
    """
    Uma classe para executar o algoritmo de Dijkstra em um grafo
    representado por uma matriz de distâncias/pesos.
    """

    def __init__(self, W, vertices):
        """
        Inicializa a classe com a matriz de distâncias e a lista de vértices.

        Parâmetros:
        W (list of list of float): Matriz de distâncias (n x n) do grafo.
                                    math.inf deve ser usado para arestas inexistentes.
        vertices (list of str): Lista com os nomes dos vértices.
        """
        self.W = W
        self.vertices = vertices
        self.n = len(vertices)
        # Mapeia o nome do vértice para seu índice
        self.idx = {v: i for i, v in enumerate(vertices)}
        self.c = [math.inf] * self.n  # Lista de custos (distâncias mínimas)
        self.pi = [None] * self.n     # Lista de pais (para reconstruir o caminho)

    def run(self, origem):
        """
        Executa o algoritmo de Dijkstra a partir de um vértice de origem.

        Parâmetros:
        origem (str): O nome do vértice inicial.

        Retorna:
        tuple: Uma tupla contendo as listas de custos, pais e o mapeamento de índices.
        """
        origem_idx = self.idx[origem]

        # V: conjunto de todos os vértices
        V = set(range(self.n))
        # V_: conjunto de vértices cujos caminhos mais curtos já foram finalizados
        V_ = {origem_idx}
        
        # Inicializa o custo da origem como 0
        self.c[origem_idx] = 0

        # Inicializa os custos a partir da origem
        for i in range(self.n):
            if i != origem_idx:
                self.c[i] = self.W[origem_idx][i]
                if self.W[origem_idx][i] < math.inf:
                    self.pi[i] = origem_idx

        # Loop principal do algoritmo
        while V_ != V:
            # Encontra o vértice 'j' em V - V_ com o menor custo
            j = min((v for v in V - V_), key=lambda v: self.c[v])
            V_.add(j)
            
            # Atualiza os custos dos vizinhos de 'j' que ainda não foram finalizados
            for i in V - V_:
                if self.c[j] + self.W[j][i] < self.c[i]: # Se o novo custo é menor
                    self.c[i] = self.c[j] + self.W[j][i] # Atualiza o custo
                    self.pi[i] = j # Atualiza o pai

        return self.c, self.pi, self.idx # Retorna as listas de custos, pais e o mapeamento de índices

    def reconstruir_caminho(self, destino):
        """
        Reconstrói o caminho da origem até o destino usando a lista de pais.

        Parâmetros:
        destino (str): O nome do vértice de destino.

        Retorna:
        list: Uma lista de strings com os nomes dos vértices no caminho.
        """
        destino_idx = self.idx[destino] # Obtém o índice do vértice de destino
        caminho = [] # Lista para armazenar o caminho
        v = destino_idx # Vértice atual
        while v is not None: # Enquanto houver um vértice atual
            caminho.append(self.vertices[v]) # Adiciona o vértice atual ao caminho
            v = self.pi[v] # Atualiza o vértice atual para o pai
        caminho.reverse() # Inverte o caminho para ir da origem ao destino
        return caminho # Retorna o caminho reconstruído

