import sys
import io
import os
import argparse
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import minimize
from scipy.stats import norm, skew, kurtosis
from matplotlib.backends.backend_pdf import PdfPages
import pymysql
from datetime import datetime

# For Windows consoles / redirected stdout (GUI) ensure UTF-8
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except Exception:
    # In some environments (like IDLE) stdout may not have buffer; ignore
    pass

def printp(msg):
    """Print wrapper that prefixes PROGRESS lines when provided as tuples."""
    print(msg)
    sys.stdout.flush()

def emit_progress(percent:int, text:str=None):
    """Emit a progress message the GUI can parse."""
    if text:
        printp(f"PROGRESS: {percent}% - {text}")
    else:
        printp(f"PROGRESS: {percent}%")

def connect_db(host="localhost", user="root", password="mysql", database="b3dw", port=3306):
    emit_progress(2, "Conectando ao banco de dados...")
    try:
        conn = pymysql.connect(host=host, user=user, password=password, database=database, port=port)
        emit_progress(5, "Conexão com MySQL estabelecida")
        return conn
    except Exception as e:
        printp(f"PROGRESS: 0% - ERRO: não foi possível conectar ao MySQL: {e}")
        raise

def create_results_table(conn):
    emit_progress(6, "Criando tabela de resultados (se necessário)...")
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS risk_analysis_result (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ticker VARCHAR(32),
        annual_return DOUBLE,
        annual_volatility DOUBLE,
        beta_ibov DOUBLE,
        coef_var DOUBLE,
        var_hist DOUBLE,
        cvar_hist DOUBLE,
        var_param DOUBLE,
        var_cf DOUBLE,
        mc_var DOUBLE,
        mc_cvar DOUBLE,
        bs_var DOUBLE,
        bs_cvar DOUBLE,
        portfolio_var DOUBLE,
        portfolio_cvar DOUBLE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB;
    """
    with conn.cursor() as cur:
        cur.execute(create_table_sql)
    conn.commit()
    emit_progress(8, "Tabela de resultados pronta")

def fetch_tickers_from_db(conn):
    emit_progress(10, "Lendo tickers da tabela dim_asset...")
    with conn.cursor() as cur:
        cur.execute("SELECT DISTINCT ticker FROM dim_asset ORDER BY ticker")
        rows = cur.fetchall()
    tickers = [r[0] for r in rows]
    emit_progress(12, f"{len(tickers)} tickers encontrados no banco")
    return tickers

def ensure_relatorio_dir(path="./relatorios"):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
    return os.path.abspath(path)

def run_analysis(tickers, start_date="2023-01-01", end_date=None,
                 confidence_level=0.95, n_simulations=1000, n_days=252,
                 save_dir="./relatorios"):
    if end_date is None:
        end_date = datetime.today().strftime("%Y-%m-%d")

    save_dir = ensure_relatorio_dir(save_dir)
    emit_progress(15, f"Relatórios serão gravados em: {save_dir}")

    # 1) Download
    emit_progress(18, "Baixando dados do Yahoo Finance (pode demorar)...")
    # add IBOV
    queries = list(tickers) + ["^BVSP"]
    try:
        data = yf.download(queries, start=start_date, end=end_date, auto_adjust=True)["Close"]
    except Exception as e:
        printp(f"PROGRESS: 0% - ERRO: falha ao baixar dados: {e}")
        raise

    # remove totally empty columns
    data.dropna(axis=1, how="all", inplace=True)
    data.rename(columns={"^BVSP": "IBOV"}, inplace=True)
    if "IBOV" not in data.columns:
        printp("PROGRESS: 0% - ERRO: índice IBOV não foi baixado corretamente.")
        raise RuntimeError("IBOV missing")

    valid_tickers = [t for t in tickers if t in data.columns]
    invalid_tickers = [t for t in tickers if t not in valid_tickers]
    if invalid_tickers:
        printp(f"PROGRESS: 20% - Tick­ers ignorados (sem dados ou delistados): {invalid_tickers}")
    else:
        emit_progress(20, "Todos os tickers têm dados válidos")

    emit_progress(22, f"{len(valid_tickers)} tickers válidos para análise")

    results_list = []
    figures = []
    total = len(valid_tickers)
    if total == 0:
        printp("PROGRESS: 0% - Nenhum ticker válido para processar. Encerrando.")
        return pd.DataFrame([])

    # iterate and compute
    for idx, ticker in enumerate(valid_tickers, start=1):
        pct_base = 22
        pct = pct_base + int((idx-1)/total * 60)  # progress during loop
        emit_progress(min(90, pct), f"Processando {ticker} ({idx}/{total})")

        # returns
        ret = data[[ticker, "IBOV"]].pct_change().dropna()
        if ret.empty:
            printp(f"PROGRESS: - - Pulando {ticker} (sem retornos válidos)")
            continue

        mean_daily_return = ret[ticker].mean()
        daily_volatility = ret[ticker].std()
        annual_return = mean_daily_return * 252
        annual_volatility = daily_volatility * np.sqrt(252)

        cov_matrix = ret.cov()
        try:
            beta = cov_matrix.loc[ticker, "IBOV"] / cov_matrix.loc["IBOV", "IBOV"]
        except Exception:
            beta = np.nan
        cv = annual_volatility / abs(annual_return) if annual_return != 0 else np.nan

        # VaR
        try:
            VaR_hist = np.percentile(ret[ticker], (1 - confidence_level) * 100)
            CVaR_hist = ret[ticker][ret[ticker] <= VaR_hist].mean()
        except Exception:
            VaR_hist = np.nan
            CVaR_hist = np.nan

        z = norm.ppf(confidence_level)
        VaR_param = -(mean_daily_return - z * daily_volatility)
        s = skew(ret[ticker])
        k = kurtosis(ret[ticker], fisher=True)
        z_cf = (z + (1/6)*(z**2 - 1)*s + (1/24)*(z**3 - 3*z)*k - (1/36)*(2*z**3 - 5*z)*s**2)
        VaR_cf = -(mean_daily_return - z_cf * daily_volatility)

        # MC
        np.random.seed(42)
        S0 = data[ticker].iloc[-1]
        sim_paths_mc = np.zeros((n_days, n_simulations))
        for i in range(n_simulations):
            daily_sim = np.random.normal(mean_daily_return, daily_volatility, n_days)
            sim_paths_mc[:, i] = S0 * np.exp(np.cumsum(daily_sim))
        final_mc = sim_paths_mc[-1, :]
        expected_mc = np.mean(final_mc)
        var_mc = np.percentile(final_mc, (1 - confidence_level) * 100)
        cvar_mc = np.mean(final_mc[final_mc <= var_mc]) if final_mc.size>0 else np.nan

        # Bootstrapping
        sim_paths_bs = np.zeros((n_days, n_simulations))
        for i in range(n_simulations):
            daily_boot = np.random.choice(ret[ticker].values, n_days, replace=True)
            sim_paths_bs[:, i] = S0 * np.exp(np.cumsum(daily_boot))
        final_bs = sim_paths_bs[-1, :]
        expected_bs = np.mean(final_bs)
        var_bs = np.percentile(final_bs, (1 - confidence_level) * 100)
        cvar_bs = np.mean(final_bs[final_bs <= var_bs]) if final_bs.size>0 else np.nan

        # portfolio optimization (ticker + IBOV)
        mean_returns = ret.mean() * 252
        cov_matrix_annual = ret.cov() * 252

        def port_vol(weights):
            return np.sqrt(weights.T @ cov_matrix_annual.values @ weights)

        def port_ret(weights):
            return weights.T @ mean_returns.values

        def neg_sharpe(weights, risk_free=0):
            v = port_vol(weights)
            return -(port_ret(weights) - risk_free) / v if v > 0 else 1e9

        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for _ in range(ret.shape[1]))
        try:
            res_minvar = minimize(port_vol, ret.shape[1] * [1 / ret.shape[1]], bounds=bounds, constraints=constraints)
            weights_minvar = res_minvar.x
            ret_minvar = port_ret(weights_minvar)
            vol_minvar = port_vol(weights_minvar)
        except Exception:
            weights_minvar = np.nan
            ret_minvar = np.nan
            vol_minvar = np.nan

        try:
            res_maxsharpe = minimize(neg_sharpe, ret.shape[1] * [1 / ret.shape[1]], bounds=bounds, constraints=constraints)
            weights_maxsharpe = res_maxsharpe.x
            ret_maxsharpe = port_ret(weights_maxsharpe)
            vol_maxsharpe = port_vol(weights_maxsharpe)
        except Exception:
            weights_maxsharpe = np.nan
            ret_maxsharpe = np.nan
            vol_maxsharpe = np.nan

        # simulate portfolio
        try:
            S0_port = ret.iloc[-1].values
            sim_paths_port = np.zeros((n_days, n_simulations))
            for i in range(n_simulations):
                daily_port = np.random.multivariate_normal(mean_returns.values / 252, ret.cov().values, n_days)
                prices = S0_port * np.exp(np.cumsum(daily_port, axis=0))
                sim_paths_port[:, i] = prices @ weights_maxsharpe
            final_port = sim_paths_port[-1, :]
            var_port = np.percentile(final_port, (1 - confidence_level) * 100)
            cvar_port = np.mean(final_port[final_port <= var_port]) if final_port.size>0 else np.nan
        except Exception:
            var_port = np.nan
            cvar_port = np.nan

        results_list.append({
            "Ativo": ticker,
            "Retorno anual (%)": annual_return * 100,
            "Volatilidade anual (%)": annual_volatility * 100,
            "Beta IBOV": beta,
            "Coeficiente de variação": cv,
            "VaR histórico 95%": VaR_hist,
            "CVaR histórico 95%": CVaR_hist,
            "VaR paramétrico": VaR_param,
            "VaR Cornish-Fisher": VaR_cf,
            "MC Preço esperado": expected_mc,
            "MC VaR": var_mc,
            "MC CVaR": cvar_mc,
            "BS Preço esperado": expected_bs,
            "BS VaR": var_bs,
            "BS CVaR": cvar_bs,
            "Portfólio Retorno": ret_maxsharpe,
            "Portfólio Volatilidade": vol_maxsharpe,
            "Portfólio VaR": var_port,
            "Portfólio CVaR": cvar_port,
            "Pesos MinVar": str(weights_minvar),
            "Pesos MaxSharpe": str(weights_maxsharpe)
        })

        # update progress inside loop
        emit_progress(min(90, pct_base + int(idx / total * 60)), f"{ticker} finalizado ({idx}/{total})")

    # After loop: save results
    emit_progress(92, "Gerando DataFrame de resultados...")
    results_df = pd.DataFrame(results_list)

    # Excel
    excel_path = os.path.join(save_dir, "analise_risco_todos_tickers.xlsx")
    try:
        results_df.to_excel(excel_path, index=False)
        emit_progress(95, f"Excel salvo em {excel_path}")
    except Exception as e:
        printp(f"PROGRESS: - - Erro ao salvar Excel: {e}")

    # PDF (basic: table)
    pdf_path = os.path.join(save_dir, "analise_risco_todos_ativos.pdf")
    try:
        with PdfPages(pdf_path) as pdf:
            for r in results_list[:0]:  # placeholder — keep PDF small: write only summary table page
                pass
            # table page
            fig_table, ax_table = plt.subplots(figsize=(12,6))
            ax_table.axis('off')
            if not results_df.empty:
                cellText = results_df.round(2).values
                table = ax_table.table(cellText=cellText, colLabels=results_df.columns, cellLoc='center', loc='center')
                table.auto_set_font_size(False)
                table.set_fontsize(8)
                table.scale(1,1.5)
            else:
                ax_table.text(0.5, 0.5, "Sem resultados", ha='center', va='center')
            pdf.savefig(fig_table, bbox_inches='tight')
            plt.close(fig_table)
        emit_progress(97, f"PDF salvo em {pdf_path}")
    except Exception as e:
        printp(f"PROGRESS: - - Erro ao salvar PDF: {e}")

    # Insert into DB
    emit_progress(98, "Inserindo resultados no banco de dados...")
    try:
        # connect fresh (use same conn passed)
        # We already have conn in outer scope if passed. We'll assume conn is open.
        # Insert rows
        # Avoid duplicates by simple INSERT (you can improve with REPLACE or unique constraints)
        db_conn = connect_db()  # open a new short-lived connection to be safe
        with db_conn.cursor() as cur:
            for _, row in results_df.iterrows():
                cur.execute("""
                    INSERT INTO risk_analysis_result
                    (ticker, annual_return, annual_volatility, beta_ibov, coef_var,
                     var_hist, cvar_hist, var_param, var_cf, mc_var, mc_cvar,
                     bs_var, bs_cvar, portfolio_var, portfolio_cvar)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    row.get("Ativo"), row.get("Retorno anual (%)"), row.get("Volatilidade anual (%)"),
                    row.get("Beta IBOV"), row.get("Coeficiente de variação"),
                    row.get("VaR histórico 95%"), row.get("CVaR histórico 95%"),
                    row.get("VaR paramétrico"), row.get("VaR Cornish-Fisher"),
                    row.get("MC VaR"), row.get("MC CVaR"),
                    row.get("BS VaR"), row.get("BS CVaR"),
                    row.get("Portfólio VaR"), row.get("Portfólio CVaR")
                ))
        db_conn.commit()
        db_conn.close()
        emit_progress(99, "Resultados inseridos no MySQL")
    except Exception as e:
        printp(f"PROGRESS: - - Erro ao inserir no banco: {e}")

    # Final
    emit_progress(100, "Concluído com sucesso!")
    return results_df

def main():
    parser = argparse.ArgumentParser(description="Análise de risco por ticker (v3).")
    parser.add_argument("tickers", nargs="*", help="Tickers opcionais. Se omitidos, pega todos de dim_asset.")
    parser.add_argument("--start", default="2023-01-01", help="Data início (YYYY-MM-DD)")
    parser.add_argument("--end", default=None, help="Data fim (YYYY-MM-DD)")
    parser.add_argument("--outdir", default="./relatorios", help="Diretório de relatórios")
    args = parser.parse_args()

    # connect
    conn = connect_db()
    create_results_table(conn)

    if args.tickers:
        tickers = args.tickers
        emit_progress(10, f"Recebidos {len(tickers)} tickers por argumento")
    else:
        tickers = fetch_tickers_from_db(conn)

    try:
        # run
        run_analysis(tickers, start_date=args.start, end_date=args.end, save_dir=args.outdir)
    except Exception as e:
        printp(f"PROGRESS: 0% - ERRO no processamento: {e}")
    finally:
        try:
            conn.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
