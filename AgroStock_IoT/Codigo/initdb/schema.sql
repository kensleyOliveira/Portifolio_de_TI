CREATE DATABASE IF NOT EXISTS agro_telemetria;
USE agro_telemetria;

CREATE TABLE IF NOT EXISTS telemetria_microclima (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperatura DECIMAL(5,2) NOT NULL,
    umidade DECIMAL(5,2) NOT NULL,
    timestamp DATETIME NOT NULL
);