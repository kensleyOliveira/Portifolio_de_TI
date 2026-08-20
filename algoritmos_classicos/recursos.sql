-- Seleciona o banco de dados para uso
USE astrosim;

-- -----------------------------------------------------
-- Tabelas para: 1. Problema do Troco (Mercador B2B)
-- -----------------------------------------------------

-- Armazena os "tipos" de unidades de recurso (as "moedas")
CREATE TABLE UnidadesRecurso (
    id_unidade INT PRIMARY KEY AUTO_INCREMENT,
    nome_recurso VARCHAR(100) NOT NULL COMMENT 'Ex: Credito Imperial, Barra de Iridio, Chip de Dados',
    valor_unitario DECIMAL(10, 2) NOT NULL COMMENT 'O valor de cada unidade'
);

-- Log de transações B2B para rastrear o troco
CREATE TABLE LogTransacoesB2B (
    id_transacao INT PRIMARY KEY AUTO_INCREMENT,
    id_mercador_vendedor INT NOT NULL,
    id_mercador_comprador INT NOT NULL,
    valor_total_devido DECIMAL(15, 2) NOT NULL,
    valor_total_pago DECIMAL(15, 2) NOT NULL,
    valor_troco_calculado DECIMAL(15, 2) NOT NULL,
    data_transacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserção de dados de exemplo para o Troco (Denominações)
INSERT INTO UnidadesRecurso (nome_recurso, valor_unitario) VALUES
('Credito Imperial Supremo', 1000.00),
('Credito Imperial Maior', 500.00),
('Credito Imperial', 100.00),
('Barra de Iridio', 50.00),
('Fragmento de Platina', 10.00),
('Chip de Dados', 5.00),
('Componente Basico', 1.00);


-- -----------------------------------------------------
-- Tabelas para: 2. Escalonamento de Intervalos (Agenda de Missões)
-- -----------------------------------------------------

CREATE TABLE MissoesExploracao (
    id_missao INT PRIMARY KEY AUTO_INCREMENT,
    nome_missao VARCHAR(255) NOT NULL,
    planeta_alvo VARCHAR(100),
    data_missao DATE,
    tempo_inicio INT NOT NULL COMMENT 'Hora (ou unidade de tempo) de início',
    tempo_fim INT NOT NULL COMMENT 'Hora (ou unidade de tempo) de término',
    recompensa_valor DECIMAL(12, 2)
);

DROP TABLE MissoesExploracao;

-- Tabela para armazenar a agenda otimizada do explorador
CREATE TABLE AgendaExplorador (
    id_agendamento INT PRIMARY KEY AUTO_INCREMENT,
    id_explorador INT NOT NULL,
    id_missao_selecionada INT NOT NULL,
    data_agendamento DATE,
    FOREIGN KEY (id_missao_selecionada) REFERENCES MissoesExploracao(id_missao)
);

DROP TABLE AgendaExplorador;

-- Inserção de dados de exemplo para Missões
INSERT INTO MissoesExploracao (nome_missao, planeta_alvo, data_missao, tempo_inicio, tempo_fim, recompensa_valor) VALUES
('Scan de Ruínas Antigas', 'Aethel', '2025-09-21', 0, 6, 5000),
('Coleta Rápida em Xylos', 'Xylos', '2025-09-22', 1, 4, 1000),
('Extração de Gás Vesper', 'Vesper-3', '2025-09-23', 5, 7, 2500),
('Patrulha de Cinturão', 'Sistema Local', '2025-09-24', 3, 8, 3000),
('Resgate de Sonda', 'Orbita de Xylos', '2025-09-25', 5, 9, 4000),
('Análise de Flora', 'Aethel', '2025-09-26', 8, 12, 6000),
('Entrega de Carga', 'Estação Central', '2025-09-27', 6, 10, 3500),
('Mapeamento de Cavernas', 'Xylos Prime', '2025-09-21', 9, 13, 2200),
('Investigação de Anomalia', 'Setor Proibido', '2025-09-22', 11, 15, 7500),
('Reparo de Satélite', 'Órbita Terrestre', '2025-09-23', 14, 16, 3000),
('Coleta de Amostras', 'Lua de Kratos', '2025-09-24', 12, 17, 4500),
('Defesa de Posto Avançado', 'Zetaris-9', '2025-09-25', 10, 18, 9000),
('Extração de Iridium', 'Campo de Asteroides', '2025-09-26', 16, 20, 5500),
('Scan Geológico', 'Pyroxia', '2025-09-27', 17, 22, 3800),
('Resgate de Mineração', 'Vesper-3', '2025-09-21', 19, 23, 6200),
('Patrulha de Rota Comercial', 'Estação Central', '2025-09-22', 20, 25, 4000),
('Estudo de Fauna', 'Aethel', '2025-09-23', 21, 26, 3300),
('Recuperação de Carga Preta', 'Campo de Detritos', '2025-09-24', 18, 24, 8000),
('Manutenção de Gerador', 'Base Lunar', '2025-09-25', 23, 27, 2000),
('Investigação de Sinal', 'Nebulosa Fantasma', '2025-09-26', 25, 30, 7000),
('Coleta de Cristais de Energia', 'Xylos', '2025-09-27', 26, 29, 4800),
('Acompanhamento de Comboio', 'Sistema Local', '2025-09-21', 24, 31, 5100),
('Análise Atmosférica', 'Pyroxia', '2025-09-22', 28, 32, 4200),
('Mapeamento de Setor Pirata', 'Setor Proibido', '2025-09-23', 27, 34, 9500),
('Extração de Água Pesada', 'Lua de Kratos', '2025-09-24', 30, 35, 5300),
('Patrulha de Defesa', 'Zetaris-9', '2025-09-25', 31, 36, 4700),
('Scan de Assinatura Warp', 'Nebulosa Fantasma', '2025-09-26', 33, 37, 6800),
('Entrega de Suprimentos', 'Base Lunar', '2025-09-27', 32, 34, 1500),
('Reparo de Escudos', 'Estação Central', '2025-09-21', 35, 39, 3900),
('Coleta de Dados de Supernova', 'Setor Proibido', '2025-09-22', 30, 40, 10000),
('Resgate de Tripulação', 'Campo de Detritos', '2025-09-23', 37, 42, 8800),
('Investigação de Artefato', 'Aethel', '2025-09-24', 38, 43, 7100),
('Patrulha Rápida', 'Sistema Local', '2025-09-25', 39, 41, 1800),
('Extração de Xenônio', 'Vesper-3', '2025-09-26', 36, 44, 5900),
('Mapeamento de Rotas Seguras', 'Campo de Asteroides', '2025-09-27', 40, 46, 6300),
('Análise de Ruínas Navais', 'Campo de Detritos', '2025-09-21', 41, 47, 7700),
('Coleta de Amostras Raras', 'Xylos Prime', '2025-09-22', 42, 45, 4900),
('Scan de Interferência', 'Zetaris-9', '2025-09-23', 43, 48, 3600),
('Patrulha Final do Ciclo', 'Estação Central', '2025-09-24', 45, 49, 2500),
('Entrega Urgente', 'Base Lunar', '2025-09-25', 46, 48, 2200),
('Coleta de Esporos', 'Aethel', '2025-09-26', 47, 50, 3100),
('Leitura de Sensor Remoto', 'Pyroxia', '2025-09-27', 44, 51, 4100),
('Extração de Emergência', 'Lua de Kratos', '2025-09-21', 49, 53, 5600),
('Investigação de Sonda Caída', 'Xylos', '2025-09-22', 48, 54, 6600),
('Mapeamento de Correntes', 'Nebulosa Fantasma', '2025-09-23', 50, 56, 7300),
('Reparo de Comunicações', 'Zetaris-9', '2025-09-24', 52, 55, 2900),
('Coleta de Gás Nobre', 'Vesper-3', '2025-09-25', 51, 57, 5400),
('Patrulha de Fronteira', 'Setor Proibido', '2025-09-26', 53, 59, 8200),
('Scan de Ninho Alienígena', 'Aethel', '2025-09-27', 55, 60, 9200),
('Última Carga do Dia', 'Estação Central', '2025-09-21', 58, 60, 2000);


-- -----------------------------------------------------
-- Tabelas para: 3. Mochila Fracionário (Coleta em Zona de Perigo)
-- -----------------------------------------------------

CREATE TABLE AmostrasMinerio (
    id_amostra INT PRIMARY KEY AUTO_INCREMENT,
    nome_minerio VARCHAR(100) NOT NULL,
    localizacao_zona VARCHAR(100),
    peso_disponivel_kg DECIMAL(10, 2) NOT NULL,
    valor_total_disponivel DECIMAL(10, 2) NOT NULL
);

-- Armazena a "carga" (o que foi pego) pelo explorador
CREATE TABLE CargaExplorador (
    id_carga INT PRIMARY KEY AUTO_INCREMENT,
    id_explorador INT NOT NULL,
    id_amostra_coletada INT NOT NULL,
    peso_coletado_kg DECIMAL(10, 2) NOT NULL,
    valor_proporcional_coletado DECIMAL(10, 2) NOT NULL,
    data_coleta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_amostra_coletada) REFERENCES AmostrasMinerio(id_amostra)
);

-- Inserção de dados de exemplo para Minérios (Mochila)
INSERT INTO AmostrasMinerio (nome_minerio, localizacao_zona, peso_disponivel_kg, valor_total_disponivel) VALUES
('Zytronium Bruto', 'Caverna Eco', 10.0, 600.00),
('Cristal Pylon', 'Ravina Sombria', 20.0, 1000.00),
('Isótopo-Delta', 'Cratera de Impacto', 30.0, 1200.00),
('Ferro Comum', 'Depósito de Superfície', 200.0, 1000.00),
('Nódulo de Cobalto', 'Geleira Instável', 50.0, 1500.00),
('Barra de Iridium', 'Campo de Detritos K-7', 15.0, 900.00),
('Gema de Quantum', 'O Olho da Tempestade', 2.0, 400.00),
('Pó de Hélio-3', 'Vulcão Adormecido', 5.0, 450.00),
('Fragmento de Titânio', 'Mina Abandonada 3', 100.0, 2500.00),
('Liga de Adamantium', 'Laboratório Secreto', 8.0, 720.00),
('Antiméria Pura', 'Núcleo do Reator Caído', 1.0, 180.00),
('Cobre Bruto', 'Planalto Arrasado', 150.0, 2250.00),
('Cristal de Energia', 'Ninho de Thresher', 25.0, 1125.00),
('Minério de Thorium', 'Fossa Radioativa', 40.0, 2200.00),
('Urânio Enriquecido', 'Usina Desativada', 12.0, 960.00),
('Platina Nativa', 'Rio de Lava Seco', 18.0, 900.00),
('Ouro de Tolo', 'Caverna de Cristal Falso', 70.0, 700.00),
('Opala de Fogo', 'Gêiseres de Pyroxia', 7.0, 490.00),
('Pedra Rúnica Antiga', 'Ruínas de Aethel', 3.0, 330.00),
('Composto de Xenônio', 'Atmosfera de Vesper', 22.0, 660.00),
('Pérola de Krayt', 'Deserto de Ossos', 0.5, 75.00),
('Silício de Alta Pureza', 'Praias de Vidro', 60.0, 1200.00),
('Bauxita de Baixa Qualidade', 'Colinas de Argila', 300.0, 1800.00),
('Nódulo de Vibranium', 'Meteoro Caído', 4.0, 500.00),
('Cristal de Gelo Eterno', 'Pico Congelado', 35.0, 1050.00),
('Amostra de Biomatéria', 'Pântano de Zetaris', 14.0, 700.00),
('Rocha Fosfórica', 'Campos de Cinzas', 80.0, 1600.00),
('Minério de Mithril', 'Montanhas Nebulosas', 9.0, 810.00),
('Fragmento de Sol Negro', 'Zona de Distorção', 1.5, 225.00),
('Isótopo de Césio', 'Depósito de Lixo Tóxico', 28.0, 1400.00),
('Diamante Industrial', 'Pressão Extrema', 50.0, 2750.00),
('Carvão Ativado', 'Floresta Petrificada', 120.0, 1200.00),
('Estanho Comum', 'Vale do Rio Seco', 90.0, 1350.00),
('Mercúrio Volátil', 'Lagoa Quimica', 13.0, 520.00),
('Pó de Estrela', 'Cinturão de Orion', 0.2, 50.00),
('Cristal de Eco', 'Caverna Eco (Profunda)', 6.0, 420.00),
('Fragmento de Ônix', 'Ravina Sombria (Fundo)', 45.0, 1800.00),
('Ametista de Vesper', 'Geodos de Vesper-3', 19.0, 760.00),
('Níquel Refinado', 'Instalação de Mineração', 75.0, 3000.00),
('Pedra-do-Sol', 'Templo Solar Caído', 2.5, 200.00),
('Minério de Oricalco', 'Atlântida Perdida', 11.0, 990.00),
('Prata Bruta', 'Veio de Prata', 33.0, 1485.00),
('Lítio de Bateria', 'Salar de Kratos', 26.0, 910.00),
('Magnésio Instável', 'Zona de Combustão', 16.0, 640.00),
('Grama de Osmium', 'Núcleo de Meteoro', 0.1, 19.00),
('Escória de Aço', 'Ruínas Industriais', 500.0, 2500.00),
('Paládio Raro', 'Posto Avançado K-4', 17.0, 1190.00),
('Componente de Sonda', 'Sonda Caída', 38.0, 1330.00),
('Zinco Comum', 'Depósito Rochoso', 110.0, 1650.00),
('Cristal de Alma', 'Cemitério de Naves', 3.5, 420.00);


