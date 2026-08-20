import pandas as pd # Usado para a visualização da matriz de adjacências.
import numpy as np # Usado para criar a matriz com valores infinitos.

class Mapa:
    """
    Representa um mapa como um grafo, onde os locais são vértices e as rotas
    são bordas (arestas) com custos.
    """
    def __init__(self):
        # A representação principal do grafo é a lista de adjacências.
        # Usa um dicionário onde a chave é o local e o valor é uma lista de tuplas
        # (destino, custo).
        self.locais = {}

    def adicionar_local(self, local):
        """Adiciona um novo local (vértice) ao mapa."""
        if local not in self.locais:
            self.locais[local] = []
            print(f"✅ Local '{local}' adicionado ao mapa.")
        else:
            print(f"⚠️ Aviso: Local '{local}' já existe no mapa.")

    def remover_local(self, local):
        """Remove um local (vértice) e todas as rotas conectadas a ele."""
        if local in self.locais: # Verifica se o local existe
            del self.locais[local] 
            # Remove todas as rotas que tinham 'local' como destino
            for origem in self.locais: # Para cada local de origem
                self.locais[origem] = [ # Atualiza as rotas de origem
                    (destino, custo) # Adiciona a rota de destino e custo
                    for destino, custo in self.locais[origem] # Para cada rota de origem
                    if destino != local # Se o destino não for o local a ser removido
                ]
            print(f"❌ Local '{local}' e suas rotas foram removidos.")
        else:
            print(f"⚠️ Erro: Local '{local}' não encontrado no mapa.")

    def adicionar_rota(self, origem, destino, custo, direcionada=False):
        """
        Adiciona uma rota (borda) entre dois locais.
        Se 'direcionada' for False, a rota é bidirecional.
        """
        # Garante que os locais existam
        if origem not in self.locais: # Verifica se a origem existe
            self.adicionar_local(origem) # Adiciona a origem se não existir
        if destino not in self.locais: # Verifica se o destino existe
            self.adicionar_local(destino) # Adiciona o destino se não existir

        # Adiciona a rota da origem para o destino
        self.locais[origem].append((destino, custo)) # Adiciona a rota de destino e custo

        # Se não for direcionada, adiciona a rota de volta
        if not direcionada: # Se não for direcionada
            self.locais[destino].append((origem, custo)) # Adiciona a rota de origem e custo

        print(f"➕ Rota adicionada: '{origem}' para '{destino}' com custo {custo}.")

    def remover_rota(self, origem, destino, direcionada=False):
        """Remove uma rota específica."""
        try:
            # Remove a rota da origem para o destino
            self.locais[origem] = [ # Atualiza as rotas de origem
                (dest, custo) # Adiciona a rota de destino e custo
                for dest, custo in self.locais[origem] # Para cada rota de origem
                if dest != destino # Se o destino não for o local a ser removido
            ]

            # Se a rota não é direcionada, remove a rota de volta
            if not direcionada: # Se não for direcionada
                self.locais[destino] = [ # Atualiza as rotas de destino
                    (orig, custo) # Adiciona a rota de origem e custo
                    for orig, custo in self.locais[destino] # Para cada rota de destino
                    if orig != origem # Se a origem não for o local a ser removido
                ]
            print(f"➖ Rota removida: '{origem}' para '{destino}'.")

        except KeyError:
            print(f"⚠️ Erro: Local '{origem}' ou '{destino}' não encontrado.")

    def visualizar_lista_adjacencias(self): # Visualiza a lista de adjacências
        """Imprime a estrutura do mapa usando a representação de lista de adjacências."""
        print("\n" + "="*40) # Início da visualização da lista de adjacências
        print("Estrutura do Mapa (Lista de Adjacências)") # Título da visualização
        print("="*40) # Fim da visualização da lista de adjacências
        for local, rotas in self.locais.items(): # Para cada local e suas rotas
            print(f"[{local}] -> {rotas}") # Exibe as rotas do local
        print("="*40) # Fim da visualização da lista de adjacências

    def visualizar_matriz_adjacencias(self):
        """Imprime a estrutura do mapa usando a representação de matriz de adjacências."""
        print("\n" + "="*40) # Início da visualização da matriz de adjacências
        print("Estrutura do Mapa (Matriz de Adjacências)") # Título da visualização
        print("="*40) # Fim da visualização da matriz de adjacências

        # Cria uma lista de todos os locais para os eixos da matriz
        locais_ordenados = sorted(list(self.locais.keys())) # Ordena os locais alfabeticamente
        tamanho = len(locais_ordenados) # Tamanho da matriz

        # Cria uma matriz N x N preenchida com zero
        matriz = np.zeros((tamanho, tamanho), dtype=int) # Matriz de adjacência

        # Mapeia cada local para seu índice na matriz
        indice = {local: i for i, local in enumerate(locais_ordenados)} # Mapeamento de locais para índices

        # Preenche a matriz com os custos das rotas
        for origem, rotas in self.locais.items(): # Para cada local de origem
            for destino, custo in rotas: # Para cada rota de destino
                i = indice[origem] # Índice da origem
                j = indice[destino] # Índice do destino
                matriz[i, j] = custo # Preenche a matriz com o custo

        # Usa pandas para uma visualização formatada
        df = pd.DataFrame(matriz, index=locais_ordenados, columns=locais_ordenados)
        print(df) # Exibe a matriz de adjacência
        print("="*40) # Fim da visualização da matriz de adjacência

    def get_lista_adjacencia(self): 
        """
        Retorna a lista de adjacência em formato de dicionário:
        { 'Sol': ['Mercúrio (0.49 UA)', 'Terra (0.51 UA)'], ... }
        """
        resultado = {} # Dicionário para armazenar a lista de adjacência
        for origem, rotas in self.locais.items(): # Para cada local de origem
            resultado[origem] = [f"{destino} ({custo})" for destino, custo in rotas] # Lista de destinos e custos
        return resultado # Retorna a lista de adjacência

    def get_matriz_adjacencia(self):
        """
        Retorna a matriz de adjacência e a lista de locais:
        matriz[i][j] = custo (ou 0 se não houver)
        locais = lista de todos os locais na ordem da matriz
        """
        import numpy as np 
        import pandas as pd

        locais_ordenados = sorted(list(self.locais.keys())) # Ordena os locais alfabeticamente
        tamanho = len(locais_ordenados) # Tamanho da matriz
        matriz = [[0 for _ in range(tamanho)] for _ in range(tamanho)] # Matriz de adjacência
        indice = {local: i for i, local in enumerate(locais_ordenados)} # Mapeamento de locais para índices

        for origem, rotas in self.locais.items(): # Para cada local de origem
            for destino, custo in rotas: # Para cada rota de destino
                i = indice[origem] # Índice da origem
                j = indice[destino] # Índice do destino
                matriz[i][j] = custo # Preenche a matriz com o custo

        return matriz, locais_ordenados # Retorna a matriz de adjacência e a lista de locais
