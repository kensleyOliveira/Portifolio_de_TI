def proximo_primo(n): # Método auxiliar para encontrar o próximo número primo
        """ Encontra o próximo número primo maior ou igual a n """
        def eh_primo(k): # Verifica se um número é primo
            if k < 2: # Números menores que 2 não são primos
                return False
            for i in range(2, int(k**0.5) + 1):#    Verifica se k é divisível por algum número entre 2 e a raiz quadrada de k
                if k % i == 0: # Se for divisível, não é primo
                    return False
            return True

        while not eh_primo(n): #   Continua incrementando n até encontrar um número primo
            n += 1
        return n