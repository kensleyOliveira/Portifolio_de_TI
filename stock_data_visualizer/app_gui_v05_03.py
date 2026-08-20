import os
import sys
import threading
import subprocess
import queue
import traceback
import re
from datetime import datetime

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from pathlib import Path
from PIL import Image, ImageTk
from PIL.ImageTk import PhotoImage
from typing import List, Any, Dict

# optional theme
try:
    import ttkbootstrap as tb
    from ttkbootstrap.constants import SUCCESS, TOP, INFO
except Exception:
    tb = None

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
# Correção: Importar a barra de ferramentas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.widgets import RectangleSelector
import seaborn as sns

# SQLAlchemy
from sqlalchemy import create_engine, text, bindparam
from sqlalchemy.engine import Engine

# pdf->image optional
try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except Exception:
    PDF2IMAGE_AVAILABLE = False

# colored logs
try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init(autoreset=True)
except Exception:
    class _C:
        def __getattr__(self, name): return ""
    Fore = Style = _C()

# ---------------- Configuration (edit here) ----------------
DB_USER = "root"
DB_PASS = "mysql"
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "b3dw"

COMMON_POPPLER_PATHS = [r"C:\poppler\poppler-25.07.0\Library\bin"]
SCRIPT_NAME = "Analise_risco_ativo_v3.py"
RELATORIOS_DIR = "./relatorios"
DEFAULT_THEME = "superhero"
PROG_RE = re.compile(r"PROGRESS:\s*(\d{1,3})%?(?:\s*-\s*(.*))?")

# ---------------- Helpers ----------------
def log_info(msg):
    print(Fore.BLUE + "[INFO] " + Style.RESET_ALL + msg)

def log_ok(msg):
    print(Fore.GREEN + "[OK] " + Style.RESET_ALL + msg)

def log_warn(msg):
    print(Fore.YELLOW + "[WARN] " + Style.RESET_ALL + msg)

def log_err(msg):
    print(Fore.RED + "[ERROR] " + Style.RESET_ALL + msg)

def ensure_rel_dir(path=RELATORIOS_DIR):
    os.makedirs(path, exist_ok=True)
    return os.path.abspath(path)

def human_pct(x):
    if pd.isna(x):
        return "NA"
    return f"{x:.2%}"

# ---------------- Metrics & Portfolios ----------------
def calc_metrics(returns: pd.DataFrame) -> pd.DataFrame:
    metrics = []
    ann_factor = 252
    for col in returns.columns:
        r = pd.to_numeric(returns[col], errors='coerce').dropna()
        if len(r) == 0:
            continue
        ann_ret = (1 + r).prod() ** (ann_factor / len(r)) - 1
        ann_vol = r.std(ddof=0) * np.sqrt(ann_factor)
        sharpe = ann_ret / ann_vol if ann_vol > 0 else np.nan
        cum = (1 + r).cumprod() - 1
        drawdown = (cum - cum.cummax()).min() if not cum.empty else np.nan
        metrics.append({
            "ticker": col, "ann_return": ann_ret, "ann_vol": ann_vol,
            "sharpe": sharpe, "max_drawdown": drawdown,
            "cum_return": cum.iloc[-1] if not cum.empty else np.nan, "n_obs": len(r)
        })
    return pd.DataFrame(metrics)

def compute_portfolio_summaries(returns_df: pd.DataFrame):
    ann = 252
    n = len(returns_df.columns)
    if n == 0:
        return "Nenhum ativo disponível para sugerir carteiras."
    mean_ret = returns_df.mean() * ann
    cov = returns_df.cov() * ann
    lines = []
    try:
        w_eq = np.repeat(1/n, n)
        ret_eq = float(np.dot(w_eq, mean_ret))
        vol_eq = float(np.sqrt(np.dot(w_eq.T, np.dot(cov, w_eq))))
        sr_eq = ret_eq/vol_eq if vol_eq>0 else np.nan
        lines.append(("Balanceada (Equal Weight)", ret_eq, vol_eq, sr_eq, w_eq))
    except Exception: pass
    try:
        inv_cov = np.linalg.inv(cov.values)
        ones = np.ones(n)
        w_min = inv_cov.dot(ones) / (ones.dot(inv_cov).dot(ones))
        ret_min = float(np.dot(w_min, mean_ret))
        vol_min = float(np.sqrt(np.dot(w_min.T, np.dot(cov.values, w_min))))
        sr_min = ret_min/vol_min if vol_min>0 else np.nan
        lines.insert(0, ("Conservadora (Min Vol)", ret_min, vol_min, sr_min, w_min))
    except Exception:
        if lines:
            lines.insert(0, ("Conservadora (Equal Weight fallback)", lines[0][1], lines[0][2], lines[0][3], lines[0][4]))
    try:
        best_sr = -1e9; best_w = None
        for _ in range(2000):
            w = np.random.random(n); w /= w.sum()
            r = float(np.dot(w, mean_ret)); v = float(np.sqrt(np.dot(w.T, np.dot(cov.values, w))))
            sr = r/v if v>0 else -1e9
            if sr > best_sr:
                best_sr = sr; best_w = w
        if best_w is not None:
            r = float(np.dot(best_w, mean_ret)); v = float(np.sqrt(np.dot(best_w.T, np.dot(cov.values, best_w))))
            lines.append(("Agressiva (Max Sharpe aprox.)", r, v, r/v if v>0 else np.nan, best_w))
    except Exception: pass
    txt = []
    for name, r, v, sr, w in lines:
        txt.append(f"{name}:")
        txt.append(f"  - Retorno anual esperado: {human_pct(r)}")
        txt.append(f"  - Volatilidade anual:     {human_pct(v)}")
        txt.append(f"  - Sharpe (aprox):         {sr:.3f}" if not pd.isna(sr) else "  - Sharpe (aprox): NA")
        try:
            weight_series = pd.Series(w, index=returns_df.columns).sort_values(ascending=False)
            top5 = weight_series.head(5)
            txt.append("  - Principais pesos: " + ", ".join([f"{idx} {human_pct(val)}" for idx,val in top5.items()]))
        except Exception: pass
        txt.append("")
    txt.append("Observação: Retornos e volatilidades são anualizados (252 dias).")
    return "\n".join(txt)

# ---------------- GUI Class ----------------
class B3DashboardV5FixSQL:
    def __init__(self, root):
        self.root = root
        self.root.title("B3 DW Dashboard - v5 (Toolbar Completo)")
        self.root.geometry("1360x880")
        if tb:
            try:
                tb.Style(theme=DEFAULT_THEME)
            except Exception:
                pass

        self.engine: Engine | None = None
        self._connect_db()
        self.proc = None
        self.thread = None
        self.queue = queue.Queue()
        self.stop_event = threading.Event()
        self.pdf_viewer = None
        self._build_ui()
        self._poll_queue()

    def _connect_db(self):
        try:
            db_url = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            self.engine = create_engine(db_url, pool_pre_ping=True)
            log_ok("SQLAlchemy engine created.")
        except Exception as e:
            self.engine = None
            log_err(f"Failed to create engine: {e}")

    def _build_ui(self):
        main_pane = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(main_pane, width=400)
        main_pane.add(left_frame, weight=1)
        right_frame = ttk.Frame(main_pane)
        main_pane.add(right_frame, weight=4)

        ctrl = ttk.LabelFrame(left_frame, text="Controles")
        ctrl.pack(fill=tk.X, padx=8, pady=6)
        ttk.Label(ctrl, text="Tickers:").grid(row=0, column=0, sticky=tk.W, padx=6)
        self.ticker_listbox = tk.Listbox(ctrl, width=28, height=12, selectmode=tk.EXTENDED, exportselection=False)
        self.ticker_listbox.grid(row=1, column=0, rowspan=6, padx=6, pady=2, sticky=tk.N)
        self.ticker_scroll = ttk.Scrollbar(ctrl, orient=tk.VERTICAL, command=self.ticker_listbox.yview)
        self.ticker_listbox.config(yscrollcommand=self.ticker_scroll.set)
        self.ticker_scroll.grid(row=1, column=1, rowspan=6, sticky="ns", pady=2)

        ttk.Label(ctrl, text="Métrica/View:").grid(row=0, column=2, sticky=tk.W, padx=6)
        metrics = ["v_returns","v_vol_21d","v_dashboard","v_drawdown","v_heatmap_returns","v_asset_returns","v_cum_returns","v_splits"]
        self.metric_combo = ttk.Combobox(ctrl, values=metrics, state="readonly", width=22); self.metric_combo.current(0)
        self.metric_combo.grid(row=1, column=2, padx=6, pady=2, sticky=tk.W)

        ttk.Label(ctrl, text="Data Início (YYYY-MM-DD):").grid(row=2, column=2, sticky=tk.W, padx=6)
        self.start_entry = ttk.Entry(ctrl, width=14); self.start_entry.insert(0, "2010-01-01"); self.start_entry.grid(row=3, column=2, sticky=tk.W, padx=6)
        ttk.Label(ctrl, text="Data Fim (YYYY-MM-DD):").grid(row=4, column=2, sticky=tk.W, padx=6)
        self.end_entry = ttk.Entry(ctrl, width=14); self.end_entry.insert(0, "2025-12-31"); self.end_entry.grid(row=5, column=2, sticky=tk.W, padx=6)

        btn_frame = ttk.Frame(left_frame); btn_frame.pack(fill=tk.X, padx=8, pady=(6,4))
        ttk.Button(btn_frame, text="Plotar (único)", command=self.on_plot_single).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Comparar (multi)", command=self.on_compare).pack(side=tk.LEFT, padx=4)

        btn_frame2 = ttk.Frame(left_frame); btn_frame2.pack(fill=tk.X, padx=8)
        ttk.Button(btn_frame2, text="Refresh Tickers", command=self.reload_tickers).pack(side=tk.LEFT, padx=4)
        # CORREÇÃO 2: Botão agora chama a nova função que gera PDF para seleção
        ttk.Button(btn_frame2, text="Gerar PDF Legível", command=self.generate_pdf_for_selection).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame2, text="👁 Visualizar PDF", command=self.open_pdf_viewer).pack(side=tk.LEFT, padx=4)

        # FUNCIONALIDADE RESTAURADA: Botões de análise
        action_frame = ttk.Frame(left_frame); action_frame.pack(fill=tk.X, padx=8, pady=(6,6))
        ttk.Button(action_frame, text="📊 Rodar Análise (selecionados)", command=self.run_analysis_selected).pack(fill=tk.X, pady=2)
        ttk.Button(action_frame, text="📊 Rodar Análise (todos)", command=self.run_analysis_all).pack(fill=tk.X, pady=2)
        ttk.Button(action_frame, text="⏹ Parar Análise", command=self.stop_analysis).pack(fill=tk.X, pady=2)

        # FUNCIONALIDADE RESTAURADA: Progresso e Log
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=8, pady=8)
        ttk.Label(left_frame, text="Progresso:").pack(anchor=tk.W, padx=8)
        self.progress = ttk.Progressbar(left_frame, orient="horizontal", length=200, mode="determinate"); self.progress.pack(fill=tk.X, padx=8, pady=(0,8))
        ttk.Label(left_frame, text="Log (Análise):").pack(anchor=tk.W, padx=8); self.log_txt = ScrolledText(left_frame, height=10); self.log_txt.pack(fill=tk.BOTH, expand=False, padx=8, pady=(4,8))

        plot_frame = ttk.Frame(right_frame)
        plot_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        
        self.fig = Figure(figsize=(9, 6), dpi=120)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        
        toolbar = NavigationToolbar2Tk(self.canvas, plot_frame)
        toolbar.update()
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        bottom_nb = ttk.Notebook(right_frame, height=260); bottom_nb.pack(fill=tk.BOTH, expand=False, padx=6, pady=(0,6))
        tab_table = ttk.Frame(bottom_nb); bottom_nb.add(tab_table, text="Tabela / Resultados")
        table_frame = ttk.Frame(tab_table); table_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        cols = ("ticker","ann_return","ann_vol","sharpe","max_drawdown","cum_return","n_obs")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c); self.tree.column(c, width=130, anchor=tk.CENTER)
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1); table_frame.columnconfigure(0, weight=1)

        tab_port = ttk.Frame(bottom_nb); bottom_nb.add(tab_port, text="Carteiras sugeridas")
        self.port_txt = ScrolledText(tab_port, height=10); self.port_txt.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        self.status = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W); self.status.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.reload_tickers(initial=True)

    def set_status(self, txt):
        self.status.config(text=txt); self.root.update_idletasks()
        
    def _prepare_dataframe_for_plotting(self, df: pd.DataFrame) -> pd.DataFrame:
        if df is None or df.empty:
            return df
        date_cols = {'date_id', 'ex_date'}
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        return df

    def _fetch_metric_df_for_ticker(self, metric, ticker, start_date, end_date):
        if self.engine is None: raise RuntimeError("DB engine not available")
        no_date_filter = {"v_heatmap_returns", "v_asset_returns"}
        if metric == "v_splits":
            q = text("SELECT * FROM v_splits WHERE ticker = :ticker AND ex_date BETWEEN :start AND :end ORDER BY ex_date")
            params = {"ticker": ticker, "start": start_date, "end": end_date}
        elif metric not in no_date_filter:
            q = text(f"SELECT * FROM {metric} WHERE ticker = :ticker AND date_id BETWEEN :start AND :end ORDER BY date_id")
            params = {"ticker": ticker, "start": start_date, "end": end_date}
        else:
            q = text(f"SELECT * FROM {metric} WHERE ticker = :ticker")
            params = {"ticker": ticker}
        df = pd.read_sql(q, self.engine, params=params)
        return self._prepare_dataframe_for_plotting(df)

    def load_tickers_from_db(self):
        if self.engine is None:
            log_warn("No DB engine available"); return []
        try:
            q = text("SELECT DISTINCT ticker FROM dim_asset ORDER BY ticker")
            return pd.read_sql(q, self.engine)['ticker'].tolist()
        except Exception as e:
            log_err(f"Failed to load tickers: {e}"); return []

    def reload_tickers(self, initial=False):
        self.ticker_listbox.delete(0, tk.END)
        for t in self.load_tickers_from_db():
            self.ticker_listbox.insert(tk.END, t)
        self.ax.clear()
        self.ax.text(0.5, 0.5, "Selecione e clique em Plotar/Comparar", ha="center", va="center")
        self.canvas.draw()
        for i in self.tree.get_children(): self.tree.delete(i)
        self.port_txt.delete(1.0, tk.END)
        if not initial:
            self.log_txt.delete(1.0, tk.END)
            self.log_txt.insert(tk.END, f"{datetime.now().isoformat()} - Tickers recarregados.\n")
        self.set_status("Tickers recarregados")
        log_info("Tickers reloaded")

    def on_plot_single(self):
        sel = self.ticker_listbox.curselection()
        if not sel:
            messagebox.showinfo("Info", "Selecione um ticker."); return
        ticker = self.ticker_listbox.get(sel[0])
        metric = self.metric_combo.get()
        start_date = self.start_entry.get().strip()
        end_date = self.end_entry.get().strip()
        self._open_plot_window(ticker, metric, start_date, end_date)

    def _open_plot_window(self, ticker, metric, start_date, end_date):
        top = tk.Toplevel(self.root)
        top.title(f"{ticker} - {metric}")
        top.geometry("1000x720")
        
        fig = Figure(figsize=(9, 6), dpi=120)
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=top)

        toolbar_frame = ttk.Frame(top)
        toolbar_frame.pack(side=tk.TOP, fill=tk.X, padx=6, pady=(0,6))
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        try:
            df = self._fetch_metric_df_for_ticker(metric, ticker, start_date, end_date)
            if df is None or df.empty:
                ax.text(0.5, 0.5, "Nenhum dado encontrado", ha="center", va="center")
            else:
                self._plot_on_axes(ax, fig, df, metric, ticker_label=ticker, legend_below=True)
            
            fig.tight_layout()
            canvas.draw()
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Erro SQL", f"Falha na query: {e}")
            top.destroy()

    def on_compare(self):
        sel = self.ticker_listbox.curselection()
        if not sel:
            messagebox.showinfo("Info", "Selecione pelo menos um ticker."); return
        tickers = [self.ticker_listbox.get(i) for i in sel]
        start_date, end_date = self.start_entry.get().strip(), self.end_entry.get().strip()

        q = text("""
            SELECT a.ticker, fp.date_id, fp.adj_close
            FROM fact_price fp JOIN dim_asset a ON a.asset_id = fp.asset_id
            WHERE a.ticker IN :tickers AND fp.date_id BETWEEN :start AND :end
            ORDER BY a.ticker, fp.date_id
        """).bindparams(bindparam("tickers", expanding=True), bindparam("start"), bindparam("end"))
        
        try:
            df_prices = pd.read_sql_query(q, self.engine, params={"tickers": tickers, "start": start_date, "end": end_date})
        except Exception as e:
            messagebox.showerror("Erro SQL", f"Falha ao buscar preços: {e}"); return

        if df_prices.empty:
            messagebox.showinfo("Info", "Nenhum preço retornado."); return

        wide = df_prices.pivot(index="date_id", columns="ticker", values="adj_close").sort_index()
        daily_r = wide.pct_change().fillna(0)
        cum = (1 + daily_r).cumprod() - 1
        cum.index = pd.to_datetime(cum.index)

        self.ax.clear()
        for t in tickers:
            if t in cum.columns:
                self.ax.plot(cum.index, cum[t], label=t)
        
        self.ax.set_title("Retorno Acumulado (comparação)")
        self.fig.autofmt_xdate(rotation=45)
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.set_xlabel("Data") # Adiciona título ao eixo X

        # CORREÇÃO 1: Ajusta a posição da legenda para ficar abaixo do título do eixo X
        handles, labels = self.ax.get_legend_handles_labels()
        if handles:
            ncol = min(6, max(1, len(handles)))
            # Ancora a parte de cima ('upper center') da legenda abaixo do eixo
            self.ax.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.25), ncol=ncol)
            # Ajusta o espaçamento inferior da figura para a legenda não ser cortada
            self.fig.subplots_adjust(bottom=0.3)
        
        self.canvas.draw()
        
        metrics_df = calc_metrics(daily_r)
        for i in self.tree.get_children(): self.tree.delete(i)
        for _, row in metrics_df.iterrows():
            self.tree.insert("", tk.END, values=(
                row["ticker"], f"{row['ann_return']:.2%}", f"{row['ann_vol']:.2%}",
                f"{row['sharpe']:.2f}", f"{row['max_drawdown']:.2%}",
                f"{row['cum_return']:.2%}", row["n_obs"]
            ))
        self.port_txt.delete(1.0, tk.END)
        self.port_txt.insert(tk.END, compute_portfolio_summaries(daily_r))

    def _plot_on_axes(self, ax, fig, df, metric, ticker_label=None, legend_below=False):
        ax.clear()
        is_date_plot = False
        date_col = 'date_id'
        
        if metric == "v_returns":
            ax.plot(df['date_id'], df['ret_simple'], label="Retorno Simples")
            is_date_plot = True
        elif metric == "v_vol_21d":
            ax.plot(df['date_id'], df['vol_21d'], label="Vol 21d")
            is_date_plot = True
        elif metric == "v_dashboard":
            ax.plot(df['date_id'], df['adj_close'], label="Preço Ajustado")
            ax2 = ax.twinx()
            ax2.plot(df['date_id'], df['vol_21d'], linestyle='--', color='orange', label="Vol 21d (R)")
            is_date_plot = True
        elif metric == "v_drawdown":
            ax.plot(df['date_id'], df['drawdown'], label="Drawdown")
            is_date_plot = True
        elif metric == "v_cum_returns":
            ax.plot(df['date_id'], df['cum_return'], label="Retorno Acumulado")
            is_date_plot = True
        elif metric == "v_splits":
            if not df['ex_date'].isnull().all():
                ax.scatter(df['ex_date'], [1]*len(df), marker='v')
            date_col = 'ex_date'
            is_date_plot = True
        elif metric == "v_heatmap_returns":
            pivot = df.pivot_table(index='year', columns='month', values='monthly_return')
            sns.heatmap(pivot, annot=True, fmt=".2%", cmap="RdYlGn", ax=ax)

        ax.set_title(f"{ticker_label} - {metric}" if ticker_label else metric)
        ax.legend(loc='best')
        ax.grid(True, linestyle='--', alpha=0.6)

        if is_date_plot:
            ax.set_xlabel("Data") # Adiciona título ao eixo X
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            fig.autofmt_xdate(rotation=45)
        
        # CORREÇÃO 1: Lógica de legenda para janela de plot único (que usa legend_below=True)
        # Usa fig.legend para lidar com eixos duplos (twinx) e posicionar abaixo do eixo X
        if legend_below:
            all_handles, all_labels = [], []
            for current_ax in fig.axes:
                handles, labels = current_ax.get_legend_handles_labels()
                all_handles.extend(handles)
                all_labels.extend(labels)
                if current_ax.get_legend():
                    current_ax.get_legend().remove() # Remove legendas individuais
            
            if all_handles:
                ncol = min(4, len(all_handles))
                # Cria uma legenda única para a figura, posicionada na parte de baixo
                fig.legend(all_handles, all_labels, loc='upper center', bbox_to_anchor=(0.5, 0.15), ncol=ncol)
                fig.subplots_adjust(bottom=0.3) # Ajusta o espaço inferior

    # --- FUNCIONALIDADES DE ANÁLISE RESTAURADAS ---
    def run_analysis_selected(self):
        sel = self.ticker_listbox.curselection()
        if not sel:
            messagebox.showinfo("Info", "Selecione tickers ou use 'Rodar Análise (todos)'."); return
        self._start_subprocess([self.ticker_listbox.get(i) for i in sel])

    def run_analysis_all(self):
        self._start_subprocess([])

    def _start_subprocess(self, tickers):
        if self.proc is not None and self.proc.poll() is None:
            messagebox.showinfo("Info", "Análise já em execução."); return
        script_path = os.path.join(os.path.dirname(__file__), SCRIPT_NAME)
        if not os.path.isfile(script_path):
            messagebox.showerror("Erro", f"Arquivo não encontrado: {script_path}"); return
        cmd = [sys.executable, script_path, "--outdir", RELATORIOS_DIR] + tickers
        try:
            self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True, creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao iniciar análise: {e}"); return
        self.stop_event.clear(); self.progress['value'] = 0; self.log_txt.delete(1.0, tk.END)
        self.set_status("Análise em execução...")
        self.thread = threading.Thread(target=self._read_output_thread, daemon=True); self.thread.start()
        log_info(f"Started analysis: {' '.join(cmd)}")

    def _read_output_thread(self):
        if self.proc and self.proc.stdout:
            for line in self.proc.stdout:
                if line: self.queue.put(line.rstrip("\n"))
                if self.stop_event.is_set(): break
        self.queue.put(f"=== PROCESSO FINALIZADO (exit code {self.proc.wait() if self.proc else 'N/A'}) ===")

    def stop_analysis(self):
        if self.proc is None or self.proc.poll() is not None:
            messagebox.showinfo("Info", "Nenhum processo em execução."); return
        self.stop_event.set()
        try:
            self.proc.terminate()
            self.proc.wait(timeout=5)
        except Exception:
            self.proc.kill()
        self.queue.put("=== PROCESSO INTERROMPIDO PELO USUÁRIO ===")
        log_warn("Analysis terminated by user")

    def _poll_queue(self):
        try:
            while True: self._handle_line(self.queue.get_nowait())
        except queue.Empty: pass
        self.root.after(200, self._poll_queue)

    def _handle_line(self, line):
        self.log_txt.insert(tk.END, line + "\n"); self.log_txt.see(tk.END)
        m = PROG_RE.search(line)
        if m:
            pct, msg = int(m.group(1)), m.group(2) or ""
            self.progress['value'] = pct
            self.set_status(f"Análise: {pct}% - {msg}")
            if pct >= 100:
                messagebox.showinfo("Concluído", "Análise concluída com sucesso!")
                self._post_analysis_refresh()

    def _post_analysis_refresh(self):
        self.reload_tickers()
        excel_path = os.path.join(RELATORIOS_DIR, "analise_risco_todos_tickers.xlsx")
        if os.path.isfile(excel_path):
            try:
                self._populate_table_from_results(pd.read_excel(excel_path))
            except Exception as e:
                log_err(f"Falha ao ler Excel de resultados: {e}")

    def _populate_table_from_results(self, df):
        if df is None or df.empty: return
        self.tree.delete(*self.tree.get_children())
        df.columns = [c.lower() for c in df.columns]
        rename_map = {'ativo': 'ticker', 'retorno anual (%)': 'ann_return', 'volatilidade anual (%)': 'ann_vol'}
        df.rename(columns=rename_map, inplace=True)
        
        for _, row in df.head(100).iterrows():
            self.tree.insert("", tk.END, values=(
                row.get('ticker', ''), f"{row.get('ann_return', 0):.2%}", 
                f"{row.get('ann_vol', 0):.2%}", "", "", "", ""
            ))
            
    # CORREÇÃO 2: Função que gera PDF para os tickers selecionados
    def generate_pdf_for_selection(self):
        sel_indices = self.ticker_listbox.curselection()
        if not sel_indices:
            messagebox.showinfo("Info", "Selecione um ou mais tickers para gerar o relatório.")
            return
        tickers = [self.ticker_listbox.get(i) for i in sel_indices]
        start_date = self.start_entry.get().strip()
        end_date = self.end_entry.get().strip()

        rel_dir = ensure_rel_dir()
        default_filename = f"relatorio_{'_'.join(tickers[:3])}_{datetime.now():%Y%m%d}.pdf"
        pdf_path = filedialog.asksaveasfilename(
            title="Salvar Relatório PDF",
            initialdir=rel_dir,
            initialfile=default_filename,
            filetypes=[("PDF Files", "*.pdf")],
            defaultextension=".pdf"
        )
        if not pdf_path:
            return

        self.set_status(f"Gerando PDF para {len(tickers)} tickers...")
        try:
            with PdfPages(pdf_path) as pdf:
                # --- Página 1: Comparação de Retorno Acumulado ---
                self.set_status("Gerando gráfico de retorno acumulado...")
                q = text("""
                    SELECT a.ticker, fp.date_id, fp.adj_close
                    FROM fact_price fp JOIN dim_asset a ON a.asset_id = fp.asset_id
                    WHERE a.ticker IN :tickers AND fp.date_id BETWEEN :start AND :end
                    ORDER BY a.ticker, fp.date_id
                """).bindparams(bindparam("tickers", expanding=True), bindparam("start"), bindparam("end"))
                
                df_prices = pd.read_sql_query(q, self.engine, params={"tickers": tickers, "start": start_date, "end": end_date})
                
                if not df_prices.empty:
                    wide = df_prices.pivot(index="date_id", columns="ticker", values="adj_close").sort_index()
                    daily_r = wide.pct_change().fillna(0)
                    cum = (1 + daily_r).cumprod() - 1
                    cum.index = pd.to_datetime(cum.index)

                    fig_cum = Figure(figsize=(10, 7.5))
                    ax_cum = fig_cum.add_subplot(111)
                    cum.plot(ax=ax_cum)
                    
                    ax_cum.set_title("Comparação de Retorno Acumulado")
                    ax_cum.set_xlabel("Data")
                    ax_cum.set_ylabel("Retorno Acumulado")
                    ax_cum.grid(True, linestyle='--', alpha=0.6)
                    fig_cum.autofmt_xdate(rotation=30)
                    ax_cum.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
                    
                    handles, labels = ax_cum.get_legend_handles_labels()
                    if handles:
                        ncol = min(5, len(handles))
                        ax_cum.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=ncol)
                        fig_cum.subplots_adjust(bottom=0.25)
                    
                    pdf.savefig(fig_cum)
                    plt.close(fig_cum)

                # --- Páginas seguintes: Dashboards Individuais ---
                for i, ticker in enumerate(tickers):
                    self.set_status(f"Gerando dashboard para {ticker} ({i+1}/{len(tickers)})...")
                    try:
                        fig_ind = Figure(figsize=(10, 7.5))
                        fig_ind.suptitle(f"Dashboard: {ticker}", fontsize=16)

                        # Gráfico 1: Preço e Vol
                        ax1 = fig_ind.add_subplot(2, 2, 1)
                        df_dash = self._fetch_metric_df_for_ticker("v_dashboard", ticker, start_date, end_date)
                        self._plot_on_axes(ax1, fig_ind, df_dash, "v_dashboard", ticker_label=f"{ticker} - Preço e Vol", legend_below=False)

                        # Gráfico 2: Retornos
                        ax2 = fig_ind.add_subplot(2, 2, 2)
                        df_ret = self._fetch_metric_df_for_ticker("v_returns", ticker, start_date, end_date)
                        self._plot_on_axes(ax2, fig_ind, df_ret, "v_returns", ticker_label=f"{ticker} - Retornos", legend_below=False)
                        if ax2.get_legend(): ax2.get_legend().remove()

                        # Gráfico 3: Drawdown
                        ax3 = fig_ind.add_subplot(2, 2, 3)
                        df_dd = self._fetch_metric_df_for_ticker("v_drawdown", ticker, start_date, end_date)
                        self._plot_on_axes(ax3, fig_ind, df_dd, "v_drawdown", ticker_label=f"{ticker} - Drawdown", legend_below=False)
                        if ax3.get_legend(): ax3.get_legend().remove()

                        # Gráfico 4: Heatmap
                        ax4 = fig_ind.add_subplot(2, 2, 4)
                        df_heat = self._fetch_metric_df_for_ticker("v_heatmap_returns", ticker, start_date, end_date)
                        self._plot_on_axes(ax4, fig_ind, df_heat, "v_heatmap_returns", ticker_label=f"{ticker} - Heatmap Mensal", legend_below=False)
                        
                        fig_ind.tight_layout(rect=[0, 0.03, 1, 0.95])
                        pdf.savefig(fig_ind)
                        plt.close(fig_ind)

                    except Exception as e:
                        log_err(f"Erro ao gerar página para {ticker}: {e}")
                        fig_err = Figure()
                        fig_err.text(0.5, 0.5, f"Erro ao gerar dados para {ticker}:\n{e}", ha='center', va='center', color='red', wrap=True)
                        pdf.savefig(fig_err)
                        plt.close(fig_err)

            self.set_status("PDF gerado com sucesso!")
            messagebox.showinfo("Sucesso", f"Relatório PDF foi salvo em:\n{pdf_path}")

        except Exception as e:
            self.set_status("Erro ao gerar PDF.")
            log_err(f"Falha na geração do PDF: {e}")
            traceback.print_exc()
            messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o PDF:\n{e}")
            
    def open_pdf_viewer(self):
        if not PDF2IMAGE_AVAILABLE:
            messagebox.showwarning("Dependência ausente", "Instale 'pdf2image' e 'Pillow'.\nVerifique também se o Poppler está no PATH.")
            return
        pdf_path = filedialog.askopenfilename(
            title="Abrir Relatório PDF", initialdir=ensure_rel_dir(),
            filetypes=[("PDF Files", "*.pdf")]
        )
        if not pdf_path: return

        if self.pdf_viewer and self.pdf_viewer.is_open():
            self.pdf_viewer.bring_to_front()
            return
            
        poppler_path = next((p for p in COMMON_POPPLER_PATHS if os.path.isdir(p)), None)
        self.pdf_viewer = PdfViewerWindow(self.root, pdf_path, poppler_path=poppler_path)
        self.pdf_viewer.open()

# ---------------- PDF Viewer class ----------------
class PdfViewerWindow:
    def __init__(self, parent, pdf_path, poppler_path=None):
        self.parent = parent
        self.pdf_path = pdf_path
        self.poppler_path = poppler_path
        self.top = None
        self.images = []
        self.tk_images = []
        self.current_page = 0
        self.n_pages = 0

    def is_open(self):
        return self.top and self.top.winfo_exists()

    def bring_to_front(self):
        if self.is_open():
            self.top.lift(); self.top.focus_force()

    def open(self):
        try:
            self.images = convert_from_path(self.pdf_path, dpi=150, poppler_path=self.poppler_path)
            self.n_pages = len(self.images)
        except Exception as e:
            messagebox.showerror("Erro ao Abrir PDF", f"Falha ao converter o PDF.\nVerifique a instalação do Poppler.\n\nDetalhe: {e}")
            return

        self.top = tk.Toplevel(self.parent)
        self.top.title(f"Visualizador - {os.path.basename(self.pdf_path)}")
        self.top.geometry("900x700")

        nav = ttk.Frame(self.top); nav.pack(fill=tk.X, padx=6, pady=6)
        self.label_info = ttk.Label(nav, text=f"Página 1/{self.n_pages}")
        self.label_info.pack(side=tk.LEFT, padx=6)
        ttk.Button(nav, text="◀ Anterior", command=self.prev_page).pack(side=tk.RIGHT)
        ttk.Button(nav, text="Próxima ▶", command=self.next_page).pack(side=tk.RIGHT)
        
        canvas_frame = ttk.Frame(self.top); canvas_frame.pack(fill=tk.BOTH, expand=True)
        hbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        vbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        self.canvas = tk.Canvas(canvas_frame, xscrollcommand=hbar.set, yscrollcommand=vbar.set, background='white')
        hbar.config(command=self.canvas.xview); vbar.config(command=self.canvas.yview)
        self.canvas.grid(row=0, column=0, sticky="nsew"); vbar.grid(row=0, column=1, sticky="ns"); hbar.grid(row=1, column=0, sticky="ew")
        canvas_frame.rowconfigure(0, weight=1); canvas_frame.columnconfigure(0, weight=1)
        
        self.tk_images = [None] * self.n_pages
        self._render_page(0)

    def _render_page(self, idx):
        if 0 <= idx < self.n_pages:
            self.current_page = idx
            pil_img = self.images[idx]
            tk_img = ImageTk.PhotoImage(pil_img)
            self.tk_images[idx] = tk_img
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=tk_img)
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
            self.label_info.config(text=f"Página {idx + 1}/{self.n_pages}")

    def prev_page(self):
        if self.current_page > 0:
            self._render_page(self.current_page - 1)

    def next_page(self):
        if self.current_page < self.n_pages - 1:
            self._render_page(self.current_page + 1)


def main():
    if tb is None:
        root_tmp = tk.Tk(); root_tmp.withdraw()
        messagebox.showwarning("Aviso", "Pacote 'ttkbootstrap' não encontrado. Continue sem tema.")
        root_tmp.destroy()
    root = tk.Tk()
    if tb:
        try: tb.Style(theme=DEFAULT_THEME)
        except Exception: pass
    app = B3DashboardV5FixSQL(root)
    log_info("Launching GUI...")
    root.mainloop()
    log_ok("GUI closed")

if __name__ == "__main__":
    main()