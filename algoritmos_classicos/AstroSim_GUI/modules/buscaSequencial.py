class PesquisaSequencial:
    """
    Uma classe para realizar a pesquisa sequencial em uma lista.
    """
    # Método construtor
    def __init__(self, lista: list):
        self._lista = lista # A lista pode conter elementos numércios ou strings
        
    # Método para buscar um item na lista
    # A função enumerate dá acesso ao índice e ao valor do item
    def __call__(self, item):
        """Permite que a instância da classe seja chamada como uma função

        Args:
            item (_type_): O item a ser procurado na lista.
        """
        return self.buscar(self._lista, item)
    
    def buscar_parcial(self, termo):
        """
        Busca a primeira ocorrência do valor alvo na lista.

        Args:
            termo (str): O valor a ser procurado (parcial).

        Returns:
            dict: Contém posição encontrada e número de verificações.
        """
        termo = termo.lower() # Converte o termo para minúsculas para evitar problemas de case sensitivity
        verificacoes = 0 
        for i, item in enumerate(self._lista): # Percorre a lista e verifica cada item
            verificacoes += 1
            if termo in item.lower(): # Verifica se o termo está contido no item (case insensitive)
                return {
                    "posicao": i, # Índice do item encontrado
                    "verificacoes": verificacoes # Número de verificações feitas
                }

        return {
            "posicao": None, # Se não encontrado, retorna None
            "verificacoes": verificacoes # Número de verificações feitas
        }
