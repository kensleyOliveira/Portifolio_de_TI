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
-- Estrutura para tabela `inventario_espacial`
--

CREATE TABLE `inventario_espacial` (
  `id` int NOT NULL,
  `cod_invent` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nome` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `categoria` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `massa` int DEFAULT NULL,
  `consumo` decimal(5,2) DEFAULT NULL,
  `id_log` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `inventario_espacial`
--

INSERT INTO `inventario_espacial` (`id`, `cod_invent`, `nome`, `categoria`, `massa`, `consumo`, `id_log`) VALUES
(1, 'CMP001', 'OBC ARM Cortex', 'Controle', 310, 8.11, 1),
(2, 'CMP002', 'Transponder X-Band', 'Comunicação', 498, 6.18, 2),
(3, 'CMP003', 'Bateria Li-Ion 50Wh', 'Energia', 759, 7.45, 3),
(4, 'CMP004', 'Star Tracker', 'Navegação', 741, 4.43, 4),
(5, 'CMP005', 'Radiômetro', 'Instrumentação', 477, 13.58, 5),
(6, 'CMP006', 'Painel Estrutural de Alumínio', 'Estrutura', 783, 3.62, 6),
(7, 'CMP007', 'Sensor de Temperatura', 'Sensores', 326, 0.86, 7),
(8, 'CMP008', 'Fusível Térmico', 'Diagnóstico', 819, 1.91, 8),
(9, 'CMP009', 'OBC ARM Cortex', 'Controle', 247, 6.13, 9),
(10, 'CMP010', 'Receptor VHF', 'Comunicação', 155, 11.48, 10),
(11, 'CMP011', 'Bateria Li-Ion 50Wh', 'Energia', 209, 2.38, 11),
(12, 'CMP012', 'Magnetômetro Digital', 'Navegação', 830, 7.87, 12),
(13, 'CMP013', 'Radiômetro', 'Instrumentação', 196, 11.09, 13),
(14, 'CMP014', 'MLI Térmico', 'Estrutura', 519, 12.50, 14),
(15, 'CMP015', 'Sensor de Radiação', 'Sensores', 939, 12.13, 15),
(16, 'CMP016', 'Memória Flash Redundante', 'Diagnóstico', 328, 4.46, 16),
(17, 'CMP017', 'OBC ARM Cortex', 'Controle', 400, 8.86, 17),
(18, 'CMP018', 'Receptor VHF', 'Comunicação', 582, 6.63, 18),
(19, 'CMP019', 'PDU Básico', 'Energia', 990, 6.48, 19),
(20, 'CMP020', 'Star Tracker', 'Navegação', 422, 13.89, 20),
(21, 'CMP021', 'Radiômetro', 'Instrumentação', 463, 7.52, 21),
(22, 'CMP022', 'Painel Estrutural de Alumínio', 'Estrutura', 631, 3.22, 22),
(23, 'CMP023', 'Sensor de Pressão', 'Sensores', 541, 10.57, 23),
(24, 'CMP024', 'Fusível Térmico', 'Diagnóstico', 372, 8.72, 24),
(25, 'CMP025', 'OBC ARM Cortex', 'Controle', 101, 0.63, 25),
(26, 'CMP026', 'Modulador Digital', 'Comunicação', 526, 12.91, 26),
(27, 'CMP027', 'Conversor DC-DC 12V', 'Energia', 751, 1.01, 27),
(28, 'CMP028', 'Star Tracker', 'Navegação', 981, 13.60, 28),
(29, 'CMP029', 'Espectrômetro IR', 'Instrumentação', 503, 9.13, 29),
(30, 'CMP030', 'Painel Estrutural de Alumínio', 'Estrutura', 451, 5.25, 30),
(31, 'CMP031', 'Sensor de Temperatura', 'Sensores', 324, 9.02, 31),
(32, 'CMP032', 'Memória Flash Redundante', 'Diagnóstico', 177, 9.33, 32),
(33, 'CMP033', 'RTU Modular', 'Controle', 959, 3.86, 33),
(34, 'CMP034', 'Transponder X-Band', 'Comunicação', 166, 4.98, 34),
(35, 'CMP035', 'Bateria Li-Ion 50Wh', 'Energia', 855, 11.26, 35),
(36, 'CMP036', 'Giroscópio MEMS', 'Navegação', 638, 9.47, 36),
(37, 'CMP037', 'Espectrômetro IR', 'Instrumentação', 335, 1.64, 37),
(38, 'CMP038', 'Painel Estrutural de Alumínio', 'Estrutura', 140, 3.41, 38),
(39, 'CMP039', 'Sensor de Radiação', 'Sensores', 760, 6.39, 39),
(40, 'CMP040', 'Porta JTAG', 'Diagnóstico', 127, 10.93, 40),
(41, 'CMP041', 'RTU Modular', 'Controle', 523, 10.09, 41),
(42, 'CMP042', 'Receptor VHF', 'Comunicação', 477, 5.47, 42),
(43, 'CMP043', 'Conversor DC-DC 12V', 'Energia', 240, 5.24, 43),
(44, 'CMP044', 'Giroscópio MEMS', 'Navegação', 861, 9.26, 44),
(45, 'CMP045', 'Radiômetro', 'Instrumentação', 679, 12.59, 45),
(46, 'CMP046', 'MLI Térmico', 'Estrutura', 689, 1.96, 46),
(47, 'CMP047', 'Acelerômetro', 'Sensores', 128, 10.63, 47),
(48, 'CMP048', 'Porta JTAG', 'Diagnóstico', 326, 0.65, 48),
(49, 'CMP049', 'Watchdog Timer', 'Controle', 298, 8.13, 49),
(50, 'CMP050', 'Antena Helicoidal', 'Comunicação', 594, 1.48, 50),
(51, 'CMP051', 'PDU Básico', 'Energia', 497, 8.85, 51),
(52, 'CMP052', 'Giroscópio MEMS', 'Navegação', 427, 10.12, 52),
(53, 'CMP053', 'Espectrômetro IR', 'Instrumentação', 211, 11.70, 53),
(54, 'CMP054', 'Mastro Retrátil', 'Estrutura', 289, 14.50, 54),
(55, 'CMP055', 'Sensor de Pressão', 'Sensores', 510, 3.06, 55),
(56, 'CMP056', 'Fusível Térmico', 'Diagnóstico', 576, 6.19, 56),
(57, 'CMP057', 'Watchdog Timer', 'Controle', 622, 8.46, 57),
(58, 'CMP058', 'Receptor VHF', 'Comunicação', 867, 1.96, 58),
(59, 'CMP059', 'Conversor DC-DC 12V', 'Energia', 104, 8.43, 59),
(60, 'CMP060', 'Star Tracker', 'Navegação', 825, 6.48, 60),
(61, 'CMP061', 'Radiômetro', 'Instrumentação', 828, 3.38, 61),
(62, 'CMP062', 'MLI Térmico', 'Estrutura', 463, 4.42, 62),
(63, 'CMP063', 'Sensor de Pressão', 'Sensores', 850, 3.58, 63),
(64, 'CMP064', 'Relé de Segurança', 'Diagnóstico', 988, 7.82, 64),
(65, 'CMP065', 'Watchdog Timer', 'Controle', 501, 5.57, 65),
(66, 'CMP066', 'Modulador Digital', 'Comunicação', 500, 2.72, 66),
(67, 'CMP067', 'Painel Solar 6W', 'Energia', 154, 5.00, 67),
(68, 'CMP068', 'Roda de Reação', 'Navegação', 164, 10.95, 68),
(69, 'CMP069', 'Radiômetro', 'Instrumentação', 174, 12.04, 69),
(70, 'CMP070', 'Painel Estrutural de Alumínio', 'Estrutura', 623, 7.02, 70),
(71, 'CMP071', 'Sensor de Pressão', 'Sensores', 568, 8.22, 71),
(72, 'CMP072', 'Memória Flash Redundante', 'Diagnóstico', 893, 14.85, 72),
(73, 'CMP073', 'Relógio RTC', 'Controle', 304, 2.39, 73),
(74, 'CMP074', 'Antena Helicoidal', 'Comunicação', 732, 11.32, 74),
(75, 'CMP075', 'Painel Solar 6W', 'Energia', 468, 10.88, 75),
(76, 'CMP076', 'Magnetômetro Digital', 'Navegação', 249, 8.97, 76),
(77, 'CMP077', 'Radiômetro', 'Instrumentação', 964, 4.76, 77),
(78, 'CMP078', 'Mastro Retrátil', 'Estrutura', 820, 0.63, 78),
(79, 'CMP079', 'Sensor de Temperatura', 'Sensores', 294, 7.12, 79),
(80, 'CMP080', 'Memória Flash Redundante', 'Diagnóstico', 832, 8.76, 80),
(81, 'CMP081', 'Relógio RTC', 'Controle', 338, 14.87, 81),
(82, 'CMP082', 'Modulador Digital', 'Comunicação', 411, 7.26, 82),
(83, 'CMP083', 'Bateria Li-Ion 50Wh', 'Energia', 887, 5.72, 83),
(84, 'CMP084', 'Magnetômetro Digital', 'Navegação', 351, 11.07, 84),
(85, 'CMP085', 'Câmera Multiespectral', 'Instrumentação', 936, 3.26, 85),
(86, 'CMP086', 'MLI Térmico', 'Estrutura', 795, 3.73, 86),
(87, 'CMP087', 'Acelerômetro', 'Sensores', 723, 9.90, 87),
(88, 'CMP088', 'Porta JTAG', 'Diagnóstico', 759, 8.85, 88),
(89, 'CMP089', 'Watchdog Timer', 'Controle', 669, 8.29, 89),
(90, 'CMP090', 'Receptor VHF', 'Comunicação', 572, 7.93, 90),
(91, 'CMP091', 'Conversor DC-DC 12V', 'Energia', 995, 7.96, 91),
(92, 'CMP092', 'Roda de Reação', 'Navegação', 151, 12.43, 92),
(93, 'CMP093', 'Câmera Multiespectral', 'Instrumentação', 186, 9.44, 93),
(94, 'CMP094', 'MLI Térmico', 'Estrutura', 664, 9.49, 94),
(95, 'CMP095', 'Acelerômetro', 'Sensores', 473, 8.42, 95),
(96, 'CMP096', 'Memória Flash Redundante', 'Diagnóstico', 611, 7.97, 96),
(97, 'CMP097', 'Watchdog Timer', 'Controle', 727, 3.59, 97),
(98, 'CMP098', 'Transponder X-Band', 'Comunicação', 628, 6.28, 98),
(99, 'CMP099', 'Painel Solar 6W', 'Energia', 918, 8.86, 99),
(100, 'CMP100', 'Giroscópio MEMS', 'Navegação', 125, 3.55, 100),
(101, 'CMP101', 'Perfusor de partículas Beta', 'Instrumentação', 321, 0.31, 101);

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `inventario_espacial`
--
ALTER TABLE `inventario_espacial`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_cod_invent` (`cod_invent`),
  ADD KEY `fk_log_missao` (`id_log`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `inventario_espacial`
--
ALTER TABLE `inventario_espacial`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=102;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `inventario_espacial`
--
ALTER TABLE `inventario_espacial`
  ADD CONSTRAINT `fk_log_missao` FOREIGN KEY (`id_log`) REFERENCES `logs_missao` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
