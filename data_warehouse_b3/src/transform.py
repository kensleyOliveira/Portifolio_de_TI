import pandas as pd
from sqlalchemy import create_engine, text
from config import MYSQL_DSN as SQLALCHEMY_DSN

engine = create_engine(SQLALCHEMY_DSN, future=True)

# A função pura que já testamos exaustivamente
def calculate_adj_close_logic(prices_df: pd.DataFrame, splits_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula o 'adj_close' com base nos preços e splits fornecidos.
    Esta é uma função pura, sem acesso ao banco de dados.
    """
    df = prices_df.sort_values("date_id", ascending=False).copy()
    splits = splits_df.sort_values("ex_date", ascending=False).copy()
    
    cumulative_factor = 1.0
    adj_values = []
    split_idx = 0
    
    for _, row in df.iterrows():
        while (split_idx < len(splits) and
               row['date_id'].date() < splits.iloc[split_idx]['ex_date'].date()):
            cumulative_factor *= float(splits.iloc[split_idx]['split_ratio'])
            split_idx += 1
            
        adj_values.append(row['close'] * cumulative_factor)
    
    df['adj_close'] = list(reversed(adj_values))
    return df.sort_values("date_id", ascending=True)

# A função orquestradora que interage com o banco
def recalc_adj_close(asset_ticker: str):
    """
    Orquestra a leitura, cálculo e escrita do preço de fechamento ajustado.
    """
    # 1. Leitura de dados (I/O)
    query_prices = """
        SELECT fp.date_id, da.ticker, fp.close
        FROM fact_price fp
        JOIN dim_asset da ON da.asset_id = fp.asset_id
        WHERE da.ticker = :ticker
        ORDER BY fp.date_id;
    """
    prices_df = pd.read_sql_query(query_prices, engine, params={"ticker": asset_ticker}, parse_dates=["date_id"])

    if prices_df.empty:
        print(f"Nenhum dado encontrado para {asset_ticker}")
        return

    query_splits = """
        SELECT s.ex_date, s.split_ratio
        FROM fact_split s
        JOIN dim_asset da ON da.asset_id = s.asset_id
        WHERE da.ticker = :ticker
        ORDER BY s.ex_date DESC
    """
    splits_df = pd.read_sql_query(query_splits, engine, params={"ticker": asset_ticker}, parse_dates=["ex_date"])

    # 2. Lógica de cálculo (Função Pura)
    df_with_adj = calculate_adj_close_logic(prices_df, splits_df)

    # 3. Escrita de dados (I/O)
    update_query = text("""
        UPDATE fact_price SET adj_close = :adj
        WHERE date_id = :d AND asset_id = (SELECT asset_id FROM dim_asset WHERE ticker = :t)
    """)
    with engine.begin() as conn:
        for _, r in df_with_adj.iterrows():
            conn.execute(
                update_query,
                {"adj": float(r['adj_close']), "d": r['date_id'].date(), "t": asset_ticker}
            )
            
    print(f"Adj closes recalculados para {asset_ticker}")