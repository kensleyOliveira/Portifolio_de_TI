import ttkbootstrap as tb
import tkinter as tk
from tkinter import messagebox
import time
from modules.pesquisaRabinKarp import RabinKarp

class TextSearchWindow(tk.Toplevel): # Janela para busca de texto nos logs
    """Classe para janela de busca de texto nos logs.
    Esta janela permite ao usuário buscar por um padrão específico nos logs armazenados no inventário.
    A busca é realizada utilizando o algoritmo Rabin-Karp, que é eficiente para encontrar padrões em textos.
    A janela exibe os resultados da busca em uma tabela, permitindo ao usuário visualizar rapidamente os logs que contêm o padrão buscado.
    A janela também possui funcionalidades para limpar a busca e voltar à janela principal.
    Args:
        parent (tk.Toplevel): A janela pai onde a busca será realizada.
        inventory (Inventory): O inventário que contém os logs a serem pesquisados.
    """
    def __init__(self, parent, inventory):
        super().__init__(parent)
        self.parent = parent
        self.inventory = inventory

        self.title("Busca de Texto - Logs")
        self.geometry("750x450")

        # Campo de entrada para padrão de busca
        lbl = tb.Label(self, text="Digite o padrão para busca:")
        lbl.pack(pady=(10,5), padx=10, anchor="w")

        self.text_search_entry = tb.Entry(self)
        self.text_search_entry.pack(pady=5, fill="x", padx=10)
        self.text_search_entry.bind("<Return>", lambda e: self.perform_text_search())

        # Frame para botões e label de resultado
        btn_frame = tb.Frame(self)
        btn_frame.pack(pady=5, padx=10, fill="x")

        tb.Button(btn_frame, text="Buscar", bootstyle="primary", command=self.perform_text_search).pack(side=tk.LEFT, padx=(0,5))
        tb.Button(btn_frame, text="Limpar Busca", bootstyle="warning", command=self.clear_search).pack(side=tk.LEFT, padx=5)
        tb.Button(btn_frame, text="Voltar", bootstyle="secondary", command=self.destroy).pack(side=tk.RIGHT)

        self.result_label = tb.Label(self, text="")
        self.result_label.pack(pady=(0,10), padx=10, anchor="w")

        # Treeview para mostrar logs
        tree_frame = tb.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        tree_scroll = tb.Scrollbar(tree_frame, orient="vertical")
        tree_scroll.pack(side="right", fill="y")

        self.tree = tb.Treeview(tree_frame, columns=("data", "hora", "mensagem"), show="headings", yscrollcommand=tree_scroll.set)
        self.tree.pack(fill="both", expand=True)
        tree_scroll.config(command=self.tree.yview)

        self.tree.heading("data", text="Data")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("mensagem", text="Mensagem")
        self.tree.column("data", width=100, anchor="center")
        self.tree.column("hora", width=80, anchor="center")
        self.tree.column("mensagem", anchor="w")

        self.tree.bind("<Double-1>", self.on_double_click)

        self.load_all_logs()

    def load_all_logs(self):
        self.tree.delete(*self.tree.get_children())
        todos_logs = self.inventory.get_all_logs()
        todos_logs.sort(key=lambda log: log.data, reverse=True)  # Ordena descrescente por data
        for log in todos_logs:
            data_str = log.data.strftime("%Y-%m-%d")
            hora_str = log.data.strftime("%H:%M:%S")
            self.tree.insert("", tk.END, values=(data_str, hora_str, log.mensagem))
        self.result_label.config(text=f"Total de logs: {len(todos_logs)}")

    def perform_text_search(self):
        valor = self.text_search_entry.get().strip()
        if not valor:
            messagebox.showwarning("Aviso", "Digite um termo para busca.")
            return

        rk = RabinKarp()
        todos_logs = self.inventory.get_all_logs()

        encontrados = []
        total_ocorrencias = 0
        inicio = time.time()

        for log in todos_logs:
            count, _, _ = rk.buscar(log.mensagem, valor)
            if count > 0:
                encontrados.append((log.data, log.mensagem))
                total_ocorrencias += count

        fim = time.time()
        tempo = (fim - inicio) * 1000

        encontrados.sort(key=lambda t: t[0], reverse=True)  # Ordena por data descrescente

        self.tree.delete(*self.tree.get_children())
        for data, msg in encontrados:
            data_str = data.strftime("%Y-%m-%d")
            hora_str = data.strftime("%H:%M:%S")
            self.tree.insert("", tk.END, values=(data_str, hora_str, msg))

        if encontrados:
            self.result_label.config(text=f"Logs encontrados: {len(encontrados)} | Total de ocorrências: {total_ocorrencias} | Tempo: {tempo:.2f} ms")
        else:
            self.result_label.config(text="Nenhum log correspondente encontrado.")

    def clear_search(self):
        self.text_search_entry.delete(0, tk.END)
        self.load_all_logs()
        self.result_label.config(text="Busca limpa, mostrando todos os logs.")

    def on_double_click(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, "values")
        msg = f"🔎 Detalhes:\nData: {values[0]}\nHora: {values[1]}\nMensagem: {values[2]}"
        messagebox.showinfo("Detalhes do Log", msg)
