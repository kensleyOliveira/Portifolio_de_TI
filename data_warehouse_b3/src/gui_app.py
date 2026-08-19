

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import traceback
import pymysql
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="pandas.io.sql")

# ---------------- Conexão Global ----------------
conn = pymysql.connect(
    host="localhost",
    user="user",
    password="password",
    database="b3dw",
    port=3306
)

# ---------------- Funções Auxiliares ----------------
def calc_metrics(returns: pd.DataFrame):
    """
    Calcula métricas básicas para cada ativo (coluna em returns).
    returns = DataFrame de retornos diários (%).
    """
    metrics = []
    ann_factor = 252

    for col in returns.columns:
        r = returns[col].dropna()
        if r.empty:
            continue

        ann_ret = (1 + r).prod() ** (ann_factor / len(r)) - 1
        ann_vol = r.std() * np.sqrt(ann_factor)
        sharpe = ann_ret / ann_vol if ann_vol > 0 else np.nan
        cum = (1 + r).cumprod() - 1
        drawdown = (cum - cum.cummax()).min()
        n_obs = len(r)

        metrics.append({
            "ticker": col,
            "ann_return": ann_ret,
            "ann_vol": ann_vol,
            "sharpe": sharpe,
            "max_drawdown": drawdown,
            "cum_return": cum.iloc[-1] if not cum.empty else np.nan,
            "n_obs": n_obs
        })
    return pd.DataFrame(metrics)


def suggest_portfolios(returns: pd.DataFrame):
    """
    Sugere carteiras:
    - Equal Weight
    - Min Vol
    - Max Sharpe
    """
    ann_factor = 252
    mean_ret = returns.mean() * ann_factor
    cov = returns.cov() * ann_factor
    n = len(returns.columns)

    txt = []

    if n == 0:
        return "Nenhum ativo para sugerir carteiras."

    # Equal weight
    w_eq = np.repeat(1/n, n)
    ret_eq = np.dot(w_eq, mean_ret)
    vol_eq = np.sqrt(np.dot(w_eq.T, np.dot(cov, w_eq)))
    txt.append(f"Equal Weight: Ret {ret_eq:.2%}, Vol {vol_eq:.2%}, Sharpe {ret_eq/vol_eq:.2f}")

    # Min Vol
    try:
        inv_cov = np.linalg.inv(cov)
        ones = np.ones(n)
        w_min = inv_cov.dot(ones) / (ones.dot(inv_cov).dot(ones))
        ret_min = np.dot(w_min, mean_ret)
        vol_min = np.sqrt(np.dot(w_min.T, np.dot(cov, w_min)))
        txt.append(f"Min Vol: Ret {ret_min:.2%}, Vol {vol_min:.2%}, Sharpe {ret_min/vol_min:.2f}")
    except Exception:
        txt.append("Min Vol: erro de cálculo (matriz singular).")

    # Max Sharpe (simplificado via busca aleatória)
    best_sr = -999
    best_w = None
    for _ in range(2000):
        w = np.random.random(n)
        w /= w.sum()
        ret = np.dot(w, mean_ret)
        vol = np.sqrt(np.dot(w.T, np.dot(cov, w)))
        sr = ret/vol if vol>0 else -999
        if sr > best_sr:
            best_sr = sr
            best_w = w
    if best_w is not None:
        txt.append(f"Max Sharpe: Ret {np.dot(best_w, mean_ret):.2%}, "
                   f"Vol {np.sqrt(best_w.T@cov@best_w):.2%}, Sharpe {best_sr:.2f}")

    return "\n".join(txt)


# ---------------- GUI Class ----------------
class B3Dashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("B3 DW Dashboard")
        self.geometry("1200x820")
        self.conn = conn

        # Top controls
        ctrl = ttk.Frame(self)
        ctrl.pack(side=tk.TOP, fill=tk.X, padx=8, pady=6)

        # Tickers listbox
        ttk.Label(ctrl, text="Tickers:").pack(side=tk.LEFT, padx=(4,2))
        tframe = ttk.Frame(ctrl)
        tframe.pack(side=tk.LEFT)
        self.ticker_listbox = tk.Listbox(tframe, width=22, height=8, selectmode=tk.EXTENDED, exportselection=False)
        self.ticker_scroll = ttk.Scrollbar(tframe, orient=tk.VERTICAL, command=self.ticker_listbox.yview)
        self.ticker_listbox.config(yscrollcommand=self.ticker_scroll.set)
        self.ticker_listbox.pack(side=tk.LEFT, fill=tk.Y)
        self.ticker_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.load_tickers()

        # Metric combobox
        ttk.Label(ctrl, text="Métrica/View:").pack(side=tk.LEFT, padx=(10,2))
        self.metric_combo = ttk.Combobox(ctrl, values=[
            "v_returns", "v_vol_21d", "v_dashboard", "v_drawdown",
            "v_heatmap_returns", "v_asset_returns", "v_cum_returns", "v_splits"
        ], state="readonly", width=22)
        self.metric_combo.current(0)
        self.metric_combo.pack(side=tk.LEFT, padx=(2, 6))

        # Date range entries
        ttk.Label(ctrl, text="Data Início (YYYY-MM-DD):").pack(side=tk.LEFT)
        self.start_entry = ttk.Entry(ctrl, width=12)
        self.start_entry.insert(0, "2010-01-01")
        self.start_entry.pack(side=tk.LEFT, padx=(4,6))

        ttk.Label(ctrl, text="Data Fim (YYYY-MM-DD):").pack(side=tk.LEFT)
        self.end_entry = ttk.Entry(ctrl, width=12)
        self.end_entry.insert(0, "2025-12-31")
        self.end_entry.pack(side=tk.LEFT, padx=(4,8))

        # Buttons
        ttk.Button(ctrl, text="Plotar (único)", command=self.on_plot).pack(side=tk.LEFT, padx=4)
        ttk.Button(ctrl, text="Comparar (multi)", command=self.on_compare).pack(side=tk.LEFT, padx=4)
        ttk.Button(ctrl, text="Refresh Tickers", command=self.reload_tickers).pack(side=tk.LEFT, padx=4)

        # Paned window
        main_pane = ttk.Panedwindow(self, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(main_pane, width=420)
        right_frame = ttk.Frame(main_pane)
        main_pane.add(left_frame, weight=1)
        main_pane.add(right_frame, weight=3)

        # Treeview table
        ttk.Label(left_frame, text="Tabela / Resultados", font=("TkDefaultFont", 10, "bold")).pack(anchor=tk.W, padx=6, pady=(6,0))
        cols = ("ticker","ann_return","ann_vol","sharpe","max_drawdown","cum_return","n_obs")
        self.tree = ttk.Treeview(left_frame, columns=cols, show="headings", height=15)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=85, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        # Portfolio suggestions
        ttk.Label(left_frame, text="Carteiras sugeridas", font=("TkDefaultFont", 10, "bold")).pack(anchor=tk.W, padx=6)
        self.port_txt = ScrolledText(left_frame, height=14)
        self.port_txt.pack(fill=tk.X, expand=False, padx=6, pady=(4,8))

        # Matplotlib figure
        self.fig = Figure(figsize=(8,6), dpi=110)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status = ttk.Label(self, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    # ---------------- ticker loading ----------------
    def load_tickers(self):
        self.ticker_listbox.delete(0, tk.END)
        tickers = []
        if self.conn:
            try:
                q = "SELECT DISTINCT ticker FROM dim_asset ORDER BY ticker"
                df = pd.read_sql(q, self.conn)
                tickers = df['ticker'].tolist()
            except Exception as e:
                print(f"[WARN] Falha ao buscar tickers: {e}")

        for t in tickers:
            self.ticker_listbox.insert(tk.END, t)

    def reload_tickers(self):
        self.load_tickers()
        self.set_status("Tickers recarregados")

    def set_status(self, txt):
        self.status.config(text=txt)
        self.update_idletasks()

    # ---------------- single plot ----------------
    def on_plot(self):
        sel = self.ticker_listbox.curselection()
        if not sel:
            messagebox.showinfo("Info", "Selecione pelo menos um ticker (um).")
            return
        ticker = self.ticker_listbox.get(sel[0])
        metric = self.metric_combo.get()
        start_date = self.start_entry.get().strip()
        end_date = self.end_entry.get().strip()
        self.plot_metric_for_ticker(ticker, metric, start_date, end_date)

    def plot_metric_for_ticker(self, ticker, metric, start_date, end_date):
        if not self.conn:
            messagebox.showerror("Erro", "Sem conexão com banco.")
            return

        no_date_filter = {"v_heatmap_returns", "v_asset_returns"}
        date_col = None
        if metric == "v_splits":
            date_col = "ex_date"
        elif metric not in no_date_filter:
            date_col = "date_id"

        if date_col:
            q = f"SELECT * FROM {metric} WHERE ticker = %s AND {date_col} BETWEEN %s AND %s ORDER BY {date_col}"
            params = (ticker, start_date, end_date)
        else:
            q = f"SELECT * FROM {metric} WHERE ticker = %s"
            params = (ticker,)

        try:
            df = pd.read_sql(q, self.conn, params=params)
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Erro SQL", f"Falha na query: {e}")
            return

        if df.empty:
            self.ax.clear()
            self.ax.text(0.5, 0.5, "Nenhum dado encontrado", ha="center", va="center")
            self.canvas.draw()
            return

        if 'date_id' in df.columns:
            try:
                df['date_id'] = pd.to_datetime(df['date_id'])
            except Exception:
                pass

        self.ax.clear()
        if metric == "v_returns":
            if "ret_simple" in df.columns:
                self.ax.plot(df['date_id'], df['ret_simple'], label="Retorno Simples")
            if "ret_log" in df.columns:
                self.ax.plot(df['date_id'], df['ret_log'], linestyle='--', label="Retorno Log")
        elif metric == "v_vol_21d":
            if "vol_21d" in df.columns:
                self.ax.plot(df['date_id'], df['vol_21d'], label="Vol 21d")
        elif metric == "v_dashboard":
            ax2 = self.ax.twinx()
            if "adj_close" in df.columns:
                self.ax.plot(df['date_id'], df['adj_close'], label="Preço Ajustado")
            if "vol_21d" in df.columns:
                ax2.plot(df['date_id'], df['vol_21d'], linestyle='--', label="Vol 21d")
        elif metric == "v_drawdown":
            if "drawdown" in df.columns:
                self.ax.plot(df['date_id'], df['drawdown'], label="Drawdown")
        elif metric == "v_cum_returns":
            if "cum_return" in df.columns:
                self.ax.plot(df['date_id'], df['cum_return'], label="Retorno Acumulado")

        self.ax.set_title(f"{ticker} - {metric}")
        self.ax.legend(loc='best')
        self.canvas.draw()

    # ---------------- compare (multi) ----------------
    def on_compare(self):
        sel = self.ticker_listbox.curselection()
        if not sel:
            messagebox.showinfo("Info", "Selecione pelo menos um ticker para comparar.")
            return
        tickers = [self.ticker_listbox.get(i) for i in sel]
        start_date = self.start_entry.get().strip()
        end_date = self.end_entry.get().strip()

        q = f"""
            SELECT a.ticker, fp.date_id, fp.adj_close
            FROM fact_price fp
            JOIN dim_asset a ON a.asset_id = fp.asset_id
            WHERE a.ticker IN ({','.join(['%s']*len(tickers))})
              AND fp.date_id BETWEEN %s AND %s
            ORDER BY a.ticker, fp.date_id
        """
        params = tickers + [start_date, end_date]

        try:
            df_prices = pd.read_sql(q, self.conn, params=params)
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Erro SQL", f"Falha ao buscar preços: {e}")
            return

        if df_prices.empty:
            messagebox.showinfo("Info", "Nenhum preço retornado para os tickers e período selecionado.")
            return

        self.ax.clear()
        wide = df_prices.pivot(index="date_id", columns="ticker", values="adj_close").sort_index()
        daily_r = wide.pct_change().fillna(0)
        cum = (1 + daily_r).cumprod() - 1
        cum.index = pd.to_datetime(cum.index)

        for t in tickers:
            if t in cum.columns:
                self.ax.plot(cum.index, cum[t], label=t)

        self.ax.set_title("Retorno Acumulado (comparação)")
        self.ax.legend(loc="best")
        self.canvas.draw()

        # ---- Calcular métricas ----
        metrics_df = calc_metrics(daily_r)

        # Limpar tree
        for i in self.tree.get_children():
            self.tree.delete(i)
        for _, row in metrics_df.iterrows():
            self.tree.insert("", tk.END, values=(
                row["ticker"],
                f"{row['ann_return']:.2%}",
                f"{row['ann_vol']:.2%}",
                f"{row['sharpe']:.2f}",
                f"{row['max_drawdown']:.2%}",
                f"{row['cum_return']:.2%}",
                row["n_obs"]
            ))

        # ---- Sugestões de carteiras ----
        self.port_txt.delete(1.0, tk.END)
        self.port_txt.insert(tk.END, suggest_portfolios(daily_r))

        self.set_status("Comparação concluída")


# ---------------- main ----------------
if __name__ == "__main__":
    app = B3Dashboard()
    app.mainloop()
