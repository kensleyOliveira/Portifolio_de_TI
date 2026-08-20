import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from modules.Lista_Matriz_adjacencia import Mapa
from modules.buscaDFS import DFS
from modules.buscaBFS import BFS
from modules.dijkstra import Dijkstra
from modules.placeholder import PlaceholderEntry
import math
import mysql.connector
from collections import deque
from modules.ArvoreGeradoraMinima import KruskalAGM
from modules.coloracao import WelchPowell
from modules.ordenacaoTopologica import TarjanTopologico
import graphviz
import os

class SpaceMapGUI(ttk.Frame): # Classe principal da interface gráfica

    def __init__(self, parent): # Inicializa a classe com o pai
        super().__init__(parent) # Chama o construtor da classe pai
        self.parent = parent # Armazena a referência para o pai

        # Conexão MySQL
        self.conn = mysql.connector.connect( # Conecta ao banco de dados MySQL
            host="localhost", 
            user="root",
            password="mysql",
            database="astrosim"
        )
        self.cursor = self.conn.cursor() # Cria um cursor para executar comandos SQL

        # Mapa em memória
        self.mapa = Mapa() # Cria um mapa em memória
        self.carregar_mapa() # Carrega o mapa do banco de dados

        # Variáveis para armazenar o caminho e o tipo de busca para a geração do grafo
        self.caminho_encontrado = None # Armazena o caminho encontrado
        self.tipo_busca = None # Armazena o tipo de busca

        # Widgets
        self._criar_widgets() # Cria os widgets da interface gráfica

        self.atualizar_treeviews() # Atualiza as treeviews com os dados do mapa

    # -------------------------------
    # Carregar grafo do banco
    # -------------------------------
    def carregar_mapa(self): # Carrega o mapa do banco de dados
        self.mapa = Mapa() # Cria um mapa em memória

        self.cursor.execute("SELECT nome FROM vertices") # Seleciona todos os locais
        for (nome,) in self.cursor.fetchall(): # Para cada local encontrado
            self.mapa.adicionar_local(nome) # Adiciona o local ao mapa

        self.cursor.execute("""
            SELECT v1.nome, v2.nome, a.distancia
            FROM arestas a
            JOIN vertices v1 ON a.origem_id = v1.id
            JOIN vertices v2 ON a.destino_id = v2.id
        """) # Seleciona todas as arestas
        for origem, destino, dist in self.cursor.fetchall(): # Para cada aresta encontrada
            self.mapa.adicionar_rota(origem, destino, float(dist)) # Adiciona a rota ao mapa

    # -------------------------------
    # CRUD Banco
    # -------------------------------
    def limpar_campos_local(self): 
        """Limpa o campo de entrada 'local'."""
        self.entry_local.delete(0, tk.END) # Limpa o campo de entrada 'local'

    def limpar_campos_rota(self):
        """Limpa os campos de entrada de 'origem', 'destino' e 'distância'."""
        self.entry_origem.delete(0, tk.END) # Limpa o campo de entrada 'origem'
        self.entry_destino.delete(0, tk.END) # Limpa o campo de entrada 'destino'
        self.entry_distancia.delete(0, tk.END) # Limpa o campo de entrada 'distancia'

    def adicionar_local(self): # Adiciona um novo local ao mapa
        nome = self.entry_local.get().strip() # Obtém o nome do local
        if not nome: return # Se o nome estiver vazio, não faz nada
        try:
            self.cursor.execute("INSERT INTO vertices (nome) VALUES (%s)", (nome,)) # Adiciona o local ao banco de dados
            self.conn.commit() # Confirma a transação
            self.carregar_mapa() # Carrega o mapa do banco de dados
            self.atualizar_treeviews() # Atualiza as treeviews com os dados do mapa
            self.limpar_campos_local() # Limpa os campos de entrada
        except mysql.connector.Error as e: # Captura erros do MySQL
            self.mostrar_status(f"⚠️ Erro ao adicionar local: {e}") # Mostra mensagem de erro

    def remover_local(self): # Remove um local do mapa
        nome = self.entry_local.get().strip() # Obtém o nome do local
        if not nome: return # Se o nome estiver vazio, não faz nada
        try:
            self.cursor.execute("DELETE FROM vertices WHERE nome = %s", (nome,)) # Remove o local do banco de dados
            self.conn.commit() # Confirma a transação
            self.carregar_mapa() # Carrega o mapa do banco de dados
            self.atualizar_treeviews() # Atualiza as treeviews com os dados do mapa
            self.limpar_campos_rota() # Limpa os campos de entrada
        except mysql.connector.Error as e: # Captura erros do MySQL
            self.mostrar_status(f"⚠️ Erro ao remover local: {e}") # Mostra mensagem de erro

    def adicionar_rota(self): # Adiciona uma nova rota ao mapa
        origem = self.entry_origem.get().strip() # Obtém o nome da origem
        destino = self.entry_destino.get().strip() # Obtém o nome do destino
        distancia = self.entry_distancia.get().strip() # Obtém a distância
        if not (origem and destino and distancia): return # Se algum campo estiver vazio, não faz nada
        try:
            self.cursor.execute( # Adiciona a rota ao banco de dados
                "INSERT INTO arestas (origem_id, destino_id, distancia) "
                "VALUES ((SELECT id FROM vertices WHERE nome=%s), "
                "(SELECT id FROM vertices WHERE nome=%s), %s)",
                (origem, destino, distancia)
            )
            self.conn.commit() # Confirma a transação
            self.carregar_mapa() # Carrega o mapa do banco de dados
            self.atualizar_treeviews() # Atualiza as treeviews com os dados do mapa
            self.limpar_campos_rota() # Limpa os campos de entrada
        except mysql.connector.Error as e: # Captura erros do MySQL
            self.mostrar_status(f"⚠️ Erro ao adicionar rota: {e}") # Mostra mensagem de erro

    def remover_rota(self): # Remove uma rota do mapa
        origem = self.entry_origem.get().strip() # Obtém o nome da origem
        destino = self.entry_destino.get().strip() # Obtém o nome do destino
        if not (origem and destino): return # Se algum campo estiver vazio, não faz nada
        try:
            self.cursor.execute( # Remove a rota do banco de dados
                "DELETE FROM arestas "
                "WHERE origem_id=(SELECT id FROM vertices WHERE nome=%s) "
                "AND destino_id=(SELECT id FROM vertices WHERE nome=%s)",
                (origem, destino)
            )
            self.conn.commit() # Confirma a transação
            self.carregar_mapa() # Carrega o mapa do banco de dados
            self.atualizar_treeviews() # Atualiza as treeviews com os dados do mapa
            self.limpar_campos_rota() # Limpa os campos de entrada
        except mysql.connector.Error as e: # Captura erros do MySQL
            self.mostrar_status(f"⚠️ Erro ao remover rota: {e}") # Mostra mensagem de erro

    # -------------------------------
    # Treeviews principais
    # -------------------------------
    def atualizar_treeviews(self): # Atualiza as treeviews com os dados do mapa
        # Locais
        for item in self.tree_locais.get_children(): # Limpa os itens existentes
            self.tree_locais.delete(item) # Remove o item da treeview
        self.cursor.execute("SELECT id, nome FROM vertices ORDER BY id") # Obtém os locais do banco de dados
        for vid, nome in self.cursor.fetchall(): # Itera sobre os locais
            self.tree_locais.insert("", tk.END, values=(vid, nome)) # Adiciona o local à treeview

        # Rotas
        for item in self.tree_rotas.get_children(): # Limpa os itens existentes
            self.tree_rotas.delete(item) # Remove o item da treeview
        self.cursor.execute("""
            SELECT a.id, v1.nome, v2.nome, a.distancia
            FROM arestas a
            JOIN vertices v1 ON a.origem_id = v1.id
            JOIN vertices v2 ON a.destino_id = v2.id
            ORDER BY a.id
        """) # Obtém as rotas do banco de dados
        for rid, origem, destino, dist in self.cursor.fetchall(): # Itera sobre as rotas
            self.tree_rotas.insert("", tk.END, values=(rid, origem, destino, dist)) # Adiciona a rota à treeview

    # Função genérica para criar Treeview com scroll
    def criar_treeview_com_scroll(self, colunas, heading_texts, altura=15): # Cria uma treeview com barras de rolagem
        for widget in self.frame_visualizacao.winfo_children(): # Limpa os widgets existentes
            widget.destroy() # Remove o widget da interface

        frame_tree = ttk.Frame(self.frame_visualizacao) # Cria um novo frame para a treeview
        frame_tree.pack(fill=BOTH, expand=True) # Expande o frame para preencher o espaço disponível

        tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", height=altura) # Cria a treeview
        for col, text in zip(colunas, heading_texts): # Define os cabeçalhos e as colunas
            tree.heading(col, text=text, anchor="center") # Define o cabeçalho da coluna
            tree.column(col, anchor="center", width=100) # Define a coluna da treeview

        # Scrollbars
        vsb = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview) # Cria a scrollbar vertical
        hsb = ttk.Scrollbar(frame_tree, orient="horizontal", command=tree.xview) # Cria a scrollbar horizontal
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set) # Configura as scrollbars
        vsb.pack(side="right", fill="y") # Adiciona a scrollbar vertical
        hsb.pack(side="bottom", fill="x") # Adiciona a scrollbar horizontal
        tree.pack(padx=5, pady=5, fill=BOTH, expand=True) # Adiciona a treeview

        return tree # Retorna a treeview

    # -------------------------------
    # Visualização lista/matriz Treeview
    # -------------------------------
    def mostrar_lista_treeview(self): # Mostra a visualização em lista
        tree = self.criar_treeview_com_scroll( # Cria a treeview
            colunas=("Local", "Rotas"), # Define as colunas
            heading_texts=("Local", "Rotas"), # Define os cabeçalhos
            altura=15 # Define a altura
        )
        for local, rotas in self.mapa.locais.items(): # Para cada local e suas rotas
            rotas_str = ', '.join([f"{dest}({custo})" for dest, custo in rotas]) # Converte as rotas em string
            tree.insert("", tk.END, values=(local, rotas_str)) # Adiciona os valores à treeview

    def mostrar_matriz_treeview(self): # Mostra a visualização em matriz
        locais = sorted(self.mapa.locais.keys()) # Obtém a lista de locais
        tree = self.criar_treeview_com_scroll( # Cria a treeview
            colunas=locais, # Define as colunas
            heading_texts=locais, # Define os cabeçalhos
            altura=len(locais) # Define a altura
        )
        indice = {local: i for i, local in enumerate(locais)} # Cria um índice para os locais
        matriz = [[0]*len(locais) for _ in locais] # Cria a matriz de adjacência
        for origem, rotas in self.mapa.locais.items(): # Para cada origem e suas rotas
            for destino, custo in rotas: # Para cada destino e custo
                i = indice[origem] # Obtém o índice da origem
                j = indice[destino] # Obtém o índice do destino
                matriz[i][j] = custo # Atualiza a matriz de adjacência

        for i, origem in enumerate(locais): # Para cada origem
            row_values = [matriz[i][j] for j in range(len(locais))] # Obtém os valores da linha
            tree.insert("", tk.END, values=row_values) # Adiciona os valores à treeview 

    # -------------------------------
    # Geração de Grafo com Graphviz
    # -------------------------------
    def gerar_grafo(self, tipo_grafo, dados, caminho_arquivo):
        dot = graphviz.Graph(comment=tipo_grafo)
        dot.attr(rankdir='LR')
        
        cores_map = {
            1: 'red', 2: 'blue', 3: 'green', 4: 'orange', 5: 'purple',
            6: 'cyan', 7: 'magenta', 8: 'yellow', 9: 'brown', 10: 'pink'
        }

        if tipo_grafo == "Coloração":
            for local, cor in dados.items():
                dot.node(local, style='filled', color=cores_map.get(cor, 'grey'))
            for origem, vizinhos in self.mapa.locais.items():
                for destino, _ in vizinhos:
                    dot.edge(origem, destino)
            
        elif tipo_grafo == "Ordenação Topológica":
            for i, local in enumerate(dados):
                dot.node(local, label=f'{i+1}. {local}')
            for origem, vizinhos in self.mapa.locais.items():
                for destino, _ in vizinhos:
                    dot.edge(origem, destino, label='')
        
        elif tipo_grafo == "Árvore Geradora Mínima":
            dot = graphviz.Graph(comment="Árvore Geradora Mínima")
            dot.attr(rankdir='LR')
            for origem, destino, custo in dados:
                dot.edge(origem, destino, label=str(custo), fontcolor='red')
            
        else: # Outros grafos
            for local in self.mapa.locais:
                dot.node(local)
            for origem, vizinhos in self.mapa.locais.items():
                for destino, custo in vizinhos:
                    dot.edge(origem, destino, label=str(custo))

        try:
            dot.render(caminho_arquivo, format='png', view=True, cleanup=True)
            self.mostrar_status(f"✅ Gráfico '{tipo_grafo}' gerado em '{caminho_arquivo}.png'.")
        except Exception as e:
            self.mostrar_status(f"⚠️ Erro ao gerar gráfico com Graphviz: {e}")
            
    def gerar_grafo_caminho(self):
        if not self.caminho_encontrado:
            self.mostrar_status("⚠️ Nenhum caminho foi encontrado para gerar o grafo.")
            return

        dot = graphviz.Digraph(comment=f"Caminho por {self.tipo_busca}")
        dot.attr(rankdir='LR')
        
        # Cria os nós do caminho
        for i, (node, _, _) in enumerate(self.caminho_encontrado):
            if i == 0:
                dot.node(node, label=node, style='filled', fillcolor='green') # Origem
            elif i == len(self.caminho_encontrado) - 1:
                dot.node(node, label=node, style='filled', fillcolor='red') # Destino
            else:
                dot.node(node, label=node)
        
        # Cria as arestas do caminho
        for i in range(len(self.caminho_encontrado) - 1):
            origem, _, _ = self.caminho_encontrado[i]
            destino, _, custo = self.caminho_encontrado[i+1]
            
            # Encontra o custo da aresta real entre origem e destino
            custo_aresta = "N/A"
            for vizinho, c in self.mapa.locais.get(origem, []):
                if vizinho == destino:
                    custo_aresta = c
                    break
            
            dot.edge(origem, destino, label=str(custo_aresta), fontcolor='blue')

        caminho_arquivo = f"caminho_{self.tipo_busca.lower()}"
        try:
            dot.render(caminho_arquivo, format='png', view=True, cleanup=True)
            self.mostrar_status(f"✅ Gráfico do caminho gerado em '{caminho_arquivo}.png'.")
        except Exception as e:
            self.mostrar_status(f"⚠️ Erro ao gerar gráfico com Graphviz: {e}")

    # -------------------------------
    # Algoritmo de Coloração de Grafos
    # -------------------------------
    def executar_coloracao(self): # Inicia o algoritmo de coloração
        try:
            algoritmo_welch = WelchPowell(self.mapa) # Cria uma instância do algoritmo de coloração
            cores = algoritmo_welch.colorir() # Executa o algoritmo de coloração
            
            # Limpa o Treeview e prepara para exibir o resultado
            tree = self.criar_treeview_com_scroll( # Cria um Treeview com scroll
                colunas=("Local", "Cor"), # Define as colunas
                heading_texts=("Local", "Cor") # Define os textos dos cabeçalhos
            )

            for local, cor in cores.items(): # Adiciona os valores ao Treeview
                tree.insert("", tk.END, values=(local, cor)) # Insere os valores no Treeview

            self.mostrar_status(f"✅ Coloração de Grafo concluída. Total de cores: {len(set(cores.values()))}") # Mostra mensagem de sucesso 
            
            # Botão para gerar o grafo colorido
            btn_graphviz = ttk.Button(self.frame_visualizacao, text="Gerar Gráfico Colorido", bootstyle=INFO, 
                                      command=lambda: self.gerar_grafo("Coloração", cores, "grafo_colorido")) # Chama a função para gerar o grafo
            btn_graphviz.pack(pady=10) # Adiciona o botão à interface

        except Exception as e:
            self.mostrar_status(f"⚠️ Erro ao executar Coloração: {e}")
            
    def executar_ordenacao_topologica(self):
        try:
            # A ordenação topológica funciona apenas em grafos direcionados acíclicos.
            # A base de dados atual tem arestas não direcionadas, então simulamos arestas
            # direcionadas para o exemplo.
            mapa_direcionado = Mapa()
            for origem, rotas in self.mapa.locais.items(): # Itera sobre as rotas do mapa
                for destino, custo in rotas: # Itera sobre os destinos e custos
                    mapa_direcionado.adicionar_rota(origem, destino, custo, direcionada=True) # Adiciona a rota como direcionada

            algoritmo_tarjan = TarjanTopologico(mapa_direcionado) # Cria uma instância do algoritmo de ordenação
            ordem = algoritmo_tarjan.ordenar() # Executa a ordenação
            
            # Limpa o Treeview e prepara para exibir o resultado
            tree = self.criar_treeview_com_scroll( # Cria um Treeview com scroll
                colunas=("Ordem", "Local"), # Define as colunas
                heading_texts=("Ordem", "Local") # Define os textos dos cabeçalhos
            )

            if ordem: # Verifica se a ordem foi encontrada
                for i, local in enumerate(ordem): # Itera sobre a ordem
                    tree.insert("", tk.END, values=(i + 1, local)) # Insere os valores no Treeview 
                self.mostrar_status(f"✅ Ordenação Topológica concluída.") # Mostra mensagem de sucesso

                # Botão para gerar o grafo de ordenação
                btn_graphviz = ttk.Button(self.frame_visualizacao, text="Gerar Gráfico da Ordem", bootstyle=INFO, 
                                          command=lambda: self.gerar_grafo("Ordenação Topológica", ordem, "ordenacao_topologica")) # Chama a função para gerar o grafo
                btn_graphviz.pack(pady=10) # Adiciona o botão à interface
            else:
                self.mostrar_status("⚠️ Não é possível realizar a Ordenação Topológica (o grafo pode conter ciclos).")

        except Exception as e:
            self.mostrar_status(f"⚠️ Erro ao executar Ordenação Topológica: {e}")

    def executar_agm(self):
        try:
            algoritmo_kruskal = KruskalAGM(self.mapa) # Cria uma instância do algoritmo de Kruskal
            agm = algoritmo_kruskal.encontrar_agm() # Executa o algoritmo de Kruskal

            # Limpa o Treeview e prepara para exibir o resultado
            tree = self.criar_treeview_com_scroll(
                colunas=("Origem", "Destino", "Custo"),
                heading_texts=("Origem", "Destino", "Custo")
            )

            custo_total = 0 # Inicializa o custo total
            for origem, destino, custo in agm: # Itera sobre as arestas da AGM
                tree.insert("", tk.END, values=(origem, destino, custo)) # Insere os valores no Treeview
                custo_total += custo # Atualiza o custo total

            self.mostrar_status(f"✅ Árvore Geradora Mínima concluída. Custo total: {custo_total}")

            # Botão para gerar o grafo AGM
            btn_graphviz = ttk.Button(self.frame_visualizacao, text="Gerar Gráfico da AGM", bootstyle=INFO, 
                                      command=lambda: self.gerar_grafo("Árvore Geradora Mínima", agm, "agm")) # Chama a função para gerar o grafo
            btn_graphviz.pack(pady=10) # Adiciona o botão à interface

        except Exception as e:
            self.mostrar_status(f"⚠️ Erro ao executar Árvore Geradora Mínima: {e}")

    # -------------------------------
    # Status
    # -------------------------------
    def mostrar_status(self, msg): # Atualiza a mensagem de status
        self.status_label.config(text=msg)

    # -------------------------------
    # Executar buscas
    # -------------------------------
    def abrir_janela_busca(self):  # Abre a janela de busca
        window = tk.Toplevel(self)
        window.title("Busca de Rotas")

        # Inputs Origem e Destino
        ttk.Label(window, text="Origem:").grid(row=0, column=0, padx=5, pady=5)
        origem_cb = ttk.Combobox(window, values=list(self.mapa.locais.keys()))
        origem_cb.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(window, text="Destino:").grid(row=1, column=0, padx=5, pady=5)
        destino_cb = ttk.Combobox(window, values=list(self.mapa.locais.keys()))
        destino_cb.grid(row=1, column=1, padx=5, pady=5)

        # Escolha do Algoritmo
        ttk.Label(window, text="Algoritmo:").grid(row=2, column=0, padx=5, pady=5)
        algoritmo_var = tk.StringVar(value="DFS")
        ttk.Radiobutton(window, text="DFS", variable=algoritmo_var, value="DFS").grid(row=2, column=1, sticky="w")
        ttk.Radiobutton(window, text="BFS", variable=algoritmo_var, value="BFS").grid(row=3, column=1, sticky="w")
        ttk.Radiobutton(window, text="Dijkstra", variable=algoritmo_var, value="Dijkstra").grid(row=4, column=1, sticky="w")

        resultado_label = ttk.Label(window, text="", font=("Arial", 10))
        resultado_label.grid(row=5, column=0, columnspan=2, pady=5)

        tree_frame = ttk.Frame(window)
        tree_frame.grid(row=6, column=0, columnspan=2, pady=5, sticky="nsew")

        def executar_busca():
            origem = origem_cb.get()
            destino = destino_cb.get()
            algoritmo = algoritmo_var.get()

            if not origem or not destino:
                resultado_label.config(text="⚠️ Escolha origem e destino")
                return

            # Limpa árvore de passos anterior
            for widget in tree_frame.winfo_children():
                widget.destroy()

            passos_tree = ttk.Treeview(tree_frame, columns=("Nó", "Pai", "Custo"), show="headings", height=10)
            passos_tree.heading("Nó", text="Nó")
            passos_tree.heading("Pai", text="Pai")
            passos_tree.heading("Custo", text="Custo")
            passos_tree.column("Nó", width=100, anchor="center")
            passos_tree.column("Pai", width=100, anchor="center")
            passos_tree.column("Custo", width=100, anchor="center")
            passos_tree.pack(padx=5, pady=5, fill=BOTH, expand=True)

            passos_tree.tag_configure("explorado", background="#000080")
            passos_tree.tag_configure("caminho", background="#008000")

            self.caminho_encontrado = None
            caminho_para_treeview = []

            if algoritmo == "DFS":
                self.tipo_busca = "DFS"
                dfs_runner = DFS(self.mapa.locais)
                caminho_dfs = dfs_runner.buscar(origem, destino)  # <- Chama método do módulo DFS

                if caminho_dfs:
                    self.caminho_encontrado = caminho_dfs
                    caminho_para_treeview = self.caminho_encontrado
                    resultado_label.config(text=f"DFS Caminho: {' -> '.join([n for n, _, _ in caminho_para_treeview])}")
                else:
                    resultado_label.config(text="❌ Nenhum caminho encontrado")

            elif algoritmo == "BFS":
                self.tipo_busca = "BFS"
                bfs_runner = BFS(self.mapa.locais, list(self.mapa.locais.keys()))
                cor, d, pi = bfs_runner.run(origem)

                if d[destino] == float('inf'):
                    resultado_label.config(text="❌ Nenhum caminho encontrado")
                else:
                    v = destino
                    caminho_bfs = []
                    while v is not None:
                        pai = pi[v] if pi[v] is not None else None
                        custo_aresta = d[v] - (d[pai] if pai else 0)
                        caminho_bfs.append((v, pai, d[v]))
                        v = pi[v]

                    caminho_bfs.reverse()
                    self.caminho_encontrado = caminho_bfs
                    caminho_para_treeview = self.caminho_encontrado
                    resultado_label.config(
                        text=f"BFS Caminho: {' -> '.join([n for n,_,_ in caminho_para_treeview])}\nDistância (arestas): {d[destino]}"
                    )

            elif algoritmo == "Dijkstra":
                self.tipo_busca = "Dijkstra"
                matriz, locais = self.mapa.get_matriz_adjacencia()

                # Ajusta matriz para infinito nas arestas inexistentes
                for i in range(len(matriz)):
                    for j in range(len(matriz)):
                        if i != j and matriz[i][j] == 0:
                            matriz[i][j] = math.inf
                        else:
                            matriz[i][j] = float(matriz[i][j])

                dijkstra_runner = Dijkstra(matriz, locais)
                custos, pi, idx = dijkstra_runner.run(origem)
                caminho_dijkstra = dijkstra_runner.reconstruir_caminho(destino)

                if custos[idx[destino]] < math.inf:
                    resultado_label.config(
                        text=f"Dijkstra Caminho: {' -> '.join(caminho_dijkstra)}\nCusto total: {custos[idx[destino]]}"
                    )

                    caminho_completo = []
                    acum = 0
                    for i, n in enumerate(caminho_dijkstra):
                        p = caminho_dijkstra[i - 1] if i > 0 else None
                        if p:
                            for dest, c in self.mapa.locais[p]:
                                if dest == n:
                                    acum += c
                                    break
                        caminho_completo.append((n, p, acum))

                    self.caminho_encontrado = caminho_completo
                    caminho_para_treeview = self.caminho_encontrado
                else:
                    resultado_label.config(text="❌ Nenhum caminho encontrado")

            # Preenche TreeView
            if caminho_para_treeview:
                for i, (n, p, c) in enumerate(caminho_para_treeview):
                    tag = "caminho" if i == len(caminho_para_treeview) - 1 else "explorado"
                    passos_tree.insert("", tk.END, values=(n, p, c), tags=(tag,))
                self.btn_gerar_grafo.config(state=NORMAL)
            else:
                passos_tree.insert("", tk.END, values=("N/A", "N/A", "N/A"))
                self.btn_gerar_grafo.config(state=DISABLED)

        ttk.Button(window, text="Executar Busca", bootstyle=PRIMARY, command=executar_busca).grid(row=7, column=0, columnspan=2, pady=5)
        self.btn_gerar_grafo = ttk.Button(window, text="Gerar Gráfico do Caminho", bootstyle=INFO, state=DISABLED, command=self.gerar_grafo_caminho)
        self.btn_gerar_grafo.grid(row=8, column=0, columnspan=2, pady=5)
    
    # -------------------------------
    # Interface gráfica
    # -------------------------------
    def _criar_widgets(self):
        ttk.Label(self, text="Mapa Espacial", font=("Arial", 16)).pack(pady=10)

        # Entradas locais
        local_frame = ttk.Frame(self)
        local_frame.pack(pady=5, fill=tk.X)
        self.entry_local = PlaceholderEntry(local_frame, width=25, placeholder="Nome do Local")
        self.entry_local.pack(side=LEFT, padx=5)
        ttk.Button(local_frame, text="Adicionar Local", bootstyle=SUCCESS, command=self.adicionar_local).pack(side=LEFT, padx=5)
        ttk.Button(local_frame, text="Remover Local", bootstyle=DANGER, command=self.remover_local).pack(side=LEFT, padx=5)

        # Entradas rotas
        rota_frame = ttk.Frame(self)
        rota_frame.pack(pady=5, fill=tk.X)
        self.entry_origem = PlaceholderEntry(rota_frame, width=15, placeholder="Origem")
        self.entry_origem.pack(side=LEFT, padx=5)
        self.entry_destino = PlaceholderEntry(rota_frame, width=15, placeholder="Destino")
        self.entry_destino.pack(side=LEFT, padx=5)
        self.entry_distancia = PlaceholderEntry(rota_frame, width=10, placeholder="Distância")
        self.entry_distancia.pack(side=LEFT, padx=5)
        ttk.Button(rota_frame, text="Adicionar Rota", bootstyle=SUCCESS, command=self.adicionar_rota).pack(side=LEFT, padx=5)
        ttk.Button(rota_frame, text="Remover Rota", bootstyle=DANGER, command=self.remover_rota).pack(side=LEFT, padx=5)

        # Treeview Locais
        ttk.Label(self, text="Locais (Vértices)", font=("Arial", 12)).pack(pady=5)
        self.tree_locais = ttk.Treeview(self, columns=("ID", "Nome"), show="headings", height=6, bootstyle=INFO)
        self.tree_locais.heading("ID", text="ID", anchor="center")
        self.tree_locais.heading("Nome", text="Nome", anchor="center")
        self.tree_locais.column("ID", anchor="center", width=50)
        self.tree_locais.column("Nome", anchor="center", width=150)
        self.tree_locais.pack(padx=10, pady=5, fill=tk.X)

        # Treeview Rotas
        ttk.Label(self, text="Rotas (Arestas)", font=("Arial", 12)).pack(pady=5)
        self.tree_rotas = ttk.Treeview(self, columns=("ID", "Origem", "Destino", "Distância"),
                                       show="headings", height=8, bootstyle=INFO)
        for col in ("ID", "Origem", "Destino", "Distância"):
            self.tree_rotas.heading(col, text=col, anchor="center")
            self.tree_rotas.column(col, anchor="center", width=100)
        self.tree_rotas.pack(padx=10, pady=5, fill=tk.X)

        # Botões de visualização
        view_frame = ttk.Frame(self)
        view_frame.pack(pady=5)
        ttk.Button(view_frame, text="Lista Adjacência", bootstyle=PRIMARY, command=self.mostrar_lista_treeview).pack(side=LEFT, padx=5)
        ttk.Button(view_frame, text="Matriz Adjacência", bootstyle=PRIMARY, command=self.mostrar_matriz_treeview).pack(side=LEFT, padx=5)
        ttk.Button(view_frame, text="Buscar Caminho", bootstyle=INFO, command=self.abrir_janela_busca).pack(side=LEFT, padx=5)

        # Novos botões de algoritmos
        algoritmos_frame = ttk.Frame(self)
        algoritmos_frame.pack(pady=5)
        ttk.Button(algoritmos_frame, text="Coloração de Grafo", bootstyle=SUCCESS, command=self.executar_coloracao).pack(side=LEFT, padx=5)
        ttk.Button(algoritmos_frame, text="Ordenação Topológica", bootstyle=SUCCESS, command=self.executar_ordenacao_topologica).pack(side=LEFT, padx=5)
        ttk.Button(algoritmos_frame, text="Árvore Geradora Mínima", bootstyle=SUCCESS, command=self.executar_agm).pack(side=LEFT, padx=5)
        
        # Frame para visualização de lista/matriz
        self.frame_visualizacao = ttk.Frame(self)
        self.frame_visualizacao.pack(padx=10, pady=10, fill=BOTH, expand=True)

        # Status
        self.status_label = ttk.Label(self, text="", font=("Arial", 10), bootstyle=SECONDARY)
        self.status_label.pack(pady=10)