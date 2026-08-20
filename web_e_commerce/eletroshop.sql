use eletroshop;

CREATE TABLE clientes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(255) NOT NULL,
  endereco VARCHAR(255) NOT NULL,
  cpf VARCHAR(14) NOT NULL UNIQUE,
  data_nascimento DATE NOT NULL,
  data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela para armazenar cada venda (pedido)
CREATE TABLE vendas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  cliente_id INT NOT NULL,
  valor_total DECIMAL(10, 2) NOT NULL,
  metodo_pagamento VARCHAR(50),
  status VARCHAR(50) DEFAULT 'pendente_pagamento',
  data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

-- Tabela para armazenar os itens de cada venda
CREATE TABLE venda_itens (
  id INT AUTO_INCREMENT PRIMARY KEY,
  venda_id INT NOT NULL,
  produto_nome VARCHAR(255) NOT NULL,
  quantidade INT NOT NULL,
  valor_unitario DECIMAL(10, 2) NOT NULL,
  subtotal DECIMAL(10, 2) NOT NULL,
  FOREIGN KEY (venda_id) REFERENCES vendas(id)
);

SELECT CONSTRAINT_NAME 
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'eletroshop' AND TABLE_NAME = 'vendas';

ALTER TABLE vendas
DROP FOREIGN KEY vendas_ibfk_1;

ALTER TABLE vendas
ADD CONSTRAINT vendas_ibfk_1
FOREIGN KEY (cliente_id) REFERENCES clientes(id)
ON DELETE CASCADE;
venda_itensvendas
