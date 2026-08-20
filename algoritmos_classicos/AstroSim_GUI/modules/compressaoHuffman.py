import json # Huffman coding module

class NoHuffman: # Classe que representa um nó na árvore de Huffman
    """Classe que representa um nó na árvore de Huffman."""
    def __init__(self, caractere=None, frequencia=0): # Inicializa o nó com um caractere e sua frequência
        """ Inicializa um nó da árvore de Huffman.
        Args:
            caractere (str): Caractere associado ao nó (None para nós internos).
            frequencia (int): Frequência do caractere no texto.
        """
        self.caractere = caractere # Caractere associado ao nó (None para nós internos)
        self.frequencia = frequencia # Frequência do caractere no texto
        # Inicializa os filhos esquerdo e direito como None         
        self.esquerda = None # Filho esquerdo do nó
        self.direita = None # Filho direito do nó

    def eh_folha(self): # Método que verifica se o nó é uma folha (não tem filhos)
        """Verifica se o nó é uma folha (não tem filhos)."""    
        return self.esquerda is None and self.direita is None # Verifica se o nó não tem filhos esquerdo e direito, ou seja, é uma folha


def codificar_huffman(texto):
    """Codifica o texto usando o algoritmo de Huffman e retorna o binário e a raiz da árvore."""
    frequencias = {} # Dicionário para armazenar a frequência de cada caractere no texto
    for c in texto: # Percorre cada caractere do texto
        # Atualiza a frequência do caractere no dicionário
        frequencias[c] = frequencias.get(c, 0) + 1 # Incrementa a frequência do caractere

    arvores = [NoHuffman(c, f) for c, f in frequencias.items()] # Cria uma lista de nós Huffman a partir das frequências
    # Ordena os nós pela frequência
    arvores.sort(key=lambda no: no.frequencia) # Ordena a lista de nós Huffman pela frequência

    while len(arvores) > 1: # Enquanto houver mais de um nó na lista, continua a construir a árvore
        # Remove os dois nós com menor frequência e cria um novo nó pai
        t1 = arvores.pop(0) # Primeiro nó com menor frequência
        t2 = arvores.pop(0) # Segundo nó com menor frequência
        # Cria um novo nó pai com a soma das frequências dos dois nós removidos
        novo_no = NoHuffman(None, t1.frequencia + t2.frequencia) # Cria um novo nó pai com a soma das frequências dos dois nós removidos
        novo_no.esquerda = t1 # Define o filho esquerdo como o primeiro nó removido
        # Define o filho direito como o segundo nó removido
        novo_no.direita = t2 # Adiciona o novo nó pai de volta à lista de árvores
        # Insere o novo nó na lista de árvores, mantendo a ordem por frequência
        arvores.append(novo_no) # Insere o novo nó na lista de árvores
        # Reordena a lista de árvores pela frequência
        arvores.sort(key=lambda no: no.frequencia) # Reordena a lista de árvores pela frequência

    raiz = arvores[0] # A raiz da árvore de Huffman é o único nó restante
    # Gera os códigos Huffman para cada caractere
    # A função gerar_codigos percorre a árvore e gera os códigos binários para cada caractere
    # A função retorna um dicionário com os códigos binários para cada caractere
    codigos = {} # Dicionário para armazenar os códigos binários de cada caractere
    # Função recursiva para gerar os códigos Huffman

    def gerar_codigos(no, caminho=""): # Método recursivo que gera os códigos Huffman
        """Gera os códigos Huffman para cada caractere na árvore."""
        if no is not None: # Se o nó não for None, continua a gerar os códigos
            # Se o nó for uma folha, armazena o código do caractere no dicionário
            if no.eh_folha(): # Se o nó for uma folha, armazena o código do caractere no dicionário
                codigos[no.caractere] = caminho # Armazena o código do caractere no dicionário
                # Se o nó não for uma folha, continua a gerar os códigos para os filhos
            gerar_codigos(no.esquerda, caminho + "0") # Chama a função recursiva para o filho esquerdo, adicionando "0" ao caminho
            # Chama a função recursiva para o filho direito, adicionando "1"
            gerar_codigos(no.direita, caminho + "1")

    gerar_codigos(raiz) # Chama a função recursiva para gerar os códigos Huffman a partir da raiz
    texto_codificado = ''.join(codigos[c] for c in texto) # Codifica o texto usando os códigos gerados
    # Retorna o texto codificado e a raiz da árvore de Huffman
    return texto_codificado, raiz


def decodificar_huffman(bits_codificados, arvore_raiz):
    """Decodifica uma sequência de bits usando a árvore de Huffman."""
    mensagem = "" # Inicializa a mensagem decodificada como uma string vazia
    no_atual = arvore_raiz # Começa a decodificação a partir da raiz da árvore de Huffman
    # Percorre cada bit na sequência de bits codificados

    for bit in bits_codificados:
        no_atual = no_atual.esquerda if bit == '0' else no_atual.direita # Move para o filho esquerdo se o bit for '0', ou para o filho direito se for '1'
        if no_atual.eh_folha(): # Se o nó atual for uma folha, significa que um caractere foi encontrado
            mensagem += no_atual.caractere # Adiciona o caractere encontrado à mensagem decodificada
            no_atual = arvore_raiz # Reseta o nó atual para a raiz da árvore para continuar a decodificação

    return mensagem # Retorna a mensagem decodificada completa


def imprimir_arvore(no, prefixo=""): 
    """Gera uma representação textual da árvore de Huffman."""
    if no is None: # Se o nó for None, retorna uma string vazia
        return "" # Se o nó for None, não há nada a imprimir
    if no.eh_folha(): # Se o nó for uma folha, imprime o caractere e sua frequência
        linha = f"{prefixo}📄 '{no.caractere}' ({no.frequencia})\n"
    else: # Se o nó não for uma folha, imprime o nó interno com sua frequência
        linha = f"{prefixo}🌿 [Interno] ({no.frequencia})\n"
    return linha + imprimir_arvore(no.esquerda, prefixo + "  ") + imprimir_arvore(no.direita, prefixo + "  ") # Chama recursivamente para os filhos esquerdo e direito, adicionando espaços ao prefixo para indentação


def imprimir_codigos(no, caminho=""):
    """Gera uma string com os códigos Huffman de cada caractere."""
    if no is None: # Se o nó for None, retorna uma string vazia
        return ""
    if no.eh_folha(): # Se o nó for uma folha, imprime o caractere e seu código
        # Retorna o caractere, o caminho (código) e a frequência do nó
        return f"'{no.caractere}' -> {caminho} (freq: {no.frequencia})\n"
    return imprimir_codigos(no.esquerda, caminho + "0") + imprimir_codigos(no.direita, caminho + "1")


def serializar_arvore(no):
    """Serializa a árvore de Huffman para JSON (como dicionário)."""
    if no is None:
        return None # Se o nó for None, retorna None
    # Retorna um dicionário com o caractere, frequência e os filhos esquerdo e direito
    # A função serializa a árvore de Huffman em um formato que pode ser facilmente convertido
    return {
        'caractere': no.caractere,
        'frequencia': no.frequencia,
        'esquerda': serializar_arvore(no.esquerda),
        'direita': serializar_arvore(no.direita) 
    }


def desserializar_arvore(data):
    """Reconstrói a árvore de Huffman a partir de um dicionário JSON."""
    if data is None: # Se o dado for None, retorna None
        return None
    no = NoHuffman(data['caractere'], data['frequencia']) # Cria um novo nó Huffman com o caractere e frequência do dicionário
    no.esquerda = desserializar_arvore(data['esquerda']) # Chama recursivamente para o filho esquerdo
    # Chama recursivamente para o filho direito
    no.direita = desserializar_arvore(data['direita'])
    return no # Retorna o nó reconstruído da árvore de Huffman
