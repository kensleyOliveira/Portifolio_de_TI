
import os
from datetime import datetime
from pathlib import Path
import pandas as pd
import yfinance as yf
from config import DATA_DIR, TICKERS

def fetch_daily_history(tickers, start="2010-01-01", end=None):
    end = end or datetime.today().strftime("%Y-%m-%d")
    df = yf.download(tickers, start=start, end=end, group_by='ticker', auto_adjust=False, progress=False)
    frames = []
    if isinstance(tickers, str) or len(tickers) == 1:
        tmp = df.reset_index().rename(columns=str.lower)
        tmp['ticker'] = tickers if isinstance(tickers, str) else tickers[0]
        tmp = tmp.rename(columns={'adj close': 'adj_close', 'date': 'trade_date'})
        frames.append(tmp[['ticker','trade_date','open','high','low','close','adj_close','volume']])
    else:
        for t in tickers:
            sub = df[t].reset_index().rename(columns=str.lower)
            sub['ticker'] = t
            sub = sub.rename(columns={'adj close': 'adj_close', 'date': 'trade_date'})
            frames.append(sub[['ticker','trade_date','open','high','low','close','adj_close','volume']])
    out = pd.concat(frames, ignore_index=True)
    out['trade_date'] = pd.to_datetime(out['trade_date'])
    out['year'] = out['trade_date'].dt.year
    out['month'] = out['trade_date'].dt.month
    return out.sort_values(['ticker','trade_date'])

def write_parquet_partitioned(df: pd.DataFrame, base_dir: str = DATA_DIR):
    base = Path(base_dir)
    for (y, m), part in df.groupby([df['year'], df['month']]):
        p = base / f"bronze/prices/year={y}/month={m:02d}"
        p.mkdir(parents=True, exist_ok=True)
        fname = p / f"prices_{y}_{m:02d}.parquet"
        part.drop(columns=['year','month']).to_parquet(fname, index=False)
        print("Wrote:", fname)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--tickers", nargs="+", default=TICKERS)
    parser.add_argument("--start", default="2010-01-01")
    parser.add_argument("--end", default=None)
    args = parser.parse_args()
    df = fetch_daily_history(args.tickers, start=args.start, end=args.end)
    write_parquet_partitioned(df)
    print("Bronze salvo em", DATA_DIR)
