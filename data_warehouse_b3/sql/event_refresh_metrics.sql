USE b3dw;

-- Habilitar o agendador de eventos (se ainda não estiver ativo)
SET GLOBAL event_scheduler = ON;

-- Criar evento para atualizar métricas diariamente às 20h (após fechamento da B3)
DELIMITER $$

CREATE EVENT IF NOT EXISTS ev_refresh_metrics
ON SCHEDULE EVERY 1 DAY
STARTS CURRENT_DATE + INTERVAL 20 HOUR
DO
BEGIN
  -- Atualizar retornos simples e logarítmicos
  REPLACE INTO metrics_returns (asset_id, date_id, ret_simple, ret_log)
  SELECT fp.asset_id,
         fp.date_id,
         CASE 
           WHEN LAG(fp.adj_close) OVER (PARTITION BY fp.asset_id ORDER BY fp.date_id) > 0
           THEN fp.adj_close / LAG(fp.adj_close) OVER (PARTITION BY fp.asset_id ORDER BY fp.date_id) - 1
         END AS ret_simple,
         CASE 
           WHEN LAG(fp.adj_close) OVER (PARTITION BY fp.asset_id ORDER BY fp.date_id) > 0
           THEN LN(fp.adj_close) - LN(LAG(fp.adj_close) OVER (PARTITION BY fp.asset_id ORDER BY fp.date_id))
         END AS ret_log
  FROM fact_price fp;

  -- Atualizar volatilidade 21 dias
  REPLACE INTO metrics_vol_21d (asset_id, date_id, vol_21d)
  SELECT asset_id,
         date_id,
         STDDEV_SAMP(ret_simple) OVER (
           PARTITION BY asset_id
           ORDER BY date_id
           ROWS BETWEEN 20 PRECEDING AND CURRENT ROW
         ) AS vol_21d
  FROM metrics_returns;
END$$

DELIMITER ;


SHOW EVENTS FROM b3dw;