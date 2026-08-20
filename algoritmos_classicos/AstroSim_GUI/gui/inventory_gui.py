
import ttkbootstrap as tb
from ttkbootstrap.constants import LEFT, END  # Add other constants as needed
from tkinter import messagebox
import tkinter as tk
import time
import sys
import os


# Módulos
from modules.inventory_manager import InventoryManager, Component
from modules.buscaSequencial import PesquisaSequencial
from modules.pesquisaBinariaIterativa import BuscaBinariaIterativa
from modules.text_search_windows import TextSearchWindow
from modules.hashing import Hashing
from modules.utils import proximo_primo

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Adiciona o caminho do diretório pai ao sys.path para importar módulos corretamente

class InventoryGUI(tb.Frame): # Classe principal da GUI do inventário
    """Classe para a interface gráfica do inventário de componentes AstroSim.
    Esta classe herda de ttkbootstrap.Frame e é responsável por gerenciar a interface do usuário, permitindo adicionar, buscar e visualizar componentes do inventário.
    A interface inclui campos para adicionar novos componentes, realizar buscas sequenciais, binárias e por hash, além de uma janela para busca de texto nos logs.
    Args:
        parent (tk.Tk): A janela principal onde o inventário será exibido.
    """
    def __init__(self, parent): # Método construtor da classe InventoryGUI
        """Inicializa a interface gráfica do inventário de componentes AstroSim."""
        
        super().__init__(parent) # Chama o construtor da classe pai (ttkbootstrap.Frame)
        self.pack(fill="both", expand=True) # Define o preenchimento e expansão do frame
        self.inventory = InventoryManager() # Inicializa o gerenciador de inventário

        tb.Label(self, text="Inventário de Componentes AstroSim", font=("Arial", 16, "bold")).pack(pady=10) # Título da janela

        add_frame = tb.LabelFrame(self, text="Adicionar Novo Componente") # Frame para adicionar novos componentes
        add_frame.pack(pady=10, padx=10, fill="x") # Cria um frame para adicionar novos componentes

        self.fields = {} # Dicionário para armazenar os campos de entrada dos componentes
        labels = ["Código:", "Nome:", "Categoria:", "Massa:", "Consumo:"] # Lista de rótulos para os campos de entrada
        for i, label in enumerate(labels): # Cria os campos de entrada para cada rótulo
            tb.Label(add_frame, text=label).grid(row=i, column=0, padx=5, pady=2, sticky="w") # Rótulo do campo de entrada
            entry = tb.Entry(add_frame) # Campo de entrada para o valor do componente
            entry.grid(row=i, column=1, padx=5, pady=2, sticky="ew") # Adiciona o campo de entrada ao grid
            self.fields[label] = entry # Armazena o campo de entrada no dicionário fields

        tb.Button(add_frame, text="Adicionar Componente", bootstyle="info", command=self.add_component).grid(row=5, column=0, columnspan=2, pady=5) # Botão para adicionar o componente ao inventário

        search_frame = tb.LabelFrame(self, text="Buscar Componente") # Frame para buscar componentes
        search_frame.pack(pady=10, padx=10, fill="x") # Cria um frame para buscar componentes

        tb.Label(search_frame, text="Buscar por:").grid(row=0, column=0, padx=5, pady=5, sticky="w") # Rótulo para o tipo de busca
        self.search_type = tb.Combobox(search_frame, values=["Código", "Nome", "Categoria", "Massa", "Consumo"], state="readonly") # Combobox para selecionar o tipo de busca
        self.search_type.set("Código") # Define o tipo de busca padrão como "Código"
        self.search_type.grid(row=0, column=1, padx=5, pady=5) # Adiciona o combobox ao grid

        tb.Label(search_frame, text="Expressão (Ex: >= 100):").grid(row=1, column=0, padx=5, pady=5, sticky="w") # Rótulo para o campo de entrada da expressão de busca
        self.search_entry = tb.Entry(search_frame) # Campo de entrada para a expressão de busca
        self.search_entry.grid(row=1, column=1, padx=5, pady=5) # Adiciona o campo de entrada ao grid

        tb.Label(search_frame, text="Função Hash:").grid(row=2, column=0, padx=5, pady=5, sticky="w") # Rótulo para o tipo de função hash
        self.hash_type_combobox = tb.Combobox(search_frame, values=["DIVISAO", "MULTIPLICACAO", "MEIO_QUADRADO", "RAIZ", "EXTRACAO", "XOR", "ROTACAO", "PESO"], state="readonly") # Combobox para selecionar o tipo de função hash
        self.hash_type_combobox.set("PESO") # Define o tipo de função hash padrão como "PESO"
        self.hash_type_combobox.grid(row=2, column=1, padx=5, pady=5) # Adiciona o combobox ao grid

        button_frame = tb.Frame(search_frame) # Frame para os botões de busca
        button_frame.grid(row=3, column=0, columnspan=2) # Cria um frame para os botões de busca
        tb.Button(button_frame, text="Busca Sequencial", bootstyle="primary", command=self.perform_sequential_search).pack(side=tk.LEFT, padx=5) # Botão para realizar a busca sequencial
        tb.Button(button_frame, text="Busca Binária", bootstyle="primary", command=self.perform_binary_search).pack(side=tk.LEFT, padx=5) # Botão para realizar a busca binária
        tb.Button(button_frame, text="Busca Hash", bootstyle="warning", command=self.perform_hash_search).pack(side=tk.LEFT, padx=5) # Botão para realizar a busca por hash
        tb.Button(button_frame, text="Busca Texto (Rabin-Karp)", bootstyle="success", command=self.open_text_search_window).pack(side=tk.LEFT, padx=5) # Botão para abrir a janela de busca de texto usando o algoritmo Rabin-Karp
        tb.Button(button_frame, text="Limpar Pesquisa", bootstyle="danger", command=self.clear_search_results).pack(side=tk.LEFT, padx=5) # Botão para limpar os resultados da pesquisa
        tb.Button(button_frame, text="Ver Todos os Logs", bootstyle="info", command=self.exibir_todos_logs).pack(side=tk.LEFT, padx=5) # Botão para exibir todos os logs do inventário

        self.search_result_label = tb.Label(self, text="", wraplength=500, justify=tk.LEFT) # Rótulo para exibir os resultados da pesquisa
        self.search_result_label.pack(pady=10, padx=10, fill="x") # Adiciona o rótulo de resultados da pesquisa ao frame

        tree_frame = tb.Frame(self) # Frame para a árvore de componentes
        tree_frame.pack(padx=10, pady=5, fill="both", expand=True) # Cria um frame para a árvore de componentes

        tree_scroll = tb.Scrollbar(tree_frame, orient="vertical") # Barra de rolagem vertical para a árvore de componentes
        tree_scroll.pack(side="right", fill="y") # Adiciona a barra de rolagem ao frame

        self.tree = tb.Treeview(tree_frame, columns=("cod", "nome", "categoria", "massa", "consumo"), show="headings", height=12, yscrollcommand=tree_scroll.set) # Cria a árvore de componentes com colunas para código, nome, categoria, massa e consumo
        self.tree.pack(side="left", fill="both", expand=True) # Adiciona a árvore de componentes ao frame
        tree_scroll.config(command=self.tree.yview) # Configura a barra de rolagem para controlar a visualização da árvore

        for col in ("cod", "nome", "categoria", "massa", "consumo"): #  Define os cabeçalhos e colunas da árvore de componentes
            self.tree.heading(col, text=col.capitalize()) # Define o cabeçalho da coluna
            self.tree.column(col, anchor="center") # Alinha o conteúdo da coluna ao centro

        self.tree.bind("<ButtonRelease-1>", self.on_tree_click) # Evento de clique na árvore de componentes
        self._update_component_list() # Atualiza a lista de componentes exibidos na árvore

        self.historico_buscas = [] # Lista para armazenar o histórico de buscas realizadas
        tb.Button(button_frame, text="Histórico de Busca", bootstyle="secondary", command=self.abrir_historico_buscas).pack(side=tk.LEFT, padx=5) # Botão para abrir o histórico de buscas realizadas
        
    def open_text_search_window(self): # Método para abrir a janela de busca de texto
        TextSearchWindow(self, self.inventory) # Abre a janela de busca de texto com o inventário atual

    def add_component(self): # Método para adicionar um novo componente ao inventário
        """Adiciona um novo componente ao inventário com base nos campos de entrada."""
        try:
            cod = self.fields["Código:"].get().strip() # Obtém o código do componente
            nome = self.fields["Nome:"].get().strip() # Obtém o nome do componente
            categoria = self.fields["Categoria:"].get().strip() # Obtém a categoria do componente
            massa = int(self.fields["Massa:"].get().strip()) # Obtém a massa do componente
            consumo = float(self.fields["Consumo:"].get().strip()) # Obtém o consumo do componente

            if not cod or not nome or not categoria: # Verifica se todos os campos obrigatórios foram preenchidos
                raise ValueError("Todos os campos de texto devem ser preenchidos.") # Lança um erro se algum campo obrigatório estiver vazio
            comp = Component(cod, nome, categoria, massa, consumo) # Cria uma instância do componente com os valores fornecidos
            self.inventory.add_component(comp) # Adiciona o componente ao inventário

            messagebox.showinfo("Sucesso", f"Componente '{nome}' adicionado ao banco de dados.") # Exibe uma mensagem de sucesso ao adicionar o componente
            for field in self.fields.values(): # Limpa os campos de entrada após adicionar o componente
                field.delete(0, tk.END) # Limpa o campo de entrada

            self._update_component_list() # Atualiza a lista de componentes exibidos na árvore
        except Exception as e: # Trata exceções ao adicionar o componente
            messagebox.showerror("Erro", f"Erro ao adicionar componente: {e}") # Exibe uma mensagem de erro se ocorrer algum problema ao adicionar o componente

    def _update_component_list(self): # Método para atualizar a lista de componentes exibidos na árvore
        """Atualiza a lista de componentes exibidos na árvore."""
        self.tree.delete(*self.tree.get_children()) # Limpa a árvore de componentes antes de atualizar
        self.all_components = self.inventory.get_all_components() # Obtém todos os componentes do inventário
        for comp in self.all_components: # Percorre todos os componentes e adiciona-os à árvore
            self.tree.insert("", tk.END, values=(comp.cod_invent, comp.nome, comp.categoria, f"{comp.massa} g", f"{comp.consumo} W")) # 

    def clear_search_results(self): # Método para limpar os resultados da pesquisa
        self.search_entry.delete(0, tk.END) # Limpa o campo de entrada da pesquisa
        self.search_result_label.config(text="") # Limpa o rótulo de resultados da pesquisa
        self._update_component_list() # Atualiza a lista de componentes exibidos na árvore

    def perform_sequential_search(self): # Método de busca sequencial
        """ Realiza a busca sequencial com base no tipo e valor informados 
        """
        valor = self.search_entry.get().strip().lower() # Obtém o valor da entrada de pesquisa
        tipo = self.search_type.get() # Obtém o tipo de pesquisa selecionado
        todos = self.inventory.get_all_components() # Obtém todos os componentes do inventário
        componentes_filtrados = [] # Lista para armazenar os componentes filtrados
        comparacoes = 0 # Contador de comparações

        inicio = time.time() # Marca o tempo de início da busca

        if tipo in ["Código", "Nome", "Categoria"]: # Se o tipo for Código, Nome ou Categoria
            mapa_atributos = { # Mapeia os tipos de pesquisa para os atributos dos componentes
                "Código": "cod_invent",
                "Nome": "nome",
                "Categoria": "categoria"
            }
            atributo = mapa_atributos.get(tipo) # Obtém o atributo correspondente ao tipo de pesquisa

            lista_busca = [getattr(comp, atributo).lower() for comp in todos] # Cria uma lista com os valores do atributo selecionado
            ps = PesquisaSequencial(lista_busca) # Cria uma instância da pesquisa sequencial
            resultado = ps.buscar_parcial(valor) # Realiza a busca parcial
            comparacoes = resultado["verificacoes"] # Conta o número de verificações realizadas
            if resultado["posicao"] is not None: # Se encontrou uma posição válida
                componentes_filtrados.append(todos[resultado["posicao"]]) # Adiciona o componente correspondente à lista filtrada

        elif tipo in ["Massa", "Consumo"]: # Se o tipo for Massa ou Consumo
            try:
                operador, num = self._parse_expressao(valor) # Tenta analisar a expressão de busca
                for comp in todos: # Percorre todos os componentes
                    comparacoes += 1 # Incrementa o contador de comparações
                    valor_comp = comp.massa if tipo == "Massa" else comp.consumo # Obtém o valor do componente correspondente ao tipo de pesquisa
                    if self._avaliar_comparacao(valor_comp, operador, num): #   Verifica se o valor do componente atende à condição da expressão
                        componentes_filtrados.append(comp) #    Adiciona o componente à lista filtrada 
            except: # Se ocorrer um erro ao analisar a expressão
                messagebox.showerror("Erro de Expressão", "Use uma expressão válida como: >= 200") # Exibe uma mensagem de erro
                return

        fim = time.time() # Marca o tempo de fim da busca
        # Calcula o tempo de execução em milissegundos
        tempo = (fim - inicio) * 1000 

        msg = (
            f"⭐ Ocorrências encontradas: {len(componentes_filtrados)}\n"
            if componentes_filtrados else
            "❌ Nenhuma ocorrência encontrada.\n"
        )
        msg += f"⚖ Comparações: {comparacoes} | ⏱ Tempo: {tempo:.2f} ms"
        self.search_result_label.config(text=msg)

        self.tree.delete(*self.tree.get_children()) # Limpa a árvore de resultados antes de exibir os componentes filtrados
        for comp in componentes_filtrados: # Percorre os componentes filtrados e os adiciona à árvore de resultados
            self.tree.insert("", tk.END, values=(comp.cod_invent, comp.nome, comp.categoria, f"{comp.massa} g", f"{comp.consumo} W")) # Insere o componente na árvore de resultados

        # Salva no histórico de busca
        self.historico_buscas.append((
            "Sequencial",
            valor,
            comparacoes,
            f"{tempo:.2f} ms"
        ))

    def perform_binary_search(self): # Método de busca binária
        """ Realiza a busca binária com base no tipo e valor informados
        """     
        valor = self.search_entry.get().strip().lower()# Obtém o valor da entrada de pesquisa
        tipo = self.search_type.get() # Obtém o tipo de pesquisa selecionado
        todos = self.inventory.get_all_components() # Obtém todos os componentes do inventário

        if tipo not in ["Código", "Nome", "Categoria"]: # Verifica se o tipo é válido para busca binária 
            messagebox.showwarning("Aviso", "Busca binária só suporta campos de texto com igualdade completa.")
            return

        mapa_atributos = { # Mapeia os tipos de pesquisa para os atributos dos componentes
            "Código": "cod_invent",
            "Nome": "nome",
            "Categoria": "categoria"
        }

        atributo = mapa_atributos.get(tipo) # Obtém o atributo correspondente ao tipo de pesquisa
        if not atributo:
            messagebox.showerror("Erro", "Atributo inválido para busca binária.")
            return

        key_func = lambda c: getattr(c, atributo).lower() # Cria uma função de chave para acessar o atributo do componente
        lista_ordenada = sorted(todos, key=key_func) # Ordena a lista de componentes com base no atributo selecionado

        bb = BuscaBinariaIterativa(lista_ordenada, key=key_func) # Cria uma instância da busca binária iterativa com a lista ordenada e a função de chave
        inicio = time.time() # Marca o tempo de início da busca
        index = bb.buscar(valor) # Realiza a busca binária pelo valor informado
        fim = time.time() # Marca o tempo de fim da busca

        tempo = (fim - inicio) * 1000 # Converte o tempo de execução para milissegundos
        comparacoes = bb.comparacoes # Conta o número de comparações realizadas na busca

        self.tree.delete(*self.tree.get_children()) # Limpa a árvore de resultados

        if index is not None: # Se encontrou um índice válido
            comp = lista_ordenada[index] # Obtém o componente correspondente ao índice encontrado
            self.tree.insert("", tk.END, values=(comp.cod_invent, comp.nome, comp.categoria, f"{comp.massa} g", f"{comp.consumo} W")) # Insere o componente na árvore de resultados
            msg = f"🔍 Resultado Binário: 1 ocorrência encontrada\n"
        else:
            msg = "❌ Nenhuma ocorrência encontrada.\n"

        msg += f"⚖ Comparações: {comparacoes} | ⏱ Tempo: {tempo:.2f} ms"
        self.search_result_label.config(text=msg)
        
        # Salva no histórico de busca
        self.historico_buscas.append((
            "Binária",
            valor,
            comparacoes,
            f"{tempo:.2f} ms"
        ))

    # Método de conversão de string para inteiro
    # Usado para calcular o hash de strings 
    def string_para_int(self, s): # Método auxiliar para converter uma string em um inteiro
        """Converte uma string em um inteiro baseado no valor de cada caractere."""
        return sum(ord(c) * (i + 1) for i, c in enumerate(str(s)))
    
    # Método busca hash
    def perform_hash_search(self): # Método de busca hash
        """ Realiza a busca hash com base no tipo e valor informados
        """
        valor = self.search_entry.get().strip().lower() # Obtém o valor da entrada de pesquisa
        tipo = self.search_type.get() # Obtém o tipo de pesquisa selecionado
        tipo_hash = self.hash_type_combobox.get().lower() # Obtém o tipo de hash selecionado

        todos = self.inventory.get_all_components() # Obtém todos os componentes do inventário
        mapa_atributos = {# Mapeia os tipos de pesquisa para os atributos dos componentes
            "Código": "cod_invent",
            "Nome": "nome",
            "Categoria": "categoria"
        }

        if tipo not in mapa_atributos: # Verifica se o tipo é válido para busca hash
            messagebox.showwarning("Aviso", "Busca Hash só suporta campos de texto.")
            return

        atributo = mapa_atributos[tipo] # Obtém o atributo correspondente ao tipo de pesquisa
        tamanho_dinamico = proximo_primo(len(todos) * 2) # Método auxiliar para encontrar o próximo número primo
        hash_table = Hashing(tamanho=tamanho_dinamico, metodo_colisao="encadeamento", tipo_hash=tipo_hash) # Cria uma instância da tabela hash com o tamanho dinâmico e o método de colisão especificado

        for comp in todos: # Preenche a tabela hash com os componentes
            chave = getattr(comp, atributo).lower() # Obtém o valor do atributo correspondente ao tipo de pesquisa
            hash_table.inserir(chave, comp) # Insere o componente na tabela hash com a chave correspondente

        inicio = time.time() # Marca o tempo de início da busca
        resultado = hash_table.buscar(valor) # Realiza a busca na tabela hash pelo valor informado
        fim = time.time() # Marca o tempo de fim da busca

        tempo = (fim - inicio) * 1000 # Converte o tempo de execução para milissegundos

        self.tree.delete(*self.tree.get_children()) # Limpa a árvore de resultados
        if resultado: # Se encontrou um resultado válido
            self.tree.insert("", tk.END, values=( # Insere o componente encontrado na árvore de resultados
                resultado.cod_invent, resultado.nome, resultado.categoria,
                f"{resultado.massa} g", f"{resultado.consumo} W"
            ))
            msg = f"🔍 Resultado Hash: 1 ocorrência encontrada\n"
        else:
            msg = "❌ Nenhuma ocorrência encontrada.\n"

        msg += f"⏱ Tempo: {tempo:.2f} ms"
        self.search_result_label.config(text=msg) # Atualiza o rótulo de resultados da pesquisa

        # Salva no histórico de busca
        self.historico_buscas.append((
            "Hash",
            valor,
            "--",  # Comparações não rastreadas em hash por padrão
            f"{tempo:.2f} ms"
        ))
       
    # Método Histórico de Buscas
    def abrir_historico_buscas(self): # Método para abrir a janela de histórico de buscas
        """Abre uma janela para exibir o histórico de buscas realizadas."""
        janela = tk.Toplevel(self) # Cria uma nova janela para o histórico de buscas
        janela.title("Histórico de Buscas") # Define o título da janela
        janela.geometry("700x300") # Define o tamanho da janela

        frame = tb.Frame(janela) # Cria um frame para o conteúdo da janela
        frame.pack(fill="both", expand=True, padx=10, pady=10) # Adiciona o frame à janela

        tree = tb.Treeview(frame, columns=("tipo", "termo", "comparacoes", "tempo"), show="headings") # Cria uma árvore para exibir o histórico de buscas
        tree.pack(fill="both", expand=True) # Adiciona a árvore ao frame

        for col, title in zip(("tipo", "termo", "comparacoes", "tempo"),
                      ("Pesquisa", "Termo", "Comparações", "Tempo")): # Define os cabeçalhos e colunas da árvore
            tree.heading(col, text=title) # Define o cabeçalho da coluna
            tree.column(col, anchor="center") # Alinha o conteúdo da coluna ao centro

        for tipo, termo, comparacoes, tempo in self.historico_buscas: # Percorre o histórico de buscas e insere os dados na árvore
            # Insere cada busca no histórico na árvore
            tree.insert("", "end", values=(tipo, termo, comparacoes, tempo))

        btn_fechar = tb.Button(janela, text="Fechar", command=janela.destroy, bootstyle="secondary") # Botão para fechar a janela de histórico de buscas
        btn_fechar.pack(pady=10) # Adiciona o botão de fechar à janela

    def _parse_expressao(self, texto): # Método auxiliar para analisar a expressão de busca
        """Analisa uma expressão de busca e retorna o operador e o número."""
        import re # Importa o módulo re para expressões regulares
        match = re.match(r"(>=|<=|>|<|=)\s*(\d+(\.\d+)?)", texto) # Expressão regular para capturar o operador e o número
        if not match: # Se a expressão não corresponder ao padrão esperado
            raise ValueError("Expressão inválida") # Lança um erro se a expressão for inválida
        # Extrai o operador e o número da expressão
        op, num, _ = match.groups()
        return op, float(num)

    def _avaliar_comparacao(self, valor, operador, alvo): # Método auxiliar para avaliar a comparação
        """Avalia uma comparação entre um valor e um alvo com base no operador."""
        return {
            ">": valor > alvo,
            "<": valor < alvo,
            ">=": valor >= alvo,
            "<=": valor <= alvo,
            "=": valor == alvo
        }.get(operador, False)

    def exibir_todos_logs(self): # Método para exibir todos os logs do inventário
        """Exibe todos os logs do inventário em uma árvore."""
        todos_logs = self.inventory.get_all_logs() # Obtém todos os logs do inventário
        self.tree.delete(*self.tree.get_children()) # Limpa a árvore de logs antes de exibir os novos logs
        for log in todos_logs: # Percorre todos os logs e os insere na árvore
            # Formata a data e hora do log
            data_str = log.data.strftime("%Y-%m-%d")
            hora_str = log.data.strftime("%H:%M:%S")
            self.tree.insert("", tk.END, values=(data_str, hora_str, log.mensagem))
        self.search_result_label.config(text=f"📋 Total de logs carregados: {len(todos_logs)}")

    def on_tree_click(self, event): # Método para lidar com o clique na árvore de logs
        selected = self.tree.focus() # Obtém o item selecionado na árvore
        # Se não houver item selecionado, não faz nada
        if not selected:
            return
        values = self.tree.item(selected, "values") # Obtém os valores do item selecionado
        # Se houver pelo menos 3 valores (data, hora e mensagem do log), exibe uma mensagem com os detalhes do log
        if len(values) >= 3:
            msg = f"🔎 Detalhes:\n📅 Data: {values[0]}\n⏰ Hora: {values[1]}\n🛰️ Log: {values[2]}"
            messagebox.showinfo("Detalhes do Log", msg)
            
            
if __name__ == "__main__": # Ponto de entrada para a aplicação
    """Inicia a aplicação GUI do inventário de componentes AstroSim."""
    root = tk.Tk()
    root.title("AstroSim - Inventário Espacial")
    app = InventoryGUI(root)
    root.mainloop()
