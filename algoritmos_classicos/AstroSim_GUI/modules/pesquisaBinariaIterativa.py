import matplotlib.pyplot as plt

class BuscaBinariaIterativa:
    def __init__(self, lista, ordem='crescente', debug=False, key=lambda x: x):
        """
        Inicializa com lista e ordena conforme a ordem especificada.
        :param lista: lista de elementos (int, str ou objetos)
        :param ordem: 'crescente' ou 'decrescente'
        :param debug: imprime passos se True (debug significa depuração ou rastreamento do código para entender o que está acontencendo na execução do código)
        :param key: função de chave para comparação (default: identidade)
        """
        self.key = key # Função de chave para comparação dos elementos da lista. Por padrão, é a identidade (ou seja, compara os próprios elementos)
        self.ordem = ordem.lower() # Converte a ordem para minusculas para evitar problemas de case sensitivity
        self.debug = debug # Ativa ou desativa o modo de depuração
        self.comparacoes = 0 # Contador de comparações feitas durante a busca

        if self.ordem == 'crescente': # Se a ordem for crescente, ordena a lista em ordem crescente
            self.lista = sorted(lista, key=self.key) # Ordena a lista em ordem crescente
        elif self.ordem == 'decrescente': # Se a ordem for decrescente, ordena a lista em ordem decrescente
            self.lista = sorted(lista, key=self.key, reverse=True) # Ordena a lista em ordem descrescente
        else:
            raise ValueError("Ordem inválida. Use 'crescente' ou 'decrescente'.")
        
    # Busca binária iterativa    
    def buscar(self, item): 
        """Executa a busca binária iterativa."""
        self.comparacoes = 0 # Reseta o contador de comparações antes de iniciar a busca
        baixo = 0 # Índice inicial da busca
        alto = len(self.lista) - 1 # Índice final da busca
        alvo = item # item a ser buscado

        while baixo <= alto: # Enquanto o índice baixo for menor ou igual ao alto, continua a busca
            meio = (baixo + alto) // 2 # Calcula o índice do meio do intervalo atual
            valor_meio = self.key(self.lista[meio])  # Obtém o valor do elemento do meio usando a função de chave
            self.comparacoes += 1 # Incrementa o contador de comparações

            if self.debug: # Se o modo de depuração estiver ativado, imprime o estado atual da busca
                print(f"[DEBUG] Comparando {alvo} com {valor_meio}")

            if valor_meio == alvo:  # Se o valor do meio for igual ao valor do item, significa que o item foi encontrado
                return meio # Retorna o índice do item encontrado
            if self.ordem == 'crescente':   # Verifica a ordem da lista para decidir a direção da busca
                if alvo < valor_meio:   # Se o valor do item for menor que o valor do meio, a busca deve continuar na metade inferior da lista
                    alto = meio - 1 # Busca na metade inferior
                else:   # Se o valor do item for maior que o valor do meio, a busca deve continuar na metade superior da lista  
                    baixo = meio + 1    # Busca na metade superior
            else: # Se a ordem for descrescente, a lógica é invertida      
                if alvo > valor_meio:   # Se o valor do item for maior que o valor do meio, a busca deve continuar na metade inferior da lista
                    alto = meio - 1 # Busca na metade inferior
                else:   # Se o valor do item for menor que o valor do meio, a busca deve continuar na metade superior da lista  
                    baixo = meio + 1    # Busca na metade superior
        return None # Se o item não for encontrado, retorna None

    # @staticmethod # Método estatístico para plota o gráfico de desempenho da busca binária 
    #     # Esta funcção plota o desempenho da busca binária em termos de números de comparações feitas na busca binária em relação ao tamanho da lista.
    #     # É útil para visualizar a eficiência do algoritmo.
    #     # Comapra o desempenho da busca binária com listas de tamanhos variados, mostrando como o número de comprarções aumenta com o tamanho da lista.
    # def plot_desempenho(): # Função estática que plota o desempenho da busca binária
    #     """Plota o gráfico de comparações vs. tamanho da lista."""
    #     import random
    #     import timeit
    #     import statistics
        
    #     N_EXECUCOES = 100 # Número de execuções para calcular o tempo médio de execução
    #     tamanhos = list(range(10, 1001, 50)) # Lista de tamanhos das listas a serem testadas
    #     comparacoes = []
    #     tempos = []
        

    #     for tam in tamanhos: # Gera listas de tamanhos variados
    #         lista = sorted(random.sample(range(tam * 10), tam)) # Gera uma lista ordenada de números aleatórios
    #         alvo = random.choice(lista) # Escolhe um alvo aleatório da lista para buscar
    #         bb = BuscaBinariaIterativa(lista) # cria uma instância da busca binária com a lista gerada
    #         bb.buscar(alvo) # Realiza a busca do alvo na lista 
    #         comparacoes.append(bb.comparacoes) # Conta o número de comparações feitas na busca
    #         tempo_rec = timeit.timeit(lambda: bb.buscar(alvo), number=N_EXECUCOES) # Calcula o tempo médio de execução da busca binária iterativa
    #         tempos.append(tempo_rec / N_EXECUCOES ) # Adiciona o tempo médio de execução à lista de tempos
        
    
    
    #     print(f"Tempo médio de execução: {statistics.mean(tempos):.6f} segundos por busca\n\n")        
    #     plt.plot(tamanhos, comparacoes, marker='o') # Plota o gráfico com os tamanhos no eixo x e o número de comparações no eixo y
    #     plt.title("Comparações na Busca Binária vs. Tamanho da Lista") # Título do gráfico
    #     plt.xlabel("Tamanho da Lista") # Eixo x do gráfico
    #     plt.ylabel("Número de Comparações") # Eixo y do gráfico
    #     plt.grid(True) # Adiciona grade ao gráfico
    #     plt.show() # Exibe o gráfico
        
   