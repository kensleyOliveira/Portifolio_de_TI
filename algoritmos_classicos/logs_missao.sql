-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Tempo de geração: 15/07/2025 às 00:38
-- Versão do servidor: 8.0.41
-- Versão do PHP: 8.2.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `astrosim`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `logs_missao`
--

CREATE TABLE `logs_missao` (
  `id` int NOT NULL,
  `data` datetime DEFAULT NULL,
  `mensagem` text COLLATE utf8mb4_general_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `logs_missao`
--

INSERT INTO `logs_missao` (`id`, `data`, `mensagem`) VALUES
(1, '2025-07-06 08:00:00', '[Sonda-2] Dados de Encélado sincronizados.'),
(2, '2025-07-06 08:02:00', '[Controle] Satélite posicionado sobre Titã.'),
(3, '2025-07-06 08:04:00', '[Controle] Iniciando análise espectral do solo marciano.'),
(4, '2025-07-06 08:06:00', '[Engenharia] Rotas de reentrada recalculadas com sucesso.'),
(5, '2025-07-06 08:08:00', '[Estação] Log completo de energia armazenado.'),
(6, '2025-07-06 08:10:00', '[Engenharia] Rotas de reentrada recalculadas com sucesso.'),
(7, '2025-07-06 08:12:00', '[Módulo Exo] Painéis solares totalmente estendidos.'),
(8, '2025-07-06 08:14:00', '[Estação] Log completo de energia armazenado.'),
(9, '2025-07-06 08:16:00', '[Robô-Minerador] Atividade subterrânea detectada em Encélado.'),
(10, '2025-07-06 08:18:00', '[Sistema] Anomalia detectada na unidade de propulsão.'),
(11, '2025-07-06 08:20:00', '[Engenharia] Rotas de reentrada recalculadas com sucesso.'),
(12, '2025-07-06 08:22:00', '[Câmera] Captura visual da superfície de Marte concluída.'),
(13, '2025-07-06 08:24:00', '[Controle] Transmissão criptografada ativada.'),
(14, '2025-07-06 08:26:00', '[Sonda-1] Aterrissagem bem-sucedida em Europa.'),
(15, '2025-07-06 08:28:00', '[Controle] Satélite posicionado sobre Titã.'),
(16, '2025-07-06 08:30:00', '[Módulo Exo] Painéis solares totalmente estendidos.'),
(17, '2025-07-06 08:32:00', '[Robô] Fóssil microscópico encontrado em solo úmido.'),
(18, '2025-07-06 08:34:00', '[Engenharia] Rotas de reentrada recalculadas com sucesso.'),
(19, '2025-07-06 08:36:00', '[Controle] Transmissão criptografada ativada.'),
(20, '2025-07-06 08:38:00', '[Sonda-1] Aterrissagem bem-sucedida em Europa.'),
(21, '2025-07-06 08:40:00', '[Sistema] Anomalia detectada na unidade de propulsão.'),
(22, '2025-07-06 08:42:00', '[Robô] Cavidade natural encontrada sob a crosta.'),
(23, '2025-07-06 08:44:00', '[Sonda-1] Aterrissagem bem-sucedida em Europa.'),
(24, '2025-07-06 08:46:00', '[Sonda-3] Comunicação estabelecida com módulo orbital.'),
(25, '2025-07-06 08:48:00', '[Sonda-4] Solo de Europa contém traços de perclorato.'),
(26, '2025-07-06 08:50:00', '[Controle] Iniciando análise espectral do solo marciano.'),
(27, '2025-07-06 08:52:00', '[Sensores] Variação magnética incomum em Ganimedes.'),
(28, '2025-07-06 08:54:00', '[Sistema] Anomalia detectada na unidade de propulsão.'),
(29, '2025-07-06 08:56:00', '[Sonda-4] Solo de Europa contém traços de perclorato.'),
(30, '2025-07-06 08:58:00', '[Robô-Minerador] Atividade subterrânea detectada em Encélado.'),
(31, '2025-07-06 09:00:00', '[Robô-Minerador] Atividade subterrânea detectada em Encélado.'),
(32, '2025-07-06 09:02:00', '[Robô] Fóssil microscópico encontrado em solo úmido.'),
(33, '2025-07-06 09:04:00', '[Robô-Minerador] Atividade subterrânea detectada em Encélado.'),
(34, '2025-07-06 09:06:00', '[Sonda-3] Comunicação estabelecida com módulo orbital.'),
(35, '2025-07-06 09:08:00', '[Módulo Exo] Painéis solares totalmente estendidos.'),
(36, '2025-07-06 09:10:00', '[Robô] Cavidade natural encontrada sob a crosta.'),
(37, '2025-07-06 09:12:00', '[Controle] Satélite posicionado sobre Titã.'),
(38, '2025-07-06 09:14:00', '[Missão] Nível de radiação em Titã dentro dos parâmetros.'),
(39, '2025-07-06 09:16:00', '[Sonda-4] Solo de Europa contém traços de perclorato.'),
(40, '2025-07-06 09:18:00', '[Transmissão] Dados enviados para o centro de controle.'),
(41, '2025-07-06 09:20:00', '[Sensores] Variação magnética incomum em Ganimedes.'),
(42, '2025-07-06 09:22:00', '[Controle] Transmissão criptografada ativada.'),
(43, '2025-07-06 09:24:00', '[Sonda-2] Dados de Encélado sincronizados.'),
(44, '2025-07-06 09:26:00', '[Controle] Iniciando análise espectral do solo marciano.'),
(45, '2025-07-06 09:28:00', '[Robô] Fóssil microscópico encontrado em solo úmido.'),
(46, '2025-07-06 09:30:00', '[Sonda-1] Aterrissagem segura em Europa confirmada.'),
(47, '2025-07-06 09:32:00', '[Sonda-2] Dados de Encélado sincronizados.'),
(48, '2025-07-06 09:34:00', '[Controle] Iniciando análise espectral do solo marciano.'),
(49, '2025-07-06 09:36:00', '[Robô-Minerador] Atividade subterrânea detectada em Encélado.'),
(50, '2025-07-06 09:38:00', '[Sonda-1] Aterrissagem segura em Europa confirmada.'),
(51, '2025-07-06 09:40:00', '[Sonda-2] Amostra coletada próxima ao cânion Valles Marineris.'),
(52, '2025-07-06 09:42:00', '[Sonda-1] Aterrissagem segura em Europa confirmada.'),
(53, '2025-07-06 09:44:00', '[Controle] Iniciando análise espectral do solo marciano.'),
(54, '2025-07-06 09:46:00', '[Sonda-3] Comunicação estabelecida com módulo orbital.'),
(55, '2025-07-06 09:48:00', '[Sonda-1] Aterrissagem bem-sucedida em Europa.'),
(56, '2025-07-06 09:50:00', '[Sistema] Anomalia detectada na unidade de propulsão.'),
(57, '2025-07-06 09:52:00', '[Controle] Satélite posicionado sobre Titã.'),
(58, '2025-07-06 09:54:00', '[Controle] Transmissão criptografada ativada.'),
(59, '2025-07-06 09:56:00', '[Estação] Log completo de energia armazenado.'),
(60, '2025-07-06 09:58:00', '[Controle] Satélite posicionado sobre Titã.'),
(61, '2025-07-06 10:00:00', '[Sonda-4] Solo de Europa contém traços de perclorato.'),
(62, '2025-07-06 10:02:00', '[Sonda-2] Dados de Encélado sincronizados.'),
(63, '2025-07-06 10:04:00', '[Sensores] Variação magnética incomum em Ganimedes.'),
(64, '2025-07-06 10:06:00', '[Sonda-4] Solo de Europa contém traços de perclorato.'),
(65, '2025-07-06 10:08:00', '[Robô] Cavidade natural encontrada sob a crosta.'),
(66, '2025-07-06 10:10:00', '[Sonda-4] Solo de Europa contém traços de perclorato.'),
(67, '2025-07-06 10:12:00', '[Sistema] Anomalia detectada na unidade de propulsão.'),
(68, '2025-07-06 10:14:00', '[Controle] Iniciando análise espectral do solo marciano.'),
(69, '2025-07-06 10:16:00', '[Sonda-1] Aterrissagem segura em Europa confirmada.'),
(70, '2025-07-06 10:18:00', '[Missão] Nível de radiação em Titã dentro dos parâmetros.'),
(71, '2025-07-06 10:20:00', '[Transmissão] Dados enviados para o centro de controle.'),
(72, '2025-07-06 10:22:00', '[Transmissão] Dados enviados para o centro de controle.'),
(73, '2025-07-06 10:24:00', '[Robô] Cavidade natural encontrada sob a crosta.'),
(74, '2025-07-06 10:26:00', '[Módulo Exo] Painéis solares totalmente estendidos.'),
(75, '2025-07-06 10:28:00', '[Sonda-3] Comunicação estabelecida com módulo orbital.'),
(76, '2025-07-06 10:30:00', '[Estação] Log completo de energia armazenado.'),
(77, '2025-07-06 10:32:00', '[Engenharia] Rotas de reentrada recalculadas com sucesso.'),
(78, '2025-07-06 10:34:00', '[Controle] Iniciando análise espectral do solo marciano.'),
(79, '2025-07-06 10:36:00', '[Missão] Nível de radiação em Titã dentro dos parâmetros.'),
(80, '2025-07-06 10:38:00', '[Sonda-1] Aterrissagem bem-sucedida em Europa.'),
(81, '2025-07-06 10:40:00', '[Módulo Exo] Painéis solares totalmente estendidos.'),
(82, '2025-07-06 10:42:00', '[Sonda-4] Solo de Europa contém traços de perclorato.'),
(83, '2025-07-06 10:44:00', '[Engenharia] Rotas de reentrada recalculadas com sucesso.'),
(84, '2025-07-06 10:46:00', '[Sonda-1] Aterrissagem bem-sucedida em Europa.'),
(85, '2025-07-06 10:48:00', '[Controle] Satélite posicionado sobre Titã.'),
(86, '2025-07-06 10:50:00', '[Controle] Satélite posicionado sobre Titã.'),
(87, '2025-07-06 10:52:00', '[Missão] Nível de radiação em Titã dentro dos parâmetros.'),
(88, '2025-07-06 10:54:00', '[Engenharia] Rotas de reentrada recalculadas com sucesso.'),
(89, '2025-07-06 10:56:00', '[Sonda-4] Solo de Europa contém traços de perclorato.'),
(90, '2025-07-06 10:58:00', '[Missão] Nível de radiação em Titã dentro dos parâmetros.'),
(91, '2025-07-06 11:00:00', '[Sonda-1] Aterrissagem bem-sucedida em Europa.'),
(92, '2025-07-06 11:02:00', '[Controle] Transmissão criptografada ativada.'),
(93, '2025-07-06 11:04:00', '[Sistema] Anomalia detectada na unidade de propulsão.'),
(94, '2025-07-06 11:06:00', '[Sistema] Anomalia detectada na unidade de propulsão.'),
(95, '2025-07-06 11:08:00', '[Sonda-2] Amostra coletada próxima ao cânion Valles Marineris.'),
(96, '2025-07-06 11:10:00', '[Robô] Cavidade natural encontrada sob a crosta.'),
(97, '2025-07-06 11:12:00', '[Sonda-3] Comunicação estabelecida com módulo orbital.'),
(98, '2025-07-06 11:14:00', '[Sonda-4] Solo de Europa contém traços de perclorato.'),
(99, '2025-07-06 11:16:00', '[Robô] Cavidade natural encontrada sob a crosta.'),
(100, '2025-07-06 11:18:00', '[Sonda-3] Comunicação estabelecida com módulo orbital.'),
(101, '2025-07-06 15:15:00', '[Sonda-2] Dados de Encélado sincronizados.');

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `logs_missao`
--
ALTER TABLE `logs_missao`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `logs_missao`
--
ALTER TABLE `logs_missao`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=102;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
