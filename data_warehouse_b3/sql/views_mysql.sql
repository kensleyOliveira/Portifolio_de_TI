USE b3dw;

-- ============================
-- Views para BI / Analytics
-- ============================

-- 1) Preços ajustados (com dimensão de setor e bolsa)
CREATE OR REPLACE VIEW v_price AS
SELECT 
    d.date_id,
    d.year,
    d.month,
    d.quarter,
    a.ticker,
    a.class,
    s.sector_name,
    s.subsector,
    s.segment,
    e.name  AS exchange_name,
    e.mic   AS exchange_mic,
    fp.adj_close,
    fp.volume
FROM fact_price fp
JOIN dim_date d        ON d.date_id   = fp.date_id
JOIN dim_asset a       ON a.asset_id  = fp.asset_id
LEFT JOIN dim_sector s ON s.sector_id = a.sector_id
LEFT JOIN dim_exchange e ON e.exchange_id = fp.exchange_id;


-- 2) Retornos diários
CREATE OR REPLACE VIEW v_returns AS
SELECT 
    r.date_id,
    d.year,
    d.month,
    a.ticker,
    r.ret_simple,
    r.ret_log
FROM metrics_returns r
JOIN dim_date d  ON d.date_id = r.date_id
JOIN dim_asset a ON a.asset_id = r.asset_id;


-- 3) Volatilidade 21 dias
CREATE OR REPLACE VIEW v_vol_21d AS
SELECT
    v.date_id,
    YEAR(v.date_id) AS year,
    MONTH(v.date_id) AS month,
    a.ticker,
    COALESCE(v.vol_21d, 0) AS vol_21d
FROM metrics_vol_21d v
JOIN dim_asset a ON a.asset_id = v.asset_id;


-- 4) Dividendos
CREATE OR REPLACE VIEW v_dividends AS
SELECT 
    a.ticker,
    d.date_id,
    f.pay_date,
    f.ex_date,
    f.amount_per_share,
    f.type
FROM fact_dividend f
JOIN dim_asset a ON a.asset_id = f.asset_id
LEFT JOIN dim_date d ON d.date_id = f.pay_date;


-- 5) Splits
CREATE OR REPLACE VIEW v_splits AS
SELECT 
    a.ticker,
    f.ex_date,
    f.split_ratio
FROM fact_split f
JOIN dim_asset a ON a.asset_id = f.asset_id;


-- 6) Dashboard consolidado (preço + retorno + vol + dividendos)
CREATE OR REPLACE VIEW v_dashboard AS
SELECT 
    p.date_id,
    p.year,
    p.month,
    p.quarter,
    p.ticker,
    p.sector_name,
    p.exchange_name,
    p.adj_close,
    p.volume,
    r.ret_simple,
    v.vol_21d,
    d.amount_per_share AS dividend
FROM v_price p
LEFT JOIN v_returns r   ON p.ticker = r.ticker AND p.date_id = r.date_id
LEFT JOIN v_vol_21d v   ON p.ticker = v.ticker AND p.date_id = v.date_id
LEFT JOIN v_dividends d ON p.ticker = d.ticker AND p.date_id = d.date_id;

USE b3dw;

-- ===========================
-- 07) Drawdown
-- ===========================

CREATE OR REPLACE VIEW v_drawdown AS
WITH base AS (
    SELECT
        fp.date_id,
        a.ticker,
        fp.asset_id,
        fp.adj_close,
        -- Retorno acumulado em relação ao primeiro preço do ativo
        fp.adj_close / FIRST_VALUE(fp.adj_close) OVER (
            PARTITION BY fp.asset_id ORDER BY fp.date_id
        ) - 1 AS cum_return
    FROM fact_price fp
    JOIN dim_asset a ON a.asset_id = fp.asset_id
),
dd AS (
    SELECT
        date_id,
        ticker,
        asset_id,
        cum_return,
        -- Máximo acumulado até o dia
        MAX(cum_return) OVER (
            PARTITION BY asset_id ORDER BY date_id ROWS UNBOUNDED PRECEDING
        ) AS cum_max
    FROM base
)
SELECT
    date_id,
    ticker,
    cum_return,
    (cum_return - cum_max) / NULLIF(cum_max, 0) AS drawdown
FROM dd;

-- ===========================
-- 08) Heatmap de Retornos (mês x ano)
-- ===========================
CREATE OR REPLACE VIEW v_heatmap_returns AS
SELECT
    a.ticker,
    YEAR(r.date_id) AS year,
    MONTH(r.date_id) AS month,
    AVG(r.ret_simple) AS monthly_return
FROM metrics_returns r
JOIN dim_asset a ON a.asset_id = r.asset_id
GROUP BY a.ticker, YEAR(r.date_id), MONTH(r.date_id);


-- ===========================
-- 09) Retorno Médio dos Ativos (mensal)
-- ===========================
CREATE OR REPLACE VIEW v_asset_returns AS
SELECT
    a.ticker,
    YEAR(r.date_id) AS year,
    MONTH(r.date_id) AS month,
    AVG(r.ret_simple) AS avg_return
FROM metrics_returns r
JOIN dim_asset a ON a.asset_id = r.asset_id
GROUP BY a.ticker, YEAR(r.date_id), MONTH(r.date_id);


-- ===========================
-- 10) Retorno Acumulado
-- ===========================

CREATE OR REPLACE VIEW v_cum_returns AS
WITH base AS (
    SELECT
        r.date_id,
        a.ticker,
        r.asset_id,
        r.ret_simple
    FROM metrics_returns r
    JOIN dim_asset a ON a.asset_id = r.asset_id
),
log_ret AS (
    SELECT
        date_id,
        ticker,
        asset_id,
        -- usar log(1+r) para acumular
        LN(1 + ret_simple) AS log_ret
    FROM base
    WHERE ret_simple IS NOT NULL
),
cum_log AS (
    SELECT
        date_id,
        ticker,
        asset_id,
        SUM(log_ret) OVER (PARTITION BY asset_id ORDER BY date_id ROWS UNBOUNDED PRECEDING) AS cum_log
    FROM log_ret
)
SELECT
    date_id,
    ticker,
    EXP(cum_log) - 1 AS cum_return
FROM cum_log;

