
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector
import os
from modules.agenda_gui import AgendaGUI
from modules.troco import carregar_unidades, pagar_compra, receber_venda, registrar_transacao

# ---------- CONFIGURAÇÃO DO BANCO (ajuste conforme seu ambiente) ----------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "mysql",
    "database": "astrosim"
}

class ResourceManagerGUI(ttk.Frame):
    """
    Interface principal do AstroSim para gerenciar:
    - Comércio B2B (problema do troco)
    - Inventário de comprador e vendedor
    - Acesso ao módulo de Escalonamento de Missões (AgendaGUI)
    """

    def __init__(self, parent):
        super().__init__(parent)

        # Carregar recursos do BD
        self.unidades = carregar_unidades()

        # Inventários iniciais
        self.inventario_comprador = {u["id_unidade"]: 2 for u in self.unidades}
        self.inventario_vendedor = {u["id_unidade"]: 1 for u in self.unidades}

        self._criar_interface()

    # ---------------------- INTERFACE ---------------------- #
    def _criar_interface(self):
        """Monta a interface gráfica principal"""
        ttk.Label(
            self,
            text="Comércio B2B - Problema do Troco",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        # Entrada do valor do minério
        valor_frame = ttk.Frame(self)
        valor_frame.pack(pady=5)
        ttk.Label(valor_frame, text="Valor do minério:").pack(side=tk.LEFT, padx=5)
        self.valor_entry = ttk.Entry(valor_frame, width=10)
        self.valor_entry.pack(side=tk.LEFT)
        self.valor_entry.insert(0, "100")

        # Inventário comprador
        ttk.Label(self, text="Inventário do Comprador:").pack(pady=5)
        self.tree_comprador = self._criar_inventario_tree()

        # Inventário vendedor
        ttk.Label(self, text="Inventário do Vendedor:").pack(pady=5)
        self.tree_vendedor = self._criar_inventario_tree()

        # Resultado transações
        ttk.Label(self, text="Resultado da Transação:").pack(pady=5)
        resultado_frame = ttk.Frame(self)
        # Usamos fill="x" e padx para dar espaço horizontal
        resultado_frame.pack(pady=5, fill="x", padx=10) 

        self.tree_resultado = ttk.Treeview(
            resultado_frame, # Parente agora é o frame
            columns=("recurso", "quantidade", "valor"),
            show="headings",
            height=7
        )

        # Scrollbars
        scroll_y_res = ttk.Scrollbar(resultado_frame, orient="vertical", command=self.tree_resultado.yview)
        scroll_x_res = ttk.Scrollbar(resultado_frame, orient="horizontal", command=self.tree_resultado.xview)
        self.tree_resultado.configure(yscrollcommand=scroll_y_res.set, xscrollcommand=scroll_x_res.set)

        # Headings e Alinhamento de Coluna
        self.tree_resultado.heading("recurso", text="Recurso")
        self.tree_resultado.column("recurso", anchor="center", width=150)
        
        self.tree_resultado.heading("quantidade", text="Qtd Usada")
        self.tree_resultado.column("quantidade", anchor="center", width=100)
        
        self.tree_resultado.heading("valor", text="Valor Unitário")
        self.tree_resultado.column("valor", anchor="center", width=100)

        # Layout com Grid dentro do Frame
        self.tree_resultado.grid(row=0, column=0, sticky="nsew")
        scroll_y_res.grid(row=0, column=1, sticky="ns")
        scroll_x_res.grid(row=1, column=0, sticky="ew")

        # Configura o redimensionamento do frame
        resultado_frame.rowconfigure(0, weight=1)
        resultado_frame.columnconfigure(0, weight=1)

        # Botões de compra/venda
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Comprar", command=self.run_compra).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Vender", command=self.run_venda).pack(side=tk.LEFT, padx=5)

        # Botão para abrir Agenda de Missões
        ttk.Button(self, text="Gerenciar Missões", command=self.abrir_agenda).pack(pady=10)
        
        # Botão para Cadastrar Novo Recurso
        ttk.Button(self, text="Cadastrar Nova Unidade de Recurso", command=self.abrir_cadastro_recurso).pack(pady=5)

        # Inicializar inventários na tela
        self._atualizar_inventario_views()

    def _criar_inventario_tree(self):
        """Cria treeview genérica para inventário com scrollbars e alinhamento"""
        
        # Frame para conter o Treeview e os Scrollbars
        tree_frame = ttk.Frame(self)
        # Usamos fill="x" e padx para dar espaço horizontal
        tree_frame.pack(pady=5, fill="x", padx=10)

        tree = ttk.Treeview(
            tree_frame, # Parente agora é o frame
            columns=("nome", "valor", "quantidade"),
            show="headings",
            height=5
        )
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        # Headings e Alinhamento de Coluna
        tree.heading("nome", text="Recurso")
        tree.column("nome", anchor="center", width=150)
        
        tree.heading("valor", text="Valor Unitário")
        tree.column("valor", anchor="center", width=100)
        
        tree.heading("quantidade", text="Qtd")
        tree.column("quantidade", anchor="center", width=70)

        # Layout com Grid dentro do Frame
        tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        # Configura o redimensionamento do frame
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        
        return tree
    # ---------------------- INVENTÁRIOS ---------------------- #
    def _atualizar_inventario_views(self):
        """Atualiza os Treeviews de inventário do comprador e vendedor."""
        for tree, inventario in [
            (self.tree_comprador, self.inventario_comprador),
            (self.tree_vendedor, self.inventario_vendedor),
        ]:
            for i in tree.get_children():
                tree.delete(i)
            for u in self.unidades:
                qtd = inventario.get(u["id_unidade"], 0)
                tree.insert(
                    "",
                    "end",
                    iid=f"{tree}-{u['id_unidade']}",
                    values=(u["nome_recurso"], u["valor_unitario"], qtd),
                )

    def _mostrar_resultado(self, dados, sucesso, resto):
        """Exibe o resultado da operação no treeview de resultado"""
        for i in self.tree_resultado.get_children():
            self.tree_resultado.delete(i)
        for nome, qtd, valor in dados:
            self.tree_resultado.insert("", "end", values=(nome, qtd, valor))
        if not sucesso:
            self.tree_resultado.insert("", "end", values=("Faltou", "-", f"{resto:.2f}"))

    # ---------------------- OPERAÇÕES ---------------------- #
    def run_compra(self):
        """Explorador COMPRA minério (usa recursos do comprador)."""
        valor = self._obter_valor()
        if valor is None:
            return

        sucesso, pagamento, resto = pagar_compra(valor, self.inventario_comprador)
        self._mostrar_resultado(pagamento, sucesso, resto)

        if sucesso:
            # Debita inventário
            for nome, qtd, valor_unit in pagamento:
                for u in self.unidades:
                    if u["nome_recurso"] == nome:
                        self.inventario_comprador[u["id_unidade"]] -= qtd
            registrar_transacao(1, 2, valor, valor - resto)

        self._atualizar_inventario_views()

    def run_venda(self):
        """Explorador VENDE minério (usa recursos do vendedor)."""
        valor = self._obter_valor()
        if valor is None:
            return

        sucesso, pagamento, resto = receber_venda(valor, self.inventario_vendedor)
        self._mostrar_resultado(pagamento, sucesso, resto)

        if sucesso:
            # Debita inventário do vendedor
            for nome, qtd, valor_unit in pagamento:
                for u in self.unidades:
                    if u["nome_recurso"] == nome:
                        self.inventario_vendedor[u["id_unidade"]] -= qtd
            registrar_transacao(2, 1, valor, valor - resto)

        self._atualizar_inventario_views()

    def _obter_valor(self):
        """Lê o valor do campo de entrada com validação"""
        try:
            return float(self.valor_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido")
            return None

    # ---------------------- INTEGRAÇÃO COM AGENDA ---------------------- #
    def abrir_agenda(self):
        """Abre a janela de gerenciamento de missões (AgendaGUI)."""
        janela_agenda = tk.Toplevel(self)
        janela_agenda.title("Escalonamento de Missões")
        agenda_frame = AgendaGUI(janela_agenda)
        agenda_frame.pack(fill="both", expand=True)

     # ---------------------- CADASTRO DE RECURSO (NOVO) ---------------------- #
    def abrir_cadastro_recurso(self):
        """Abre uma janela Toplevel para cadastrar uma nova UnidadeRecurso."""
        janela_cadastro = tk.Toplevel(self)
        janela_cadastro.title("Cadastrar Novo Recurso")
        janela_cadastro.geometry("350x170")

        form_frame = ttk.Frame(janela_cadastro, padding=10)
        form_frame.pack(fill="both", expand=True)

        ttk.Label(form_frame, text="Nome do Recurso:").grid(row=0, column=0, sticky="w", pady=5)
        nome_entry = ttk.Entry(form_frame, width=30)
        nome_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Valor Unitário:").grid(row=1, column=0, sticky="w", pady=5)
        valor_entry = ttk.Entry(form_frame, width=30)
        valor_entry.grid(row=1, column=1, padx=5, pady=5)

        def _salvar_recurso():
            """Função interna para salvar o novo recurso no BD."""
            nome = nome_entry.get().strip()
            valor_txt = valor_entry.get().strip()

            if not nome:
                messagebox.showerror("Erro", "Nome do recurso é obrigatório.", parent=janela_cadastro)
                return
            
            try:
                valor = float(valor_txt)
                if valor <= 0:
                    messagebox.showerror("Erro", "Valor deve ser um número positivo.", parent=janela_cadastro)
                    return
            except Exception:
                messagebox.showerror("Erro", "Valor unitário inválido. Use formato 123.45", parent=janela_cadastro)
                return
            
            conn = None
            try:
                # Usar a DB_CONFIG definida no início do arquivo
                conn = mysql.connector.connect(**DB_CONFIG) 
                cur = conn.cursor()
                sql = "INSERT INTO UnidadesRecurso (nome_recurso, valor_unitario) VALUES (%s, %s)"
                cur.execute(sql, (nome, valor))
                conn.commit()
                cur.close()
                
                messagebox.showinfo("Sucesso", "Novo recurso salvo com sucesso.", parent=janela_cadastro)
                janela_cadastro.destroy()
                
                # Atualizar a GUI principal para refletir o novo recurso
                self.unidades = carregar_unidades()
                self._atualizar_inventario_views()

            except Exception as e:
                messagebox.showerror("Erro BD", f"Erro ao salvar recurso: {e}", parent=janela_cadastro)
            finally:
                if conn:
                    conn.close()

        btn_salvar = ttk.Button(form_frame, text="Salvar Recurso", command=_salvar_recurso)
        btn_salvar.grid(row=2, column=0, columnspan=2, pady=10)

        # Tornar a janela modal (foca nesta janela)
        janela_cadastro.transient(self)
        janela_cadastro.grab_set()
        self.wait_window(janela_cadastro)
