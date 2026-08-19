
import numpy as np
import pandas as pd

TRADING_DAYS = 252

def compute_daily_returns(df_prices):
    """
    df_prices: DataFrame with columns ['ticker','date_id','adj_close']
    Returns DataFrame with columns ['ticker','date_id','adj_close','ret_simple','ret_log']
    """
    df = df_prices.copy()
    # ensure correct dtypes and sort
    df['date_id'] = pd.to_datetime(df['date_id'])
    df = df.sort_values(['ticker','date_id']).reset_index(drop=True)
    df['ret_simple'] = df.groupby('ticker')['adj_close'].pct_change()
    df['ret_log'] = df.groupby('ticker')['adj_close'].apply(lambda x: np.log(x) - np.log(x.shift(1)))
    return df

def metrics_per_asset(df_returns, rf_annual=0.0):
    """
    Recebe df_returns com ['ticker','date_id','ret_simple','ret_log']
    Retorna DataFrame com métricas por ticker:
      - ann_return, ann_vol, sharpe, max_drawdown, cum_return, n_obs
    """
    out = []
    for t, g in df_returns.groupby('ticker'):
        r = g['ret_simple'].dropna()
        if r.empty:
            out.append({
                'ticker': t,
                'ann_return': np.nan,
                'ann_vol': np.nan,
                'sharpe': np.nan,
                'max_drawdown': np.nan,
                'cum_return': np.nan,
                'n_obs': 0
            })
            continue

        mean_d = r.mean()
        vol_d = r.std(ddof=1)
        ann_return = (1 + mean_d) ** TRADING_DAYS - 1
        ann_vol = vol_d * np.sqrt(TRADING_DAYS)
        sharpe = (ann_return - rf_annual) / ann_vol if ann_vol > 0 else np.nan

        # cum return
        cum_return = (1 + r).prod() - 1

        # max drawdown: compute wealth index
        wealth = (1 + r).cumprod()
        peak = wealth.cummax()
        drawdown = (wealth - peak) / peak
        max_dd = drawdown.min()  # most negative

        out.append({
            'ticker': t,
            'ann_return': ann_return,
            'ann_vol': ann_vol,
            'sharpe': sharpe,
            'max_drawdown': max_dd,
            'cum_return': cum_return,
            'n_obs': len(r)
        })

    metrics_df = pd.DataFrame(out).set_index('ticker')
    return metrics_df

def compute_cov_matrix(df_returns, tickers=None):
    """
    Retorna (df_pivot, mean_daily, cov_annual)
    df_returns: DataFrame from compute_daily_returns (contains ret_simple)
    tickers: optional list to fix column order
    """
    df_pivot = df_returns.pivot(index='date_id', columns='ticker', values='ret_simple')
    if tickers:
        # keep only provided tickers and maintain order
        cols = [c for c in tickers if c in df_pivot.columns]
        df_pivot = df_pivot[cols]
    # drop rows where all are NaN
    df_pivot = df_pivot.dropna(how='all')
    mean_daily = df_pivot.mean()
    cov_daily = df_pivot.cov()
    cov_annual = cov_daily * TRADING_DAYS
    return df_pivot, mean_daily, cov_annual

def min_variance_weights(cov):
    """
    cov: covariance matrix (pandas DataFrame)
    Retorna weights (Series) for minimum variance portfolio (no short-constraints)
    """
    # handle singular matrices with pseudo-inverse
    inv = np.linalg.pinv(cov.values)
    ones = np.ones(inv.shape[0])
    w = inv.dot(ones)
    w = w / w.sum()
    return pd.Series(w, index=cov.index)

def weights_proportional_to_return(mean_returns):
    """
    mean_returns: Series of mean returns (can be annualized)
    returns normalized non-negative weights (if all <=0 fallback to equal weights)
    """
    v = mean_returns.copy().astype(float)
    v = v.clip(lower=0)
    if v.sum() == 0 or v.isna().all():
        n = len(v)
        return pd.Series(np.ones(n) / n, index=v.index)
    return v / v.sum()

def propose_portfolios(mean_annual, cov_annual):
    """
    mean_annual: Series (annualized returns)
    cov_annual: DataFrame (annual covariance matrix)
    Retorna dict com weights for 'conservative','moderate','aggressive'
    conservative: min variance
    moderate: average of minvar and proportional-to-return
    aggressive: proportional to return
    """
    minvar = min_variance_weights(cov_annual)
    prop = weights_proportional_to_return(mean_annual)
    moderate = 0.5 * minvar + 0.5 * prop
    # ensure non-negative and normalize
    moderate = moderate.clip(lower=0)
    if moderate.sum() == 0:
        moderate = pd.Series(np.ones(len(prop)) / len(prop), index=prop.index)
    else:
        moderate = moderate / moderate.sum()

    aggressive = prop.copy()
    # sanitize NaNs and normalize
    for s in [minvar, moderate, aggressive]:
        s[s.isna()] = 0.0
        if s.sum() != 0:
            s[:] = s / s.sum()
        else:
            s[:] = 1.0 / len(s)

    return {'conservative': minvar, 'moderate': moderate, 'aggressive': aggressive}

def portfolio_stats(weights, mean_annual, cov_annual, rf_annual=0.0):
    """
    weights: Series aligned with mean_annual.index and cov_annual.index
    Retorna dict com 'ret', 'vol', 'sharpe'
    """
    w = weights.values
    ret = float(np.dot(w, mean_annual.values))
    vol = float(np.sqrt(w @ cov_annual.values @ w))
    sharpe = (ret - rf_annual) / vol if vol > 0 else np.nan
    return {'ret': ret, 'vol': vol, 'sharpe': sharpe}
