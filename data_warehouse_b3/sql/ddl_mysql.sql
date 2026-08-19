USE b3dw;

-- dim_date
CREATE TABLE IF NOT EXISTS dim_date (
  date_id DATE PRIMARY KEY,
  year INT,
  quarter INT,
  month INT,
  day INT,
  weekday INT,
  is_business BOOLEAN,
  is_holiday BOOLEAN
) ENGINE=InnoDB;

-- dim_exchange
CREATE TABLE IF NOT EXISTS dim_exchange (
  exchange_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  mic VARCHAR(16),
  timezone VARCHAR(64),
  UNIQUE KEY uq_exchange_name (name)
) ENGINE=InnoDB;

-- dim_sector
CREATE TABLE IF NOT EXISTS dim_sector (
  sector_id INT AUTO_INCREMENT PRIMARY KEY,
  sector_name VARCHAR(200) NOT NULL,
  subsector VARCHAR(200),
  segment VARCHAR(200),
  UNIQUE KEY uq_sector_name (sector_name)
) ENGINE=InnoDB;

-- dim_asset
CREATE TABLE IF NOT EXISTS dim_asset (
  asset_id INT AUTO_INCREMENT PRIMARY KEY,
  ticker VARCHAR(32) NOT NULL UNIQUE,
  isin VARCHAR(32),
  class VARCHAR(32),
  currency VARCHAR(8) DEFAULT 'BRL',
  sector_id INT,
  listed_at DATE,
  delisted_at DATE,
  FOREIGN KEY (sector_id) REFERENCES dim_sector(sector_id)
) ENGINE=InnoDB;

-- staging
CREATE TABLE IF NOT EXISTS stg_prices (
  ticker VARCHAR(32),
  trade_date DATETIME,
  open DECIMAL(18,6),
  high DECIMAL(18,6),
  low DECIMAL(18,6),
  close DECIMAL(18,6),
  adj_close DECIMAL(18,6),
  volume BIGINT,
  PRIMARY KEY (ticker, trade_date)
) ENGINE=InnoDB;

-- fact_price
CREATE TABLE IF NOT EXISTS fact_price (
  asset_id INT,
  date_id DATE,
  exchange_id INT,
  open DECIMAL(18,6),
  high DECIMAL(18,6),
  low DECIMAL(18,6),
  close DECIMAL(18,6),
  adj_close DECIMAL(18,6),
  volume BIGINT,
  PRIMARY KEY (asset_id, date_id),
  FOREIGN KEY (asset_id) REFERENCES dim_asset(asset_id),
  FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
  FOREIGN KEY (exchange_id) REFERENCES dim_exchange(exchange_id)
) ENGINE=InnoDB;

-- fact_dividend
CREATE TABLE IF NOT EXISTS fact_dividend (
  asset_id INT,
  pay_date DATE,
  ex_date DATE,
  record_date DATE,
  amount_per_share DECIMAL(18,6),
  type VARCHAR(32),
  PRIMARY KEY (asset_id, pay_date, ex_date),
  FOREIGN KEY (asset_id) REFERENCES dim_asset(asset_id)
) ENGINE=InnoDB;

-- fact_split
CREATE TABLE IF NOT EXISTS fact_split (
  asset_id INT,
  ex_date DATE,
  split_ratio DECIMAL(18,6),
  PRIMARY KEY (asset_id, ex_date),
  FOREIGN KEY (asset_id) REFERENCES dim_asset(asset_id)
) ENGINE=InnoDB;
