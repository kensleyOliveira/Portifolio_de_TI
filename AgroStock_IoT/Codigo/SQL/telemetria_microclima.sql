USE agro_telemetria;

CREATE TABLE IF NOT EXISTS telemetria_microclima (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperatura FLOAT NOT NULL,
    umidade FLOAT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE USER IF NOT EXISTS 'root'@'%' IDENTIFIED BY 'mysql';

ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'mysql';

GRANT ALL PRIVILEGES ON agro_telemetria.* TO 'root'@'%';

FLUSH PRIVILEGES;

SELECT * FROM telemetria_microclima;