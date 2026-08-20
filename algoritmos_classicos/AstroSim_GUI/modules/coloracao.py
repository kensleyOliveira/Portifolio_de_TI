from modules.Lista_Matriz_adjacencia import Mapa

class WelchPowell: # Algoritmo de Welch-Powell para Coloração de Grafos
    def __init__(self, mapa: Mapa): # Inicializa o algoritmo com um mapa
        self.mapa = mapa # Armazena o mapa

    def colorir(self):
        """Executa o algoritmo de Welch-Powell para coloração do grafo."""
        # Ordena os vértices por grau (quantidade de conexões), em ordem decrescente
        vertices = sorted(self.mapa.locais.keys(),
                          key=lambda v: len(self.mapa.locais[v]),
                          reverse=True)

        cores = {}   # Armazena a cor de cada vértice
        cor_atual = 1 # Cor atual a ser atribuída

        for v in vertices: # Para cada vértice
            if v not in cores: # Se o vértice ainda não foi colorido
                cores[v] = cor_atual # Atribui a cor atual ao vértice
                # Tenta colorir outros vértices não adjacentes com a mesma cor
                for u in vertices:
                    if u not in cores and not self._adjacente(u, cores, cor_atual): # Se o vértice não está colorido e não é adjacente
                        cores[u] = cor_atual # Atribui a cor atual ao vértice
                cor_atual += 1 # Incrementa a cor atual

        return cores # Retorna o dicionário de cores

    def _adjacente(self, vertice, cores, cor):
        """Verifica se o vértice tem algum vizinho já colorido com a mesma cor."""
        for vizinho, _ in self.mapa.locais[vertice]: # Para cada vizinho do vértice
            if vizinho in cores and cores[vizinho] == cor: # Se o vizinho está colorido com a mesma cor
                return True # Retorna True se encontrar um vizinho com a mesma cor
        return False # Retorna False se não encontrar
