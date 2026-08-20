'''É uma técnica eficiente de pesquisa de padrões em Strings, especialmente útil quando necessita producar 
multiplos padrões ao mesmo tempo'''

import unicodedata # Biblioteca utilizada para remover acentos dos caracteres (normalização Unicode)

# Classe Rabin-Karp-Matcher
class RabinKarp:
    
    # Construtor da classe
    def __init__(self, base=256):
        self.base = base # Base numérica usada para clacular o hash, considerando todos os caracteres ACII estendidos
        self.primo = None # número primo usado como modulador no cálculo do hash (reduz colisões)
     
    # Método para seleção do primo a ser utilizado  
    def escolher_primo(self, tamanho_texto): # Método que escolhe um número primo baseado no tamanho do texto
        if tamanho_texto <= 200: # Retorna o primo 101 para textos pequenos
            return 101
        elif tamanho_texto <= 1100: # Retorna o primo 257 para textos médios
            return 997
        elif tamanho_texto <= 9000: # Retorna o primo 1009 para textos grandes
            return 1009
        elif tamanho_texto <= 900000: # Retorna o primo 131071 para textos muito grandes
            return 131071
        else:
            return 1000000007

    # Método de normalização do texto
    def normalizar(self, texto): # Método que normaliza o texto para facilitar a busca
        texto = texto.lower()# Converte o texto todo para maísculas, tornando a busca case-insensitive
        texto = unicodedata.normalize('NFD', texto)#Separa letras acentuadas em letra base + marca de acento
        texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')#Apaga os acentos 
        return texto

    # Método busca do padrão no texto
    def buscar(self, texto, padrao): # Método que busca o padrão no texto
        
        texto_original = texto # Guarda o texto originial para retornar os trechos reais
        
        # Converte o texto para minúsculo e sem acentos
        texto_norm = self.normalizar(texto) # Normaliza o texto para facilitar a busca
        padrao_norm = self.normalizar(padrao) # Normaliza o padrão para facilitar a busca

        # Verifica se o padrão é maior que o texto.
        n = len(texto_norm) # Tamanho do texto normalizado
        m = len(padrao_norm) # Tamanho do padrão normalizado
        if m > n: # Se o padrão é maior que o texto, não há como encontrar
            return 0, [], [] # O texto é menor que padrão - retorna zero

        # Define o primo dinamicamente com base no tamanho do texto
        self.primo = self.escolher_primo(n) # Escolhe um número primo adequado para o tamanho do texto
        
        # Inicialização das variáveis, utilizadas no cálculo do hash
        hash_padrao = 0 # Hash do padrão 
        hash_texto = 0 # Hash da janela atual do texto
        h = 1

        # Cálculo do valor de h, usado no "rolling hash"
        for i in range(m - 1):# Calcula h como base^(m-1) % primo
            h = (h * self.base) % self.primo #  h é usado para remover o caractere mais à esquerda da janela atual do texto

        # Cálcula o hash do padrão e ad primeira janela de texto (primeiros m caracteres)
        for i in range(m): # Itera sobre os primeiros m caracteres do padrão e do texto
            # hash_padrao e hash_texto são calculados como uma soma ponderada dos valores   
            
            # ord() converte cada caractere em seu valor numérico (Unicode/ASCII).
            hash_padrao = (self.base * hash_padrao + ord(padrao_norm[i])) % self.primo # Calcula o hash do padrão
            hash_texto = (self.base * hash_texto + ord(texto_norm[i])) % self.primo # Calcula o hash da primeira janela do texto

        posicoes = [] # Lista posicoes: onde o padrão foi encontrado (índice no texto normalizado).
        trechos = [] # Lista trechos: trecho original do texto onde foi encontrada a ocorrência.
        contagem = 0 #Variável contagem: número total de ocorrências.

        # Percorre o texto até o último ponto onde ainda cabe uma janela de tamanho m.
        for i in range(n - m + 1): #    Percorre o texto normalizado até o último ponto onde ainda cabe uma janela de tamanho m
            
            # Se o hash do padrão bate com o hash da janela atual, faz a verificação caractere a caractere.
            if hash_padrao == hash_texto: # Se os hashes são iguais, pode haver uma correspondência
                if texto_norm[i:i + m] == padrao_norm: # Verifica se a janela atual do texto corresponde ao padrão
                    posicoes.append(i) # Armazena o índice da ocorrência
                    trechos.append(texto_original[i:i + m]) # Armazena o trecho original (com acento, maiúsculas, entre outros)
                    contagem += 1 # Incrementa a contagem
            
            # Atualiza o hash da janela para a próxima posição (rolling hash)
            if i < n - m: # Se não for a última janela, atualiza o hash
                
                # Subtrai o caractere que está saindo, adiciona o caractere que está entrando
                # e usa % primo para manter o hash positivo e pequeno
                hash_texto = (self.base * (hash_texto - ord(texto_norm[i]) * h) + ord(texto_norm[i + m])) % self.primo # Atualiza o hash da janela atual do texto
                
                # Faz uma correção, a fim de evitar que o valor do hash torne-se negativo,
                # o que pode acontecer durante o cálculo do "rolling hash
                if hash_texto < 0: #    Se o hash_texto ficou negativo, corrige
                    hash_texto += self.primo # Corrige o hash para que fique positivo

        # Retorna número de vezes que o padrão apareceu, Lista de posições normalizadas, lista de 
        # trechos originais encontrados
        return contagem, posicoes, trechos # Retorna a contagem de ocorrências, as posições e os trechos encontrados
