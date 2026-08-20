from modules.Lista_Matriz_adjacencia import Mapa

class TarjanTopologico: # Classe para ordenação topológica usando o algoritmo de Tarjan
    def __init__(self, mapa: Mapa): # Inicializa a classe com um mapa
        self.mapa = mapa # Armazena o mapa
        self.visitado = set() # Conjunto de vértices visitados
        self.ordem = [] # Lista para a ordem topológica

    def ordenar(self):
        """Executa o algoritmo de ordenação topológica de Tarjan."""
        for v in self.mapa.locais: # Para cada local no mapa
            if v not in self.visitado: # Se o local não foi visitado
                self._dfs(v) # Executa a busca em profundidade
        self.ordem.reverse() # Inverte a ordem para obter a topológica
        return self.ordem # Retorna a ordem topológica

    def _dfs(self, v): # Executa a busca em profundidade
        self.visitado.add(v) # Marca o vértice como visitado
        for vizinho, _ in self.mapa.locais[v]: # Para cada vizinho do vértice
            if vizinho not in self.visitado: # Se o vizinho não foi visitado
                self._dfs(vizinho) # Executa a busca em profundidade no vizinho
        self.ordem.append(v) # Adiciona o vértice à ordem
