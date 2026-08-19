import os
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Carrega o .env explicitamente e sobrescreve variáveis do sistema se existirem
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path, override=True)

# Pega DSN e diretório de dados do .env
MYSQL_DSN = os.getenv("MYSQL_DSN")
DATA_DIR = os.getenv("DATA_DIR", "./data")

# Cria engine SQLAlchemy
engine = create_engine(MYSQL_DSN, future=True)

def test_connection():
    """Testa a conexão com o MySQL antes de qualquer carga."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexão com MySQL OK! Resultado:", result.scalar())
            return True
    except Exception as e:
        print("❌ Falha na conexão com MySQL:", e)
        return False

def read_bronze(base_dir=DATA_DIR):
    paths = list(Path(base_dir).glob("bronze/prices/year=*/month=*/prices_*.parquet"))
    frames = [pd.read_parquet(p) for p in paths]
    if not frames:
        print("Nenhum arquivo bronze encontrado.")
        return pd.DataFrame()
    df = pd.concat(frames, ignore_index=True)
    df['trade_date'] = pd.to_datetime(df['trade_date'])
    return df

def load_staging(df: pd.DataFrame):
    if df.empty:
        return
    with engine.begin() as conn:
        df.to_sql("stg_prices", conn, if_exists="replace", index=False, method='multi', chunksize=1000)
    print("✅ Staging carregada.")

def upsert_dims_and_facts():
    with engine.begin() as conn:
        conn.exec_driver_sql("""
        INSERT INTO dim_exchange (name, mic, timezone)
        VALUES ('B3','BVMF','America/Sao_Paulo')
        ON DUPLICATE KEY UPDATE name = VALUES(name);
        """)
        conn.exec_driver_sql("""
        INSERT INTO dim_asset (ticker)
        SELECT DISTINCT ticker FROM stg_prices sp
        ON DUPLICATE KEY UPDATE ticker = VALUES(ticker);
        """)
        conn.exec_driver_sql("""
        INSERT INTO dim_date (date_id, year, quarter, month, day, weekday, is_business, is_holiday)
        SELECT DISTINCT
            DATE(trade_date),
            YEAR(trade_date),
            QUARTER(trade_date),
            MONTH(trade_date),
            DAY(trade_date),
            DAYOFWEEK(trade_date),
            TRUE,
            FALSE
        FROM stg_prices
        ON DUPLICATE KEY UPDATE date_id = date_id;
        """)
        conn.exec_driver_sql("""
        INSERT INTO fact_price (asset_id, date_id, exchange_id, open, high, low, close, adj_close, volume, trades)
        SELECT
          da.asset_id,
          DATE(sp.trade_date),
          de.exchange_id,
          sp.open, sp.high, sp.low, sp.close, sp.adj_close, sp.volume, NULL
        FROM stg_prices sp
        JOIN dim_asset da ON da.ticker = sp.ticker
        JOIN dim_exchange de ON de.name = 'B3'
        ON DUPLICATE KEY UPDATE
          open = VALUES(open),
          high = VALUES(high),
          low = VALUES(low),
          close = VALUES(close),
          adj_close = VALUES(adj_close),
          volume = VALUES(volume),
          trades = VALUES(trades);
        """)
    print("✅ Dimensões e fatos atualizados.")

def refresh_metrics():
    """Executa o SQL de métricas (metrics_mysql.sql)."""
    script_dir = Path(__file__).parent
    sql_path = script_dir.parent / "sql" / "metrics_mysql.sql"
    
    if not sql_path.exists():
        print("⚠️ Arquivo metrics_mysql.sql não encontrado. Pulei refresh de métricas.")
        return

    sql_text = sql_path.read_text(encoding="utf-8")
    with engine.begin() as conn:
        for stmt in [s.strip() for s in sql_text.split(';') if s.strip()]:
            conn.exec_driver_sql(stmt)
    print("✅ Métricas (returns e vol_21d) atualizadas.")

if __name__ == "__main__":
    if not test_connection():
        print("❌ Não foi possível conectar ao MySQL. Abortando pipeline.")
        exit(1)

    df = read_bronze()
    load_staging(df)
    upsert_dims_and_facts()
    refresh_metrics()
    print("🚀 Pipeline concluído com sucesso!")
