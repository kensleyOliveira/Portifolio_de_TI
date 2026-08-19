USE b3dw;

-- ============================
-- Métricas (quase materialized views)
-- ============================

-- 1) Retornos diários (simples e log)
CREATE TABLE IF NOT EXISTS metrics_returns (
  asset_id   INT NOT NULL,
  date_id    DATE NOT NULL,
  ret_simple DOUBLE NULL,
  ret_log    DOUBLE NULL,
  PRIMARY KEY (asset_id, date_id),
  FOREIGN KEY (asset_id) REFERENCES dim_asset(asset_id),
  FOREIGN KEY (date_id)  REFERENCES dim_date(date_id)
) ENGINE=InnoDB;

-- Refresh dos retornos
REPLACE INTO metrics_returns (asset_id, date_id, ret_simple, ret_log)
SELECT
    fp.asset_id,
    fp.date_id,
    CASE
        WHEN LAG(fp.adj_close) OVER (PARTITION BY fp.asset_id ORDER BY fp.date_id) > 0.01
        -- FORÇAR CÁLCULO USANDO DOUBLE PARA EVITAR ESTOURO DE DECIMAL 👇
        THEN fp.adj_close / CAST(LAG(fp.adj_close) OVER (PARTITION BY fp.asset_id ORDER BY fp.date_id) AS DOUBLE) - 1
    END AS ret_simple,
    CASE
        WHEN fp.adj_close > 0.01 AND LAG(fp.adj_close) OVER (PARTITION BY fp.asset_id ORDER BY fp.date_id) > 0.01
        -- BOA PRÁTICA APLICAR O CAST AQUI TAMBÉM 👇
        THEN LN(CAST(fp.adj_close AS DOUBLE)) - LN(CAST(LAG(fp.adj_close) OVER (PARTITION BY fp.asset_id ORDER BY fp.date_id) AS DOUBLE))
    END AS ret_log
FROM fact_price fp;


-- 2) Volatilidade 21 dias (rolling std de retornos)
CREATE TABLE IF NOT EXISTS metrics_vol_21d (
  asset_id INT NOT NULL,
  date_id  DATE NOT NULL,
  vol_21d  DOUBLE NULL,
  PRIMARY KEY (asset_id, date_id),
  FOREIGN KEY (asset_id) REFERENCES dim_asset(asset_id),
  FOREIGN KEY (date_id)  REFERENCES dim_date(date_id)
) ENGINE=InnoDB;

-- Refresh da volatilidade
REPLACE INTO metrics_vol_21d (asset_id, date_id, vol_21d)
SELECT asset_id,
       date_id,
       STDDEV_SAMP(ret_simple) OVER (
         PARTITION BY asset_id
         ORDER BY date_id
         ROWS BETWEEN 20 PRECEDING AND CURRENT ROW
       ) AS vol_21d
FROM metrics_returns;



