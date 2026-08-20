

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector
import os

from modules import algoritmoGuloso  # importa a função de escalonamento
from modules.escalonamentoIntervalor import Intervalo, calcular_escalonamento_dp  # importa a função de escalonamento

# ---------- CONFIGURAÇÃO DO BANCO (ajuste conforme seu ambiente) ----------
DB_CONFIG = {
    "host": os.environ.get("ASTROSIM_DB_HOST", "localhost"),
    "user": os.environ.get("ASTROSIM_DB_USER", "root"),
    "password": os.environ.get("ASTROSIM_DB_PASSWORD", "mysql"),
    "database": os.environ.get("ASTROSIM_DB_NAME", "astrosim"),
}

DEFAULT_EXPLORADOR_ID = 1  # ajuste/parametrize conforme necessidade

# ---------- UTILITÁRIOS DB ----------
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        messagebox.showerror("Erro BD", f"Não foi possível conectar ao BD: {e}")
        raise

# ---------- GUI ----------
class AgendaGUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self._criar_interface()
        self.carregar_missoes_do_bd()
        self.carregar_amostras_do_bd()
        self.carregar_missoes_do_bd_recomp()

    def _criar_interface(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=8)

        # Aba 1: Cadastro de Missões
        self.frame_missoes = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_missoes, text="Missões (Cadastro)")
        self._montar_form_missao(self.frame_missoes)
        
        # Aba 2: Cadastro de Amostras
        self.frame_cadastro_amostras = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_cadastro_amostras, text="Amostras (Cadastro)")
        self._montar_form_amostra(self.frame_cadastro_amostras)

        # Aba 3: Agendamento / Escalonamento
        self.frame_agendamento = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_agendamento, text="Agendamento (Escalonar)")
        self._montar_agendamento(self.frame_agendamento)

        # Aba 4: Coleta de Minérios (Mochila)
        self.frame_coleta = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_coleta, text="Coleta de Minérios (Mochila)")
        self._montar_coleta_minerios(self.frame_coleta)

        # Aba 5: Escalonamento por Recompensa
        self.frame_escalonamento = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_escalonamento, text="Escalonamento (Recompensa)")
        self._montar_escalonamento_recompensa(self.frame_escalonamento)

    # ------------ FORMULÁRIO DE MISSÃO ------------
    def _montar_form_missao(self, parent):
        frm = ttk.Frame(parent)
        frm.pack(fill="x", padx=8, pady=8)

        labels = [
            ("Nome da missão:", "nome_missao"),
            ("Planeta alvo:", "planeta_alvo"),
            ("Data (YYYY-MM-DD):", "data_missao"),
            ("Hora início (int):", "tempo_inicio"),
            ("Hora fim (int):", "tempo_fim"),
            ("Recompensa (valor):", "recompensa_valor"),
        ]
        self.form_vars = {}
        for i, (lbl, key) in enumerate(labels):
            ttk.Label(frm, text=lbl).grid(row=i, column=0, sticky="w", pady=4)
            ent = ttk.Entry(frm)
            ent.grid(row=i, column=1, sticky="ew", padx=6, pady=4)
            self.form_vars[key] = ent
        frm.columnconfigure(1, weight=1)

        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill="x", padx=8, pady=6)
        ttk.Button(btn_frame, text="Salvar missão", command=self.salvar_missao_db).pack(side="left")
        ttk.Button(btn_frame, text="Limpar campos", command=self._limpar_form).pack(side="left", padx=6)

    def _montar_form_amostra(self, parent):
        """ Cria o formulário de cadastro de amostras """
        frm = ttk.Frame(parent)
        frm.pack(fill="x", padx=8, pady=8)

        labels = [
            ("Nome do Minério:", "nome_minerio"),
            ("Localização (Zona):", "localizacao_zona"),
            ("Peso Disponível (kg):", "peso_disponivel_kg"),
            ("Valor Total Disponível:", "valor_total_disponivel"),
        ]
        # Usar um dicionário de variáveis diferente para este formulário
        self.form_vars_amostra = {} 
        for i, (lbl, key) in enumerate(labels):
            ttk.Label(frm, text=lbl).grid(row=i, column=0, sticky="w", pady=4)
            ent = ttk.Entry(frm)
            ent.grid(row=i, column=1, sticky="ew", padx=6, pady=4)
            self.form_vars_amostra[key] = ent
        frm.columnconfigure(1, weight=1)

        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill="x", padx=8, pady=6)
        ttk.Button(btn_frame, text="Salvar Amostra", command=self.salvar_amostra_db).pack(side="left")
        ttk.Button(btn_frame, text="Limpar Campos", command=self._limpar_form_amostra).pack(side="left", padx=6)

    def _limpar_form_amostra(self):
        """ Limpa os campos do formulário de amostras """
        for ent in self.form_vars_amostra.values():
            ent.delete(0, "end")

    def salvar_amostra_db(self):
        """ Salva a nova amostra de minério no banco de dados """
        nome = self.form_vars_amostra["nome_minerio"].get().strip()
        localizacao = self.form_vars_amostra["localizacao_zona"].get().strip() or None # Permite nulo
        peso_txt = self.form_vars_amostra["peso_disponivel_kg"].get().strip()
        valor_txt = self.form_vars_amostra["valor_total_disponivel"].get().strip()

        if not nome:
            messagebox.showerror("Erro", "Nome do minério é obrigatório.")
            return
        
        try:
            peso = float(peso_txt)
            if peso <= 0:
                messagebox.showerror("Erro", "Peso deve ser um número positivo.")
                return
        except Exception:
            messagebox.showerror("Erro", "Peso disponível inválido. Use formato 123.45")
            return
        
        try:
            valor = float(valor_txt)
            if valor <= 0:
                 messagebox.showerror("Erro", "Valor total deve ser um número positivo.")
                 return
        except Exception:
            messagebox.showerror("Erro", "Valor total inválido. Use formato 123.45")
            return

        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            sql = """
                INSERT INTO AmostrasMinerio
                (nome_minerio, localizacao_zona, peso_disponivel_kg, valor_total_disponivel)
                VALUES (%s, %s, %s, %s)
            """
            cur.execute(sql, (nome, localizacao, peso, valor))
            conn.commit()
            cur.close()
            messagebox.showinfo("Sucesso", "Amostra de minério salva com sucesso.")
            self._limpar_form_amostra()
            
            # Recarregar a lista na aba de coleta para refletir a nova amostra
            self.carregar_amostras_do_bd() 
            
        except Exception as e:
            messagebox.showerror("Erro BD", f"Erro ao salvar amostra: {e}")
        finally:
            if conn:
                conn.close()

    def _limpar_form(self):
        for ent in self.form_vars.values():
            ent.delete(0, "end")

    def salvar_missao_db(self):
        nome = self.form_vars["nome_missao"].get().strip()
        planeta = self.form_vars["planeta_alvo"].get().strip()
        data_txt = self.form_vars["data_missao"].get().strip()
        inicio_txt = self.form_vars["tempo_inicio"].get().strip()
        fim_txt = self.form_vars["tempo_fim"].get().strip()
        recompensa_txt = self.form_vars["recompensa_valor"].get().strip() or "0"

        if not nome:
            messagebox.showerror("Erro", "Nome da missão obrigatório.")
            return
        try:
            data_missao = datetime.strptime(data_txt, "%Y-%m-%d").date()
        except Exception:
            messagebox.showerror("Erro", "Data inválida. Formato: YYYY-MM-DD.")
            return
        try:
            inicio = int(inicio_txt)
            fim = int(fim_txt)
            if fim <= inicio:
                messagebox.showerror("Erro", "Tempo fim deve ser maior que tempo início.")
                return
        except Exception:
            messagebox.showerror("Erro", "Tempo início/fim devem ser inteiros.")
            return
        try:
            recompensa = float(recompensa_txt)
        except Exception:
            messagebox.showerror("Erro", "Recompensa inválida.")
            return

        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            sql = """
                INSERT INTO MissoesExploracao
                (nome_missao, planeta_alvo, data_missao, tempo_inicio, tempo_fim, recompensa_valor)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cur.execute(sql, (nome, planeta, data_missao, inicio, fim, recompensa))
            conn.commit()
            cur.close()
            messagebox.showinfo("Sucesso", "Missão salva com sucesso.")
            self._limpar_form()
            self.carregar_missoes_do_bd()
            self.carregar_missoes_do_bd_recomp()    
        except Exception as e:
            messagebox.showerror("Erro BD", f"Erro ao salvar missão: {e}")
        finally:
            if conn:
                conn.close()

    # ------------ AGENDAMENTO / ESCALONAMENTO ------------
    def _montar_agendamento(self, parent):
        top = ttk.Frame(parent)
        top.pack(fill="both", expand=True, padx=8, pady=8)

        # --- Listbox com scrollbars ---
        left = ttk.Frame(top)
        left.pack(side="left", fill="y", padx=(0,8))
        ttk.Label(left, text="Missões disponíveis:").pack(anchor="w")

        self.lb_missoes = tk.Listbox(left, selectmode="extended", width=40, height=15)
        self.lb_missoes.pack(side="left", fill="both", expand=True)

        scroll_y = ttk.Scrollbar(left, orient="vertical", command=self.lb_missoes.yview)
        scroll_y.pack(side="right", fill="y")

        scroll_x = ttk.Scrollbar(left, orient="horizontal", command=self.lb_missoes.xview)
        scroll_x.pack(side="bottom", fill="x")

        self.lb_missoes.config(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        # --- Botões ---
        mid = ttk.Frame(top)
        mid.pack(side="left", fill="y", padx=(0,8))
        ttk.Button(mid, text="Adicionar →", command=self.adicionar_selecionadas_para_tree).pack(pady=6)
        ttk.Button(mid, text="Remover selecionadas", command=self.remover_selecionadas_tree).pack(pady=6)
        ttk.Button(mid, text="Escalonar agenda", command=self.escalonar_agenda).pack(pady=12)

        # --- Treeview com scrollbars ---
        right = ttk.Frame(top)
        right.pack(side="left", fill="both", expand=True)
        ttk.Label(right, text="Missões selecionadas / Resultado:").pack(anchor="w")

        columns = ("id_missao", "nome", "planeta", "data", "inicio", "fim", "recompensa")
        tree_frame = ttk.Frame(right)
        tree_frame.pack(fill="both", expand=True)

        self.tree_missoes = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        for col, head in zip(columns, ("ID", "Nome", "Planeta", "Data", "Início", "Fim", "Recompensa")):
            self.tree_missoes.heading(col, text=head)
            self.tree_missoes.column(col, width=90, anchor="center")

        scroll_y_tree = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_missoes.yview)
        scroll_x_tree = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree_missoes.xview)
        self.tree_missoes.configure(yscrollcommand=scroll_y_tree.set, xscrollcommand=scroll_x_tree.set)

        self.tree_missoes.grid(row=0, column=0, sticky="nsew")
        scroll_y_tree.grid(row=0, column=1, sticky="ns")
        scroll_x_tree.grid(row=1, column=0, sticky="ew")

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        # --- Botões inferiores ---
        bottom = ttk.Frame(parent)
        bottom.pack(fill="x", padx=8, pady=6)
        ttk.Button(bottom, text="Salvar agenda selecionada no BD", command=self.salvar_agenda_bd).pack(side="left")
        ttk.Button(bottom, text="Recarregar missões", command=self.carregar_missoes_do_bd).pack(side="left", padx=6)
        ttk.Button(bottom, text="Voltar", command=self.parent.destroy).pack(side="right")

    def carregar_missoes_do_bd(self):
        try:
            conn = get_db_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM MissoesExploracao ORDER BY data_missao, tempo_inicio")
            rows = cur.fetchall()
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro BD", f"Erro ao carregar missões: {e}")
            rows = []

        self.lb_missoes.delete(0, "end")
        self._missoes_cache = {}
        for r in rows:
            display = f"[{r['id_missao']}] {r['nome_missao']} | {r['planeta_alvo']} | {r['data_missao']} ({r['tempo_inicio']}-{r['tempo_fim']})"
            self.lb_missoes.insert("end", display)
            self._missoes_cache[display] = r

    def adicionar_selecionadas_para_tree(self):
        selections = [self.lb_missoes.get(i) for i in self.lb_missoes.curselection()]
        if not selections:
            messagebox.showinfo("Info", "Nenhuma missão selecionada na lista.")
            return
        for disp in selections:
            r = self._missoes_cache.get(disp)
            if not r:
                continue
            iid = f"m_{r['id_missao']}"
            if iid in self.tree_missoes.get_children():
                continue
            self.tree_missoes.insert("", "end", iid=iid, values=(
                r["id_missao"],
                r["nome_missao"],
                r["planeta_alvo"],
                r["data_missao"],
                r["tempo_inicio"],
                r["tempo_fim"],
                float(r.get("recompensa_valor") or 0),
            ))

    def remover_selecionadas_tree(self):
        for iid in self.tree_missoes.selection():
            self.tree_missoes.delete(iid)

    def escalonar_agenda(self):
        items = []
        for iid in self.tree_missoes.get_children():
            vals = self.tree_missoes.item(iid, "values")
            item = {
                "id_missao": int(vals[0]),
                "nome_missao": vals[1],
                "planeta_alvo": vals[2],
                "data_missao": vals[3],
                "tempo_inicio": int(vals[4]),
                "tempo_fim": int(vals[5]),
                "recompensa_valor": float(vals[6]),
            }
            items.append(item)

        if not items:
            messagebox.showinfo("Info", "Nenhuma missão na lista para escalonar.")
            return

        # lista original
        orig_ids = {m["id_missao"] for m in items}

        # chama o escalonador guloso
        selecionadas = algoritmoGuloso.escalonar_missoes(items)
        selecionadas_ids = {m["id_missao"] for m in selecionadas}

        # determinar removidas
        removidas = orig_ids - selecionadas_ids
        removidas_nomes = [m["nome_missao"] for m in items if m["id_missao"] in removidas]

        # limpar tree e reexibir apenas as selecionadas
        for iid in self.tree_missoes.get_children():
            self.tree_missoes.delete(iid)
        for r in selecionadas:
            iid = f"m_{r['id_missao']}"
            self.tree_missoes.insert("", "end", iid=iid, values=(
                r["id_missao"],
                r["nome_missao"],
                r["planeta_alvo"],
                r["data_missao"],
                r["tempo_inicio"],
                r["tempo_fim"],
                float(r.get("recompensa_valor") or 0),
            ))

        msg = f"{len(selecionadas)} missões escalonadas (sem sobreposição)."
        if removidas_nomes:
            msg += "\n\nMissões removidas:\n- " + "\n- ".join(removidas_nomes)

        messagebox.showinfo("Escalonado", msg)

    def salvar_agenda_bd(self):
        ids = []
        for iid in self.tree_missoes.get_children():
            vals = self.tree_missoes.item(iid, "values")
            ids.append((int(vals[0]), vals[3]))

        if not ids:
            messagebox.showinfo("Info", "Nenhuma missão para salvar na agenda.")
            return

        conn = None  # Inicializa a conexão como None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # --- INÍCIO DA MODIFICAÇÃO (OPÇÃO A) ---
            # 1. Limpa a agenda anterior deste explorador
            sql_delete = "DELETE FROM AgendaExplorador WHERE id_explorador = %s"
            cur.execute(sql_delete, (DEFAULT_EXPLORADOR_ID,))
            # --- FIM DA MODIFICAÇÃO ---

            # 2. Insere a nova agenda
            sql_insert = """
                INSERT INTO AgendaExplorador (id_explorador, id_missao_selecionada, data_agendamento)
                VALUES (%s, %s, %s)
            """
            for id_missao, data_missao in ids:
                cur.execute(sql_insert, (DEFAULT_EXPLORADOR_ID, id_missao, data_missao))
            
            conn.commit()  # Efetiva o DELETE e os INSERTs juntos
            cur.close()
            messagebox.showinfo("Sucesso", "Agenda salva com sucesso no banco.")
            
        except Exception as e:
            messagebox.showerror("Erro BD", f"Erro ao salvar agenda: {e}")
            if conn:
                conn.rollback()  # Desfaz a transação em caso de erro
        
        finally:
            if conn:
                conn.close()  # Garante que a conexão seja sempre fechada
                
    # ------------ COLETA DE MINÉRIOS (MOCHILA) ------------
    def _montar_coleta_minerios(self, parent):
        top = ttk.Frame(parent)
        top.pack(fill="both", expand=True, padx=8, pady=8)

        # --- Listbox com scrollbars (Amostras disponíveis) ---
        left = ttk.Frame(top)
        left.pack(side="left", fill="y", padx=(0, 8))
        ttk.Label(left, text="Amostras disponíveis na zona:").pack(anchor="w")

        self.lb_amostras = tk.Listbox(left, selectmode="extended", width=45, height=15)
        self.lb_amostras.pack(side="left", fill="both", expand=True)

        scroll_y = ttk.Scrollbar(left, orient="vertical", command=self.lb_amostras.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x = ttk.Scrollbar(left, orient="horizontal", command=self.lb_amostras.xview)
        scroll_x.pack(side="bottom", fill="x")
        self.lb_amostras.config(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        # --- Controles (Capacidade e Botão) ---
        mid = ttk.Frame(top)
        mid.pack(side="left", fill="y", padx=(0, 8))
        
        ttk.Label(mid, text="Capacidade da Mochila (kg):").pack(pady=(0, 4))
        self.capacidade_entry = ttk.Entry(mid, width=15)
        self.capacidade_entry.pack(pady=4)
        self.capacidade_entry.insert(0, "100.0") # Valor padrão

        ttk.Button(mid, text="Maximizar Coleta →", command=self.maximizar_coleta).pack(pady=12)

        # --- Treeview (Resultado da Coleta) ---
        right = ttk.Frame(top)
        right.pack(side="left", fill="both", expand=True)
        ttk.Label(right, text="Carga Coletada (Resultado):").pack(anchor="w")

        columns = ("id_amostra", "nome", "peso_coletado", "valor_coletado", "ratio")
        tree_frame = ttk.Frame(right)
        tree_frame.pack(fill="both", expand=True)

        self.tree_coleta = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        col_map = {
            "id_amostra": ("ID", 40),
            "nome": ("Nome Minério", 120),
            "peso_coletado": ("Peso Coletado", 90),
            "valor_coletado": ("Valor Coletado", 90),
            "ratio": ("Ratio (V/P)", 80)
        }
        for col, (head, width) in col_map.items():
            self.tree_coleta.heading(col, text=head)
            self.tree_coleta.column(col, width=width, anchor="center")

        scroll_y_tree = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_coleta.yview)
        scroll_x_tree = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree_coleta.xview)
        self.tree_coleta.configure(yscrollcommand=scroll_y_tree.set, xscrollcommand=scroll_x_tree.set)

        self.tree_coleta.grid(row=0, column=0, sticky="nsew")
        scroll_y_tree.grid(row=0, column=1, sticky="ns")
        scroll_x_tree.grid(row=1, column=0, sticky="ew")

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        # --- Botões inferiores ---
        bottom = ttk.Frame(parent)
        bottom.pack(fill="x", padx=8, pady=6)
        ttk.Button(bottom, text="Salvar Carga no BD", command=self.salvar_carga_bd).pack(side="left")
        ttk.Button(bottom, text="Recarregar Amostras", command=self.carregar_amostras_do_bd).pack(side="left", padx=6)
        ttk.Button(bottom, text="Voltar", command=self.parent.destroy).pack(side="right")
        
        # Cache inicial
        self._amostras_cache = {}

    def carregar_amostras_do_bd(self):
        try:
            conn = get_db_connection()
            cur = conn.cursor(dictionary=True)
            # Seleciona apenas amostras que ainda têm peso
            cur.execute("SELECT * FROM AmostrasMinerio WHERE peso_disponivel_kg > 0 ORDER BY nome_minerio")
            rows = cur.fetchall()
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro BD", f"Erro ao carregar amostras de minério: {e}")
            rows = []

        self.lb_amostras.delete(0, "end")
        self._amostras_cache = {}
        for r in rows:
            # Calcula ratio para exibição
            peso = float(r['peso_disponivel_kg'])
            valor = float(r['valor_total_disponivel'])
            ratio = (valor / peso) if peso > 0 else 0
            display = (f"[{r['id_amostra']}] {r['nome_minerio']} "
                       f"(P: {peso:.2f}kg, V: {valor:.2f}, R: {ratio:.2f})")
            self.lb_amostras.insert("end", display)
            # Armazena o registro completo no cache pelo ID
            self._amostras_cache[r['id_amostra']] = r 

    def maximizar_coleta(self):
        try:
            capacidade = float(self.capacidade_entry.get())
            if capacidade <= 0:
                raise ValueError("Capacidade deve ser positiva")
        except Exception:
            messagebox.showerror("Erro", "Capacidade da mochila inválida. Insira um número positivo.")
            return

        # O algoritmo roda em cima de *todas* as amostras disponíveis
        if not self._amostras_cache:
            messagebox.showinfo("Info", "Nenhuma amostra de minério carregada.")
            return

        # 1. Criar lista de candidatos (Itens) a partir do cache
        candidatos = []
        for r in self._amostras_cache.values():
            item = algoritmoGuloso.Item(
                nome=r['nome_minerio'],
                valor=float(r['valor_total_disponivel']),
                peso=float(r['peso_disponivel_kg'])
            )
            # Adiciona dados extras ao objeto Item para referência futura
            item.id_amostra = r['id_amostra']
            candidatos.append(item)
        
        # 2. Chamar o algoritmo guloso fracionário
        solucao_final = algoritmoGuloso.algoritmo_guloso_fracionario(candidatos, capacidade)

        # 3. Processar resultados e exibir no Treeview
        self.tree_coleta.delete(*self.tree_coleta.get_children())
        
        coletados_ids = set()
        total_valor_coletado = 0
        total_peso_coletado = 0

        for item, peso_coletado in solucao_final:
            # item.ratio foi calculado na criação do Item
            valor_proporcional = item.ratio * peso_coletado 
            total_valor_coletado += valor_proporcional
            total_peso_coletado += peso_coletado
            coletados_ids.add(item.id_amostra)

            self.tree_coleta.insert("", "end", values=(
                item.id_amostra,
                item.nome,
                f"{peso_coletado:.2f}",
                f"{valor_proporcional:.2f}",
                f"{item.ratio:.2f}"
            ))

        # 4. Preparar mensagem de feedback (incluindo excluídos)
        excluidos_nomes = [
            c.nome for c in candidatos if c.id_amostra not in coletados_ids
        ]
        
        msg = (f"Coleta otimizada concluída!\n\n"
               f"Capacidade da Mochila: {capacidade:.2f} kg\n"
               f"Peso Total Coletado: {total_peso_coletado:.2f} kg\n"
               f"Valor Total Coletado: {total_valor_coletado:.2f}\n")

        if excluidos_nomes:
            msg += "\nMinérios totalmente excluídos (sem espaço ou ratio baixo):\n- "
            msg += "\n- ".join(excluidos_nomes)
        
        messagebox.showinfo("Resultado da Coleta", msg)

    def salvar_carga_bd(self):
        cargas = []
        # Pega os dados do Treeview de resultado
        for iid in self.tree_coleta.get_children():
            vals = self.tree_coleta.item(iid, "values")
            try:
                id_amostra = int(vals[0])
                peso_coletado = float(vals[2])
                valor_coletado = float(vals[3])
                cargas.append((DEFAULT_EXPLORADOR_ID, id_amostra, peso_coletado, valor_coletado))
            except Exception as e:
                messagebox.showerror("Erro", f"Dados inválidos no resultado da coleta: {e}")
                return

        if not cargas:
            messagebox.showinfo("Info", "Nenhuma carga selecionada para salvar.")
            return

        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            # 1. Limpa a carga anterior deste explorador (consistente com as outras abas)
            sql_delete = "DELETE FROM CargaExplorador WHERE id_explorador = %s"
            cur.execute(sql_delete, (DEFAULT_EXPLORADOR_ID,))

            # 2. Insere a nova carga
            sql_insert = """
                INSERT INTO CargaExplorador 
                (id_explorador, id_amostra_coletada, peso_coletado_kg, valor_proporcional_coletado)
                VALUES (%s, %s, %s, %s)
            """
            # Usa executemany para inserir todos os registros de uma vez
            cur.executemany(sql_insert, cargas)
            
            conn.commit()
            cur.close()
            messagebox.showinfo("Sucesso", 
                                f"{len(cargas)} registros de carga salvos com sucesso na tabela CargaExplorador.")

        except Exception as e:
            messagebox.showerror("Erro BD", f"Erro ao salvar carga: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    # ------------ ESCALONAMENTO POR RECOMPENSA ------------
    def _montar_escalonamento_recompensa(self, parent):
        top = ttk.Frame(parent)
        top.pack(fill="both", expand=True, padx=8, pady=8)

        # --- Listbox com scrollbars ---
        left = ttk.Frame(top)
        left.pack(side="left", fill="y", padx=(0, 8))
        ttk.Label(left, text="Missões disponíveis:").pack(anchor="w")

        self.lb_missoes_recomp = tk.Listbox(left, selectmode="extended", width=40, height=15)
        self.lb_missoes_recomp.pack(side="left", fill="both", expand=True)

        scroll_y = ttk.Scrollbar(left, orient="vertical", command=self.lb_missoes_recomp.yview)
        scroll_y.pack(side="right", fill="y")

        scroll_x = ttk.Scrollbar(left, orient="horizontal", command=self.lb_missoes_recomp.xview)
        scroll_x.pack(side="bottom", fill="x")

        self.lb_missoes_recomp.config(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        # --- Botões ---
        mid = ttk.Frame(top)
        mid.pack(side="left", fill="y", padx=(0, 8))
        ttk.Button(mid, text="Adicionar →", command=self.adicionar_missoes_recomp).pack(pady=6)
        ttk.Button(mid, text="Remover selecionadas", command=self.remover_missoes_recomp).pack(pady=6)
        ttk.Button(mid, text="Escalonar (Max Recompensa)", command=self.escalonar_recompensa).pack(pady=12)

        # --- Treeview ---
        right = ttk.Frame(top)
        right.pack(side="left", fill="both", expand=True)
        ttk.Label(right, text="Resultado do Escalonamento:").pack(anchor="w")

        columns = ("id_missao", "nome", "planeta", "data", "inicio", "fim", "recompensa")
        self.tree_recomp = ttk.Treeview(right, columns=columns, show="headings", height=15)
        for col, head in zip(columns, ("ID", "Nome", "Planeta", "Data", "Início", "Fim", "Recompensa")):
            self.tree_recomp.heading(col, text=head)
            self.tree_recomp.column(col, width=90, anchor="center")
        self.tree_recomp.pack(fill="both", expand=True)

        # --- Botões inferiores ---
        bottom = ttk.Frame(parent)
        bottom.pack(fill="x", padx=8, pady=6)
        ttk.Button(bottom, text="Salvar agenda otimizada no BD", command=self.salvar_agenda_recompensa).pack(side="left")
        ttk.Button(bottom, text="Recarregar missões", command=self.carregar_missoes_do_bd_recomp).pack(side="left", padx=6)
        ttk.Button(bottom, text="Voltar", command=self.parent.destroy).pack(side="right")

        # Cache inicial
        self._missoes_cache_recomp = {}
        
    def carregar_missoes_do_bd_recomp(self):
        try:
            conn = get_db_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM MissoesExploracao ORDER BY data_missao, tempo_inicio")
            rows = cur.fetchall()
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro BD", f"Erro ao carregar missões: {e}")
            rows = []

        self.lb_missoes_recomp.delete(0, "end")
        self._missoes_cache_recomp = {}
        for r in rows:
            display = f"[{r['id_missao']}] {r['nome_missao']} | {r['planeta_alvo']} | {r['data_missao']} ({r['tempo_inicio']}-{r['tempo_fim']})"
            self.lb_missoes_recomp.insert("end", display)
            self._missoes_cache_recomp[display] = r

    def adicionar_missoes_recomp(self):
        selections = [self.lb_missoes_recomp.get(i) for i in self.lb_missoes_recomp.curselection()]
        if not selections:
            messagebox.showinfo("Info", "Nenhuma missão selecionada.")
            return
        for disp in selections:
            r = self._missoes_cache_recomp.get(disp)
            if not r:
                continue
            iid = f"r_{r['id_missao']}"
            if iid in self.tree_recomp.get_children():
                continue
            self.tree_recomp.insert("", "end", iid=iid, values=(
                r["id_missao"],
                r["nome_missao"],
                r["planeta_alvo"],
                r["data_missao"],
                r["tempo_inicio"],
                r["tempo_fim"],
                float(r.get("recompensa_valor") or 0),
            ))

    def remover_missoes_recomp(self):
        for iid in self.tree_recomp.selection():
            self.tree_recomp.delete(iid)

    def escalonar_recompensa(self):
        items = []
        for iid in self.tree_recomp.get_children():
            vals = self.tree_recomp.item(iid, "values")
            item = {
                "id_missao": int(vals[0]),
                "nome_missao": vals[1],
                "planeta_alvo": vals[2],
                "data_missao": vals[3],
                "tempo_inicio": int(vals[4]),
                "tempo_fim": int(vals[5]),
                "recompensa_valor": float(vals[6]),
            }
            items.append(item)

        if not items:
            messagebox.showinfo("Info", "Nenhuma missão para escalonar.")
            return

        # Converter para Intervalos
        intervalos = [
            Intervalo(
                id_missao=m["id_missao"],
                inicio=m["tempo_inicio"],
                fim=m["tempo_fim"],
                valor=m["recompensa_valor"]
            )
            for m in items
        ]

        valor_total, escolhidas = calcular_escalonamento_dp(intervalos)
        escolhidas_ids = {m.id_missao for m in escolhidas}

        # determinar removidas
        removidas = [m["nome_missao"] for m in items if m["id_missao"] not in escolhidas_ids]

        # atualizar treeview
        for iid in self.tree_recomp.get_children():
            self.tree_recomp.delete(iid)
        for r in escolhidas:
            missao = next(m for m in items if m["id_missao"] == r.id_missao)
            iid = f"r_{missao['id_missao']}"
            self.tree_recomp.insert("", "end", iid=iid, values=(
                missao["id_missao"],
                missao["nome_missao"],
                missao["planeta_alvo"],
                missao["data_missao"],
                missao["tempo_inicio"],
                missao["tempo_fim"],
                missao["recompensa_valor"],
            ))

        msg = f"Escalonamento concluído!\nRecompensa total = {valor_total:.2f}"
        if removidas:
            msg += "\n\nMissões removidas:\n- " + "\n- ".join(removidas)
        messagebox.showinfo("Resultado", msg)

    def salvar_agenda_recompensa(self):
        ids = []
        for iid in self.tree_recomp.get_children():
            vals = self.tree_recomp.item(iid, "values")
            ids.append((int(vals[0]), vals[3]))

        if not ids:
            messagebox.showinfo("Info", "Nenhuma missão para salvar na agenda.")
            return

        conn = None  # Inicializa a conexão como None
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            # --- INÍCIO DA MODIFICAÇÃO (OPÇÃO A) ---
            # 1. Limpa a agenda anterior deste explorador
            sql_delete = "DELETE FROM AgendaExplorador WHERE id_explorador = %s"
            cur.execute(sql_delete, (DEFAULT_EXPLORADOR_ID,))
            # --- FIM DA MODIFICAÇÃO ---

            # 2. Insere a nova agenda
            sql_insert = """
                INSERT INTO AgendaExplorador (id_explorador, id_missao_selecionada, data_agendamento)
                VALUES (%s, %s, %s)
            """
            for id_missao, data_missao in ids:
                cur.execute(sql_insert, (DEFAULT_EXPLORADOR_ID, id_missao, data_missao))
            
            conn.commit()  # Efetiva o DELETE e os INSERTs juntos
            cur.close()
            messagebox.showinfo("Sucesso", "Agenda otimizada salva com sucesso no banco.")

        except Exception as e:
            messagebox.showerror("Erro BD", f"Erro ao salvar agenda: {e}")
            if conn:
                conn.rollback()  # Desfaz a transação em caso de erro

        finally:
            if conn:
                conn.close()  # Garante que a conexão seja sempre fechada

