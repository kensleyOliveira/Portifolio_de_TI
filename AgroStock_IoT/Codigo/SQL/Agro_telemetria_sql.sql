CREATE DATABASE IF NOT EXISTS agro_telemetria;
USE agro_telemetria;

CREATE TABLE IF NOT EXISTS telemetria_microclima (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperatura FLOAT NOT NULL,
    umidade FLOAT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);