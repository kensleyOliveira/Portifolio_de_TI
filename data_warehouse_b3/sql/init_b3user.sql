-- Garante que está no banco correto
USE b3dw;

-- Garante que remove o antigo
DROP USER IF EXISTS 'b3user'@'localhost';

-- Cria o usuário válido para qualquer origem
CREATE USER 'b3user'@'%' IDENTIFIED WITH mysql_native_password BY 'b3pass';

-- Dá privilégios completos no banco b3dw
GRANT ALL PRIVILEGES ON b3dw.* TO 'b3user'@'%';

-- Aplica
FLUSH PRIVILEGES;

-- Conferir
SELECT user, host, plugin FROM mysql.user WHERE user='b3user';

-- ---------------------------------------------------------------------------------------------
-- Refazer
DROP USER 'b3user'@'%';

CREATE USER 'b3user'@'%' IDENTIFIED WITH mysql_native_password BY 'b3pass';

-- Dá privilégios completos no banco b3dw
GRANT ALL PRIVILEGES ON b3dw.* TO 'b3user'@'%';

-- Conferir
SELECT user, host, plugin FROM mysql.user WHERE user='b3user';

-- ---------------------------------------------------------------------------------------------
-- Remove qualquer definição antiga do usuário para garantir um início limpo
DROP USER IF EXISTS 'root'@'%';

DROP USER IF EXISTS 'root'@'172.26.0.1';

-- Conferir
SELECT user, host, plugin FROM mysql.user WHERE user='root';