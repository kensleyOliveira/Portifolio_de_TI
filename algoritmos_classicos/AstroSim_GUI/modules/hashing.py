import math # Este módulo é necessário para algumas operações matemáticas

class Hashing: # Classe para implementar diferentes métodos de hashing
    """Classe que implementa diferentes métodos de hashing."""
    def __init__(self, tamanho=10, metodo_colisao='encadeamento', tipo_hash='divisao'): # Inicializa a tabela hash com o tamanho especificado, método de colisão e tipo de hash
        """ Inicializa a tabela hash com o tamanho especificado, método de colisão e tipo de hash.
        Args:
            tamanho (int): Tamanho da tabela hash.
            metodo_colisao (str): Método de resolução de colisão ('encadeamento' ou 'endereco_aberto').
            tipo_hash (str): Tipo de função hash ('divisao', 'multiplicacao', 'meio_quadrado', 'extracao', 'raiz', 'xor', 'rotacao', 'peso').
        """
        self.tamanho = tamanho # Tamanho da tabela hash
        # Inicializa a tabela hash com listas vazias para encadeamento ou None para endereçamento aberto
        # A tabela hash é uma lista de listas (para encadeamento) ou uma lista de None (para endereçamento aberto)
        self.tabela = [[] for _ in range(tamanho)] if metodo_colisao == 'encadeamento' else [None] * tamanho
        self.metodo_colisao = metodo_colisao
        self.tipo_hash = tipo_hash

    def calcular_hash(self, chave): # Método para calcular o hash da chave usando o tipo de hash especificado
        """Calcula o índice da tabela hash para a chave fornecida."""
        if isinstance(chave, str): # Se a chave for uma string, converte para um valor numérico
            chave = self._converter_alfanumerica(chave) # Converte a chave alfanumérica para um valor numérico

        if self.tipo_hash == 'divisao': # Método de divisão: usa o módulo do tamanho da tabela
            return chave % self.tamanho # Retorna o índice da tabela hash usando o método de divisão
        elif self.tipo_hash == 'multiplicacao': # Método de multiplicação: usa a constante A para calcular o índice
            A = 0.6180339887  # (a razão áurea inversa) possui propriedades matemáticas que ajudam a distribuir as chaves de forma mais uniforme na tabela.
            return int(self.tamanho * ((chave * A) % 1)) # Retorna o índice da tabela hash usando o método de multiplicação
        elif self.tipo_hash == 'meio_quadrado': # Método do meio quadrado: calcula o quadrado da chave e extrai os dígitos do meio
            quadrado = chave * chave # Calcula o quadrado da chave
            meio = int(str(quadrado)[len(str(quadrado))//2 - 1: len(str(quadrado))//2 + 1]) # Extrai os dígitos do meio do quadrado
            return meio % self.tamanho # Retorna o índice da tabela hash usando o método do meio quadrado
        elif self.tipo_hash == 'extracao': # Método de extração: extrai parte da chave para calcular o índice
            str_chave = str(chave) # Converte a chave para string
            extraido = int(str_chave[1:3]) if len(str_chave) > 3 else chave # Extrai os dois primeiros dígitos da chave (ou usa a chave inteira se for menor que 3 dígitos)
            return extraido % self.tamanho # Retorna o índice da tabela hash usando o método de extração
        elif self.tipo_hash == 'raiz': # Método da raiz quadrada: calcula a raiz quadrada da chave e usa a parte decimal
            raiz = int((chave ** 0.5) * 100) # Calcula a raiz quadrada da chave e multiplica por 100 para obter uma parte inteira
            return raiz % self.tamanho # Retorna o índice da tabela hash usando o método da raiz quadrada
        elif self.tipo_hash == 'xor': # Método XOR: aplica a operação XOR em todos os caracteres da chave
            return self._xor_hash(str(chave)) % self.tamanho # Retorna o índice da tabela hash usando o método XOR
        elif self.tipo_hash == 'rotacao': # Método de rotação: aplica uma rotação de bits nos caracteres da chave
            return self._rotacao_bits(str(chave)) % self.tamanho # Retorna o índice da tabela hash usando o método de rotação
        elif self.tipo_hash == 'peso': # Método de peso: calcula o peso da chave baseado na posição dos caracteres
            return self._peso_por_posicao(str(chave)) % self.tamanho # Retorna o índice da tabela hash usando o método de peso
        else:
            raise ValueError("Tipo de hash desconhecido") # Se o tipo de hash não for reconhecido, lança um erro

    def inserir(self, chave, valor): # Método para inserir um par chave-valor na tabela hash
        indice = self.calcular_hash(chave) # Calcula o índice da tabela hash para a chave fornecida
        if self.metodo_colisao == 'encadeamento': # Se o método de colisão for encadeamento, insere o par na lista correspondente
            for par in self.tabela[indice]: # Verifica se a chave já existe na lista
                # Se a chave já existe, atualiza o valor
                if par[0] == chave:
                    par[1] = valor
                    return
            self.tabela[indice].append([chave, valor]) # Adiciona o novo par chave-valor na lista
        else:  # Se o método de colisão for endereçamento aberto, procura um espaço vazio na tabela
            # Percorre a tabela até encontrar um espaço vazio ou a chave já existente
            original = indice
            while self.tabela[indice] is not None and self.tabela[indice][0] != chave: 
                indice = (indice + 1) % self.tamanho
                if indice == original:
                    raise Exception("Tabela Hash cheia")
            self.tabela[indice] = [chave, valor]

    def buscar(self, chave): # Método para buscar um valor na tabela hash usando a chave
        """Busca um valor na tabela hash usando a chave fornecida.
        Args:
            chave (str): A chave a ser buscada na tabela hash.
        Returns:
            _type_: O valor associado à chave, ou None se a chave não for encontrada.
        """
        indice = self.calcular_hash(chave) # Calcula o índice da tabela hash para a chave fornecida
        # Se o método de colisão for encadeamento, percorre a lista correspondente
        if self.metodo_colisao == 'encadeamento':
            for par in self.tabela[indice]:
                if par[0] == chave:
                    return par[1]
            return None
        else: # Se o método de colisão for endereçamento aberto, procura a chave na tabela
            # Percorre a tabela até encontrar a chave ou um espaço vazio
            original = indice
            while self.tabela[indice] is not None:
                if self.tabela[indice][0] == chave:
                    return self.tabela[indice][1]
                indice = (indice + 1) % self.tamanho
                if indice == original:
                    break
            return None

    def remover(self, chave): # Método para remover um par chave-valor da tabela hash
        """Remove um par chave-valor da tabela hash.
        Args:
            chave (str): A chave a ser removida da tabela hash.
        Returns:
            bool: True se a chave foi removida, False se a chave não foi encontrada.
        """
        indice = self.calcular_hash(chave) # Calcula o índice da tabela hash para a chave fornecida
        # Se o método de colisão for encadeamento, percorre a lista correspondente
        if self.metodo_colisao == 'encadeamento':
            for i, par in enumerate(self.tabela[indice]):
                if par[0] == chave:
                    del self.tabela[indice][i]
                    return True
        else: # Se o método de colisão for endereçamento aberto, procura a chave na tabela
            # Percorre a tabela até encontrar a chave ou um espaço vazio
            original = indice
            while self.tabela[indice] is not None:
                if self.tabela[indice][0] == chave:
                    self.tabela[indice] = None
                    return True
                indice = (indice + 1) % self.tamanho
                if indice == original:
                    break
        return False # Se a chave não foi encontrada, retorna False

    '''  ========================
            Funções auxiliares
         ========================
'''
    def _converter_alfanumerica(self, chave_str): # Método para converter uma chave alfanumérica em um valor numérico
        """Converte uma chave alfanumérica em um valor numérico."""
        return sum(ord(c) for c in chave_str)

    def _xor_hash(self, chave_str): # Método para calcular o hash usando a operação XOR
        """Calcula o hash usando a operação XOR em todos os caracteres da chave."""
        result = 0
        for c in chave_str: # Percorre cada caractere da chave
            # ord() converte cada caractere em seu valor numérico (Unicode/ASCII).
            # A operação XOR é aplicada entre o resultado acumulado e o valor do caractere  
            result ^= ord(c) # Desloca os bits do valor do caractere para a esquerda e combina com o deslocamento para a direita
        return result

    def _rotacao_bits(self, chave_str): # Método para calcular o hash usando rotação de bits
        """Calcula o hash usando rotação de bits."""
        total = 0
        for i, c in enumerate(chave_str): # Converte cada caractere em seu valor numérico e aplica a rotação
            # ord() converte cada caractere em seu valor numérico (Unicode/ASCII).
            # A rotação é feita deslocando os bits do valor do caractere para a esquerda
            valor = ord(c) # Desloca os bits do valor do caractere para a esquerda
            rot = (valor << i) | (valor >> (8 - i)) # Desloca os bits do valor do caractere para a esquerda e combina com o deslocamento para a direita
            total += rot # Adiciona o valor rotacionado ao total
        return total

    def _peso_por_posicao(self, chave_str): # Método para calcular o hash baseado no peso dos caracteres por posição
        """Calcula o hash baseado no peso dos caracteres por posição."""
        return sum((i+1) * ord(c) for i, c in enumerate(chave_str)) # Calcula o peso de cada caractere multiplicando pelo seu índice (começando em 1) e somando os resultados

    def imprimir(self): # Método para imprimir a tabela hash
        """Imprime a tabela hash."""
        for i, item in enumerate(self.tabela):
            print(f"{i}: {item}")