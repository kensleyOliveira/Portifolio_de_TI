import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json
from modules import compressaoHuffman as huff


class DataTransmissionGUI(ttk.Frame): # Classe principal para a GUI de transmissão de dados
    """Classe que representa a interface gráfica para transmissão de dados com compressão Huffman.
    Esta classe herda de ttk.Frame e contém todos os componentes necessários para a compressão e descompressão de dados usando o algoritmo de Huffman.
    A interface inclui campos para entrada de texto, exibição de códigos gerados, árvore Huffman e botões para compressão, descompressão e manipulação de arquivos.
    Args:
        parent (tk.Tk): A janela principal onde a GUI será exibida.
    """
    def __init__(self, parent): # Método construtor da classe
        super().__init__(parent, padding=10) # Inicializa o frame com padding
        self.pack(fill=tk.BOTH, expand=True) # Preenche o espaço disponível na janela

        self.arvore_raiz = None # Variável para armazenar a raiz da árvore de Huffman

        # Título
        ttk.Label(self, text="Transmissão de Dados - Compressão Huffman",
                  font=("Segoe UI", 16, "bold")).pack(pady=(5, 15)) # Adiciona um título à GUI com fonte personalizada

        # Notebook com abas
        notebook = ttk.Notebook(self) # Cria um notebook para organizar as abas
        notebook.pack(fill=tk.BOTH, expand=True, padx=5) # Adiciona o notebook à GUI

        self._criar_abas(notebook) # Cria as abas do notebook
        self._criar_botoes_principais() # Cria os botões principais para compressão e descompressão
        self._criar_botoes_arquivos() # Cria os botões para manipulação de arquivos

    # === ABAS ===
    def _criar_abas(self, notebook): # Método para criar as abas do notebook
        self._criar_aba_mensagem(notebook) # Cria a aba para mensagem original e comprimida
        self._criar_aba_codigos(notebook) # Cria a aba para exibir os códigos gerados
        self._criar_aba_arvore(notebook) # Cria a aba para exibir a árvore de Huffman
        self._criar_aba_entrada_manual(notebook) # Cria a aba para entrada manual de códigos Huffman

    def _criar_aba_mensagem(self, notebook): # Método para criar a aba de mensagem
        aba = ttk.Frame(notebook) # Cria uma nova aba no notebook
        notebook.add(aba, text="Mensagem") # Adiciona a aba ao notebook com o título "Mensagem"

        self._criar_rotulo("Mensagem a ser comprimida:", aba) # Cria um rótulo para a mensagem original
        self.texto_original = self._criar_textbox(aba, height=4) # Cria uma caixa de texto para a mensagem original

        self._criar_rotulo("Texto comprimido (binário):", aba) # Cria um rótulo para o texto comprimido
        self.texto_comprimido = self._criar_textbox(aba, height=4) # Cria uma caixa de texto para o texto comprimido

        self._criar_rotulo("Texto descomprimido:", aba) # Cria um rótulo para o texto descomprimido
        self.texto_descomprimido = ttk.Label(aba, text="", wraplength=740, 
                                             font=("Segoe UI", 10), bootstyle="light") # Cria um rótulo para exibir o texto descomprimido
        self.texto_descomprimido.pack(pady=(0, 10), anchor='w', padx=5) # Adiciona o rótulo à aba com padding e alinhamento

    def _criar_aba_codigos(self, notebook): # Método para criar a aba de códigos gerados
        """Cria a aba para exibir os códigos gerados pelo algoritmo de Huffman."""
        aba = ttk.Frame(notebook) 
        notebook.add(aba, text="Códigos Gerados")

        self._criar_rotulo("Códigos Huffman:", aba)
        self.codigos_texto = self._criar_textbox(aba, height=10)

    def _criar_aba_arvore(self, notebook): # Método para criar a aba da árvore de Huffman
        """Cria a aba para exibir a árvore de Huffman."""
        
        # Criar o frame da aba
        aba = ttk.Frame(notebook)
        
        notebook.add(aba, text="Árvore Huffman")

        self._criar_rotulo("Árvore de Huffman:", aba)
        self.arvore_texto = self._criar_textbox(aba, height=14)

    def _criar_aba_entrada_manual(self, notebook): # Método para criar a aba de entrada manual de códigos
        """Cria a aba para entrada manual de códigos Huffman."""
        aba = ttk.Frame(notebook)
        notebook.add(aba, text="Entrada Manual")

        self._criar_rotulo("Inserir códigos Huffman manualmente (ex: 'a' -> 01):", aba)
        self.codigos_personalizados = self._criar_textbox(aba, height=10)

    # === COMPONENTES ===
    def _criar_rotulo(self, texto, parent): # Método auxiliar para criar rótulos
        """Cria um rótulo com o texto especificado."""
        ttk.Label(parent, text=texto, font=("Segoe UI", 10)).pack(anchor='w', pady=(10, 2), padx=5)

    def _criar_textbox(self, parent, height): # Método auxiliar para criar caixas de texto
        """Cria uma caixa de texto com rolagem e configurações específicas."""
        caixa = ScrolledText(parent, height=height, width=90,
                             font=("Consolas", 10), wrap='none')
        caixa.pack(pady=(0, 10), padx=5, fill=tk.BOTH, expand=True)
        return caixa

    def _atualizar_textbox(self, caixa, texto): # Método auxiliar para atualizar o conteúdo de uma caixa de texto
        """Atualiza o conteúdo de uma caixa de texto com o texto fornecido."""
        caixa.delete("1.0", tk.END)
        caixa.insert("1.0", texto)

    # === BOTÕES ===
    def _criar_botoes_principais(self): # Método para criar os botões principais de compressão e descompressão
        """Cria os botões principais para compressão e descompressão de dados."""
        frame = ttk.Frame(self)
        frame.pack(pady=10)
        ttk.Button(frame, text="Comprimir", bootstyle="success", command=self.comprimir).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame, text="Descomprimir", bootstyle="info", command=self.descomprimir).pack(side=tk.LEFT, padx=10)

    def _criar_botoes_arquivos(self): # Método para criar os botões de manipulação de arquivos
        """Cria os botões para carregar códigos de arquivo, salvar códigos gerados e salvar árvore Huffman."""
        frame = ttk.Frame(self)
        frame.pack(pady=5)

        ttk.Button(frame, text="📂 Carregar Códigos de Arquivo", command=self.carregar_codigos_de_arquivo).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame, text="💾 Salvar Códigos Gerados", command=self.salvar_codigos_gerados).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame, text="💾 Salvar Árvore Huffman", command=self.salvar_arvore_huffman).pack(side=tk.LEFT, padx=10)

    # === FUNÇÕES PRINCIPAIS ===
    def comprimir(self): # Método para comprimir o texto usando o algoritmo de Huffman
        """Comprime o texto inserido na caixa de texto original usando o algoritmo de Huffman."""
        texto = self.texto_original.get("1.0", tk.END).strip()
        if not texto: # Verifica se o texto está vazio
            self._atualizar_textbox(self.texto_comprimido, "[Erro] Mensagem vazia.")
            return

        binario, self.arvore_raiz = huff.codificar_huffman(texto) # Codifica o texto usando o algoritmo de Huffman

        self._atualizar_textbox(self.texto_comprimido, binario) # Atualiza a caixa de texto comprimido com o binário gerado
        self._atualizar_textbox(self.codigos_texto, huff.imprimir_codigos(self.arvore_raiz)) # Atualiza a caixa de texto com os códigos gerados
        self._atualizar_textbox(self.arvore_texto, huff.imprimir_arvore(self.arvore_raiz)) # Atualiza a caixa de texto com a representação da árvore de Huffman
        self.texto_descomprimido.config(text="") # Limpa o rótulo de texto descomprimido

    def descomprimir(self): # Método para descomprimir o texto usando a árvore de Huffman
        """Descomprime o texto binário inserido na caixa de texto comprimido usando a árvore de Huffman."""
        binario = self.texto_comprimido.get("1.0", tk.END).strip() # Verifica se o texto comprimido está vazio
        if not binario: # Se o texto comprimido estiver vazio, exibe um erro
            self.texto_descomprimido.config(text="[Erro] Nenhum dado para descomprimir.")
            return

        arvore = self.arvore_raiz or self._reconstruir_arvore_dos_codigos(self._ler_codigos_personalizados()) # Reconstrói a árvore de Huffman a partir dos códigos personalizados, se a árvore raiz não estiver definida

        if arvore is None: # Se a árvore não puder ser reconstruída, exibe um erro
            self.texto_descomprimido.config(text="[Erro] Nenhuma árvore ou código válido disponível.")
            return

        try: # Tenta descomprimir o texto binário usando a árvore de Huffman
            texto = huff.decodificar_huffman(binario, arvore) # Descomprime o texto binário usando a árvore de Huffman
            self.texto_descomprimido.config(text=texto) # Atualiza o rótulo de texto descomprimido com o texto resultante
        except Exception as e: # Se ocorrer um erro durante a descompressão, exibe uma mensagem de erro
            self.texto_descomprimido.config(text=f"[Erro ao decodificar]: {e}")

    # === MANIPULAÇÃO DE CÓDIGOS ===
    def _ler_codigos_personalizados(self): # Método para ler os códigos personalizados inseridos pelo usuário
        texto = self.codigos_personalizados.get("1.0", tk.END).strip() # Obtém o texto inserido na caixa de códigos personalizados
        codigos = {} # Dicionário para armazenar os códigos personalizados
        for linha in texto.splitlines(): # Percorre cada linha do texto inserido
            if '->' in linha: # Verifica se a linha contém o separador '->'
                try: # Tenta dividir a linha em caractere e código
                    caractere, codigo = linha.strip().split('->') # Divide a linha em caractere e código
                    caractere = caractere.strip().strip("'").strip('"') # Remove espaços e aspas do caractere
                    codigos[caractere] = codigo.strip() # Adiciona o código ao dicionário de códigos
                except Exception: # Se ocorrer um erro ao dividir a linha, ignora a linha
                    continue # Ignora linhas inválidas
        return codigos # Retorna o dicionário de códigos personalizados

    def _reconstruir_arvore_dos_codigos(self, codigos_dict): # Método para reconstruir a árvore de Huffman a partir dos códigos personalizados
        if not codigos_dict: # Se o dicionário de códigos estiver vazio, retorna None
            return None # Se não houver códigos personalizados, não há árvore para reconstruir
        raiz = huff.NoHuffman() # Cria a raiz da árvore de Huffman
        for caractere, codigo in codigos_dict.items(): # Percorre cada caractere e seu código no dicionário de códigos personalizados
            no = raiz # Começa na raiz da árvore
            for bit in codigo: # Percorre cada bit do código
                if bit == '0': # Se o bit for '0', move para o filho esquerdo
                    if not no.esquerda: # Se não houver filho esquerdo, cria um novo nó
                        no.esquerda = huff.NoHuffman() # Cria um novo nó para o filho esquerdo
                    no = no.esquerda # Move para o filho esquerdo
                elif bit == '1': # Se o bit for '1', move para o filho direito
                    if not no.direita: # Se não houver filho direito, cria um novo nó
                        no.direita = huff.NoHuffman() # Cria um novo nó para o filho direito
                    no = no.direita # Move para o filho direito
            no.caractere = caractere # Define o caractere no nó atual como o caractere correspondente ao código
        return raiz # Retorna a raiz da árvore de Huffman reconstruída a partir dos códigos personalizados

    # === ARQUIVOS ===
    def carregar_codigos_de_arquivo(self): # Método para carregar códigos Huffman de um arquivo
        caminho = filedialog.askopenfilename( 
            title="Selecionar arquivo de códigos",
            filetypes=[("Arquivos de texto", "*.txt"), ("Arquivos JSON", "*.json")]
        ) # Abre um diálogo para selecionar o arquivo de códigos Huffman
        if not caminho: # Se nenhum arquivo for selecionado, não faz nada
            return

        try: # Tenta ler o arquivo selecionado
            with open(caminho, 'r', encoding='utf-8') as f: # Abre o arquivo para leitura
                if caminho.endswith('.json'): # Se o arquivo for JSON, carrega os códigos como um dicionário
                    codigos_dict = json.load(f) # Converte o JSON em um dicionário
                    texto = '\n'.join(f"'{k}' -> {v}" for k, v in codigos_dict.items()) # Formata o dicionário em uma string para exibição
                else: # Se o arquivo for de texto, lê o conteúdo diretamente
                    texto = f.read() # Lê o conteúdo do arquivo de texto
            self._atualizar_textbox(self.codigos_personalizados, texto) # Atualiza a caixa de texto com os códigos lidos do arquivo
            messagebox.showinfo("Códigos carregados", "Códigos Huffman carregados com sucesso.") # Exibe uma mensagem de sucesso após carregar os códigos
        except Exception as e: # Se ocorrer um erro ao ler o arquivo, exibe uma mensagem de erro
            messagebox.showerror("Erro ao carregar", f"Erro ao ler arquivo: {e}") # Exibe uma mensagem de erro se não for possível ler o arquivo

    def salvar_codigos_gerados(self): # Método para salvar os códigos gerados em um arquivo
        texto = self.codigos_texto.get("1.0", tk.END).strip() # Obtém o texto dos códigos gerados
        if not texto: # Se não houver códigos gerados, exibe um aviso
            messagebox.showwarning("Aviso", "Nenhum código gerado para salvar.") # Se não houver códigos gerados, não há nada para salvar
            return # Se não houver códigos gerados, não há nada para salvar

        caminho = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivo texto", "*.txt")],
            title="Salvar códigos Huffman"
        ) # Abre um diálogo para salvar os códigos gerados
        if caminho: # Se um caminho for selecionado, salva os códigos no arquivo
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(texto) # Escreve os códigos gerados no arquivo selecionado
            # Exibe uma mensagem de sucesso após salvar os códigos
            messagebox.showinfo("Sucesso", f"Códigos salvos em:\n{caminho}")

    def salvar_arvore_huffman(self): # Método para salvar a árvore de Huffman em um arquivo
        texto = self.arvore_texto.get("1.0", tk.END).strip() # Obtém o texto da árvore de Huffman
        if not texto: # Se não houver árvore gerada, exibe um aviso
            # Se não houver árvore gerada, não há nada para salvar
            messagebox.showwarning("Aviso", "Nenhuma árvore de Huffman gerada para salvar.")
            return # Se não houver árvore gerada, não há nada para salvar

        caminho = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivo texto", "*.txt")],
            title="Salvar árvore de Huffman"
        ) # Abre um diálogo para salvar a árvore de Huffman
        # Se um caminho for selecionado, salva a árvore no arquivo
        if caminho:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(texto) # Escreve a árvore de Huffman no arquivo selecionado
            # Exibe uma mensagem de sucesso após salvar a árvore
            messagebox.showinfo("Sucesso", f"Árvore salva em:\n{caminho}")
