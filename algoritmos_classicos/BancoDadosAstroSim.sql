-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: astrosim
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `arestas`
--

DROP TABLE IF EXISTS `arestas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `arestas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `origem_id` int NOT NULL,
  `destino_id` int NOT NULL,
  `distancia` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `origem_id` (`origem_id`),
  KEY `destino_id` (`destino_id`),
  CONSTRAINT `arestas_ibfk_1` FOREIGN KEY (`origem_id`) REFERENCES `vertices` (`id`),
  CONSTRAINT `arestas_ibfk_2` FOREIGN KEY (`destino_id`) REFERENCES `vertices` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `arestas`
--

LOCK TABLES `arestas` WRITE;
/*!40000 ALTER TABLE `arestas` DISABLE KEYS */;
INSERT INTO `arestas` VALUES (1,1,2,'0.49'),(2,1,3,'0.51'),(3,2,12,'300000'),(4,3,4,'0.27'),(5,3,5,'0.52'),(6,4,6,'4.5'),(7,4,7,'8.74'),(8,5,8,'28.1'),(9,5,9,'1640000000'),(10,8,10,'10.3'),(11,10,11,'85000000'),(12,6,13,'407000000'),(13,10,14,'63333'),(14,13,15,'158000000000'),(15,12,19,'1580000000'),(16,19,18,'11020000000'),(17,15,16,'153070000000');
/*!40000 ALTER TABLE `arestas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario_espacial`
--

DROP TABLE IF EXISTS `inventario_espacial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario_espacial` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cod_invent` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nome` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `categoria` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `massa` int DEFAULT NULL,
  `consumo` decimal(5,2) DEFAULT NULL,
  `id_log` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_cod_invent` (`cod_invent`),
  KEY `fk_log_missao` (`id_log`),
  CONSTRAINT `fk_log_missao` FOREIGN KEY (`id_log`) REFERENCES `logs_missao` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario_espacial`
--

LOCK TABLES `inventario_espacial` WRITE;
/*!40000 ALTER TABLE `inventario_espacial` DISABLE KEYS */;
INSERT INTO `inventario_espacial` VALUES (1,'CMP001','OBC ARM Cortex','Controle',310,8.11,1),(2,'CMP002','Transponder X-Band','Comunicação',498,6.18,2),(3,'CMP003','Bateria Li-Ion 50Wh','Energia',759,7.45,3),(4,'CMP004','Star Tracker','Navegação',741,4.43,4),(5,'CMP005','Radiômetro','Instrumentação',477,13.58,5),(6,'CMP006','Painel Estrutural de Alumínio','Estrutura',783,3.62,6),(7,'CMP007','Sensor de Temperatura','Sensores',326,0.86,7),(8,'CMP008','Fusível Térmico','Diagnóstico',819,1.91,8),(9,'CMP009','OBC ARM Cortex','Controle',247,6.13,9),(10,'CMP010','Receptor VHF','Comunicação',155,11.48,10),(11,'CMP011','Bateria Li-Ion 50Wh','Energia',209,2.38,11),(12,'CMP012','Magnetômetro Digital','Navegação',830,7.87,12),(13,'CMP013','Radiômetro','Instrumentação',196,11.09,13),(14,'CMP014','MLI Térmico','Estrutura',519,12.50,14),(15,'CMP015','Sensor de Radiação','Sensores',939,12.13,15),(16,'CMP016','Memória Flash Redundante','Diagnóstico',328,4.46,16),(17,'CMP017','OBC ARM Cortex','Controle',400,8.86,17),(18,'CMP018','Receptor VHF','Comunicação',582,6.63,18),(19,'CMP019','PDU Básico','Energia',990,6.48,19),(20,'CMP020','Star Tracker','Navegação',422,13.89,20),(21,'CMP021','Radiômetro','Instrumentação',463,7.52,21),(22,'CMP022','Painel Estrutural de Alumínio','Estrutura',631,3.22,22),(23,'CMP023','Sensor de Pressão','Sensores',541,10.57,23),(24,'CMP024','Fusível Térmico','Diagnóstico',372,8.72,24),(25,'CMP025','OBC ARM Cortex','Controle',101,0.63,25),(26,'CMP026','Modulador Digital','Comunicação',526,12.91,26),(27,'CMP027','Conversor DC-DC 12V','Energia',751,1.01,27),(28,'CMP028','Star Tracker','Navegação',981,13.60,28),(29,'CMP029','Espectrômetro IR','Instrumentação',503,9.13,29),(30,'CMP030','Painel Estrutural de Alumínio','Estrutura',451,5.25,30),(31,'CMP031','Sensor de Temperatura','Sensores',324,9.02,31),(32,'CMP032','Memória Flash Redundante','Diagnóstico',177,9.33,32),(33,'CMP033','RTU Modular','Controle',959,3.86,33),(34,'CMP034','Transponder X-Band','Comunicação',166,4.98,34),(35,'CMP035','Bateria Li-Ion 50Wh','Energia',855,11.26,35),(36,'CMP036','Giroscópio MEMS','Navegação',638,9.47,36),(37,'CMP037','Espectrômetro IR','Instrumentação',335,1.64,37),(38,'CMP038','Painel Estrutural de Alumínio','Estrutura',140,3.41,38),(39,'CMP039','Sensor de Radiação','Sensores',760,6.39,39),(40,'CMP040','Porta JTAG','Diagnóstico',127,10.93,40),(41,'CMP041','RTU Modular','Controle',523,10.09,41),(42,'CMP042','Receptor VHF','Comunicação',477,5.47,42),(43,'CMP043','Conversor DC-DC 12V','Energia',240,5.24,43),(44,'CMP044','Giroscópio MEMS','Navegação',861,9.26,44),(45,'CMP045','Radiômetro','Instrumentação',679,12.59,45),(46,'CMP046','MLI Térmico','Estrutura',689,1.96,46),(47,'CMP047','Acelerômetro','Sensores',128,10.63,47),(48,'CMP048','Porta JTAG','Diagnóstico',326,0.65,48),(49,'CMP049','Watchdog Timer','Controle',298,8.13,49),(50,'CMP050','Antena Helicoidal','Comunicação',594,1.48,50),(51,'CMP051','PDU Básico','Energia',497,8.85,51),(52,'CMP052','Giroscópio MEMS','Navegação',427,10.12,52),(53,'CMP053','Espectrômetro IR','Instrumentação',211,11.70,53),(54,'CMP054','Mastro Retrátil','Estrutura',289,14.50,54),(55,'CMP055','Sensor de Pressão','Sensores',510,3.06,55),(56,'CMP056','Fusível Térmico','Diagnóstico',576,6.19,56),(57,'CMP057','Watchdog Timer','Controle',622,8.46,57),(58,'CMP058','Receptor VHF','Comunicação',867,1.96,58),(59,'CMP059','Conversor DC-DC 12V','Energia',104,8.43,59),(60,'CMP060','Star Tracker','Navegação',825,6.48,60),(61,'CMP061','Radiômetro','Instrumentação',828,3.38,61),(62,'CMP062','MLI Térmico','Estrutura',463,4.42,62),(63,'CMP063','Sensor de Pressão','Sensores',850,3.58,63),(64,'CMP064','Relé de Segurança','Diagnóstico',988,7.82,64),(65,'CMP065','Watchdog Timer','Controle',501,5.57,65),(66,'CMP066','Modulador Digital','Comunicação',500,2.72,66),(67,'CMP067','Painel Solar 6W','Energia',154,5.00,67),(68,'CMP068','Roda de Reação','Navegação',164,10.95,68),(69,'CMP069','Radiômetro','Instrumentação',174,12.04,69),(70,'CMP070','Painel Estrutural de Alumínio','Estrutura',623,7.02,70),(71,'CMP071','Sensor de Pressão','Sensores',568,8.22,71),(72,'CMP072','Memória Flash Redundante','Diagnóstico',893,14.85,72),(73,'CMP073','Relógio RTC','Controle',304,2.39,73),(74,'CMP074','Antena Helicoidal','Comunicação',732,11.32,74),(75,'CMP075','Painel Solar 6W','Energia',468,10.88,75),(76,'CMP076','Magnetômetro Digital','Navegação',249,8.97,76),(77,'CMP077','Radiômetro','Instrumentação',964,4.76,77),(78,'CMP078','Mastro Retrátil','Estrutura',820,0.63,78),(79,'CMP079','Sensor de Temperatura','Sensores',294,7.12,79),(80,'CMP080','Memória Flash Redundante','Diagnóstico',832,8.76,80),(81,'CMP081','Relógio RTC','Controle',338,14.87,81),(82,'CMP082','Modulador Digital','Comunicação',411,7.26,82),(83,'CMP083','Bateria Li-Ion 50Wh','Energia',887,5.72,83),(84,'CMP084','Magnetômetro Digital','Navegação',351,11.07,84),(85,'CMP085','Câmera Multiespectral','Instrumentação',936,3.26,85),(86,'CMP086','MLI Térmico','Estrutura',795,3.73,86),(87,'CMP087','Acelerômetro','Sensores',723,9.90,87),(88,'CMP088','Porta JTAG','Diagnóstico',759,8.85,88),(89,'CMP089','Watchdog Timer','Controle',669,8.29,89),(90,'CMP090','Receptor VHF','Comunicação',572,7.93,90),(91,'CMP091','Conversor DC-DC 12V','Energia',995,7.96,91),(92,'CMP092','Roda de Reação','Navegação',151,12.43,92),(93,'CMP093','Câmera Multiespectral','Instrumentação',186,9.44,93),(94,'CMP094','MLI Térmico','Estrutura',664,9.49,94),(95,'CMP095','Acelerômetro','Sensores',473,8.42,95),(96,'CMP096','Memória Flash Redundante','Diagnóstico',611,7.97,96),(97,'CMP097','Watchdog Timer','Controle',727,3.59,97),(98,'CMP098','Transponder X-Band','Comunicação',628,6.28,98),(99,'CMP099','Painel Solar 6W','Energia',918,8.86,99),(100,'CMP100','Giroscópio MEMS','Navegação',125,3.55,100),(101,'CMP101','Perfusor de partículas Beta','Instrumentação',321,0.31,101);
/*!40000 ALTER TABLE `inventario_espacial` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs_missao`
--

DROP TABLE IF EXISTS `logs_missao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs_missao` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data` datetime DEFAULT NULL,
  `mensagem` text COLLATE utf8mb4_general_ci,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs_missao`
--

LOCK TABLES `logs_missao` WRITE;
/*!40000 ALTER TABLE `logs_missao` DISABLE KEYS */;
INSERT INTO `logs_missao` VALUES (1,'2025-07-06 08:00:00','[Sonda-2] Dados de Encélado sincronizados.'),(2,'2025-07-06 08:02:00','[Controle] Satélite posicionado sobre Titã.'),(3,'2025-07-06 08:04:00','[Controle] Iniciando análise espectral do solo marciano.'),(4,'2025-07-06 08:06:00','[Engenharia] Rotas de reentrada recalculadas com sucesso.'),(5,'2025-07-06 08:08:00','[Estação] Log completo de energia armazenado.'),(6,'2025-07-06 08:10:00','[Engenharia] Rotas de reentrada recalculadas com sucesso.'),(7,'2025-07-06 08:12:00','[Módulo Exo] Painéis solares totalmente estendidos.'),(8,'2025-07-06 08:14:00','[Estação] Log completo de energia armazenado.'),(9,'2025-07-06 08:16:00','[Robô-Minerador] Atividade subterrânea detectada em Encélado.'),(10,'2025-07-06 08:18:00','[Sistema] Anomalia detectada na unidade de propulsão.'),(11,'2025-07-06 08:20:00','[Engenharia] Rotas de reentrada recalculadas com sucesso.'),(12,'2025-07-06 08:22:00','[Câmera] Captura visual da superfície de Marte concluída.'),(13,'2025-07-06 08:24:00','[Controle] Transmissão criptografada ativada.'),(14,'2025-07-06 08:26:00','[Sonda-1] Aterrissagem bem-sucedida em Europa.'),(15,'2025-07-06 08:28:00','[Controle] Satélite posicionado sobre Titã.'),(16,'2025-07-06 08:30:00','[Módulo Exo] Painéis solares totalmente estendidos.'),(17,'2025-07-06 08:32:00','[Robô] Fóssil microscópico encontrado em solo úmido.'),(18,'2025-07-06 08:34:00','[Engenharia] Rotas de reentrada recalculadas com sucesso.'),(19,'2025-07-06 08:36:00','[Controle] Transmissão criptografada ativada.'),(20,'2025-07-06 08:38:00','[Sonda-1] Aterrissagem bem-sucedida em Europa.'),(21,'2025-07-06 08:40:00','[Sistema] Anomalia detectada na unidade de propulsão.'),(22,'2025-07-06 08:42:00','[Robô] Cavidade natural encontrada sob a crosta.'),(23,'2025-07-06 08:44:00','[Sonda-1] Aterrissagem bem-sucedida em Europa.'),(24,'2025-07-06 08:46:00','[Sonda-3] Comunicação estabelecida com módulo orbital.'),(25,'2025-07-06 08:48:00','[Sonda-4] Solo de Europa contém traços de perclorato.'),(26,'2025-07-06 08:50:00','[Controle] Iniciando análise espectral do solo marciano.'),(27,'2025-07-06 08:52:00','[Sensores] Variação magnética incomum em Ganimedes.'),(28,'2025-07-06 08:54:00','[Sistema] Anomalia detectada na unidade de propulsão.'),(29,'2025-07-06 08:56:00','[Sonda-4] Solo de Europa contém traços de perclorato.'),(30,'2025-07-06 08:58:00','[Robô-Minerador] Atividade subterrânea detectada em Encélado.'),(31,'2025-07-06 09:00:00','[Robô-Minerador] Atividade subterrânea detectada em Encélado.'),(32,'2025-07-06 09:02:00','[Robô] Fóssil microscópico encontrado em solo úmido.'),(33,'2025-07-06 09:04:00','[Robô-Minerador] Atividade subterrânea detectada em Encélado.'),(34,'2025-07-06 09:06:00','[Sonda-3] Comunicação estabelecida com módulo orbital.'),(35,'2025-07-06 09:08:00','[Módulo Exo] Painéis solares totalmente estendidos.'),(36,'2025-07-06 09:10:00','[Robô] Cavidade natural encontrada sob a crosta.'),(37,'2025-07-06 09:12:00','[Controle] Satélite posicionado sobre Titã.'),(38,'2025-07-06 09:14:00','[Missão] Nível de radiação em Titã dentro dos parâmetros.'),(39,'2025-07-06 09:16:00','[Sonda-4] Solo de Europa contém traços de perclorato.'),(40,'2025-07-06 09:18:00','[Transmissão] Dados enviados para o centro de controle.'),(41,'2025-07-06 09:20:00','[Sensores] Variação magnética incomum em Ganimedes.'),(42,'2025-07-06 09:22:00','[Controle] Transmissão criptografada ativada.'),(43,'2025-07-06 09:24:00','[Sonda-2] Dados de Encélado sincronizados.'),(44,'2025-07-06 09:26:00','[Controle] Iniciando análise espectral do solo marciano.'),(45,'2025-07-06 09:28:00','[Robô] Fóssil microscópico encontrado em solo úmido.'),(46,'2025-07-06 09:30:00','[Sonda-1] Aterrissagem segura em Europa confirmada.'),(47,'2025-07-06 09:32:00','[Sonda-2] Dados de Encélado sincronizados.'),(48,'2025-07-06 09:34:00','[Controle] Iniciando análise espectral do solo marciano.'),(49,'2025-07-06 09:36:00','[Robô-Minerador] Atividade subterrânea detectada em Encélado.'),(50,'2025-07-06 09:38:00','[Sonda-1] Aterrissagem segura em Europa confirmada.'),(51,'2025-07-06 09:40:00','[Sonda-2] Amostra coletada próxima ao cânion Valles Marineris.'),(52,'2025-07-06 09:42:00','[Sonda-1] Aterrissagem segura em Europa confirmada.'),(53,'2025-07-06 09:44:00','[Controle] Iniciando análise espectral do solo marciano.'),(54,'2025-07-06 09:46:00','[Sonda-3] Comunicação estabelecida com módulo orbital.'),(55,'2025-07-06 09:48:00','[Sonda-1] Aterrissagem bem-sucedida em Europa.'),(56,'2025-07-06 09:50:00','[Sistema] Anomalia detectada na unidade de propulsão.'),(57,'2025-07-06 09:52:00','[Controle] Satélite posicionado sobre Titã.'),(58,'2025-07-06 09:54:00','[Controle] Transmissão criptografada ativada.'),(59,'2025-07-06 09:56:00','[Estação] Log completo de energia armazenado.'),(60,'2025-07-06 09:58:00','[Controle] Satélite posicionado sobre Titã.'),(61,'2025-07-06 10:00:00','[Sonda-4] Solo de Europa contém traços de perclorato.'),(62,'2025-07-06 10:02:00','[Sonda-2] Dados de Encélado sincronizados.'),(63,'2025-07-06 10:04:00','[Sensores] Variação magnética incomum em Ganimedes.'),(64,'2025-07-06 10:06:00','[Sonda-4] Solo de Europa contém traços de perclorato.'),(65,'2025-07-06 10:08:00','[Robô] Cavidade natural encontrada sob a crosta.'),(66,'2025-07-06 10:10:00','[Sonda-4] Solo de Europa contém traços de perclorato.'),(67,'2025-07-06 10:12:00','[Sistema] Anomalia detectada na unidade de propulsão.'),(68,'2025-07-06 10:14:00','[Controle] Iniciando análise espectral do solo marciano.'),(69,'2025-07-06 10:16:00','[Sonda-1] Aterrissagem segura em Europa confirmada.'),(70,'2025-07-06 10:18:00','[Missão] Nível de radiação em Titã dentro dos parâmetros.'),(71,'2025-07-06 10:20:00','[Transmissão] Dados enviados para o centro de controle.'),(72,'2025-07-06 10:22:00','[Transmissão] Dados enviados para o centro de controle.'),(73,'2025-07-06 10:24:00','[Robô] Cavidade natural encontrada sob a crosta.'),(74,'2025-07-06 10:26:00','[Módulo Exo] Painéis solares totalmente estendidos.'),(75,'2025-07-06 10:28:00','[Sonda-3] Comunicação estabelecida com módulo orbital.'),(76,'2025-07-06 10:30:00','[Estação] Log completo de energia armazenado.'),(77,'2025-07-06 10:32:00','[Engenharia] Rotas de reentrada recalculadas com sucesso.'),(78,'2025-07-06 10:34:00','[Controle] Iniciando análise espectral do solo marciano.'),(79,'2025-07-06 10:36:00','[Missão] Nível de radiação em Titã dentro dos parâmetros.'),(80,'2025-07-06 10:38:00','[Sonda-1] Aterrissagem bem-sucedida em Europa.'),(81,'2025-07-06 10:40:00','[Módulo Exo] Painéis solares totalmente estendidos.'),(82,'2025-07-06 10:42:00','[Sonda-4] Solo de Europa contém traços de perclorato.'),(83,'2025-07-06 10:44:00','[Engenharia] Rotas de reentrada recalculadas com sucesso.'),(84,'2025-07-06 10:46:00','[Sonda-1] Aterrissagem bem-sucedida em Europa.'),(85,'2025-07-06 10:48:00','[Controle] Satélite posicionado sobre Titã.'),(86,'2025-07-06 10:50:00','[Controle] Satélite posicionado sobre Titã.'),(87,'2025-07-06 10:52:00','[Missão] Nível de radiação em Titã dentro dos parâmetros.'),(88,'2025-07-06 10:54:00','[Engenharia] Rotas de reentrada recalculadas com sucesso.'),(89,'2025-07-06 10:56:00','[Sonda-4] Solo de Europa contém traços de perclorato.'),(90,'2025-07-06 10:58:00','[Missão] Nível de radiação em Titã dentro dos parâmetros.'),(91,'2025-07-06 11:00:00','[Sonda-1] Aterrissagem bem-sucedida em Europa.'),(92,'2025-07-06 11:02:00','[Controle] Transmissão criptografada ativada.'),(93,'2025-07-06 11:04:00','[Sistema] Anomalia detectada na unidade de propulsão.'),(94,'2025-07-06 11:06:00','[Sistema] Anomalia detectada na unidade de propulsão.'),(95,'2025-07-06 11:08:00','[Sonda-2] Amostra coletada próxima ao cânion Valles Marineris.'),(96,'2025-07-06 11:10:00','[Robô] Cavidade natural encontrada sob a crosta.'),(97,'2025-07-06 11:12:00','[Sonda-3] Comunicação estabelecida com módulo orbital.'),(98,'2025-07-06 11:14:00','[Sonda-4] Solo de Europa contém traços de perclorato.'),(99,'2025-07-06 11:16:00','[Robô] Cavidade natural encontrada sob a crosta.'),(100,'2025-07-06 11:18:00','[Sonda-3] Comunicação estabelecida com módulo orbital.'),(101,'2025-07-06 15:15:00','[Sonda-2] Dados de Encélado sincronizados.');
/*!40000 ALTER TABLE `logs_missao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vertices`
--

DROP TABLE IF EXISTS `vertices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vertices` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nome` (`nome`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vertices`
--

LOCK TABLES `vertices` WRITE;
/*!40000 ALTER TABLE `vertices` DISABLE KEYS */;
INSERT INTO `vertices` VALUES (14,'Alnitak'),(12,'Centauri'),(19,'Galáxia Anã do Cão Maior'),(16,'Galáxia Anã Elíptica de Sagitário'),(15,'Galáxia de Andrômeda'),(6,'Júpiter'),(5,'Marte'),(2,'Mercúrio'),(11,'Nebulosa_Orion'),(8,'Netuno'),(18,'Pequena Nuvem de Magalhães'),(13,'Pulsar'),(9,'Sargitario_A'),(7,'Saturno'),(1,'Sol'),(3,'Terra'),(10,'Urano'),(4,'Vênus');
/*!40000 ALTER TABLE `vertices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'astrosim'
--

--
-- Dumping routines for database 'astrosim'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-25 22:58:10
