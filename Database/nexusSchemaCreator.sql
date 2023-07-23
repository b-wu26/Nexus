CREATE DATABASE  IF NOT EXISTS `nexus` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `nexus`;
-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: nexus
-- ------------------------------------------------------
-- Server version	8.0.30

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
-- Table structure for table `class_profile`
--

DROP TABLE IF EXISTS `class_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_profile` (
  `idclass_profile` int NOT NULL,
  `class_name` varchar(45) NOT NULL,
  `course_code` varchar(15) NOT NULL,
  `faculty` varchar(45) NOT NULL,
  PRIMARY KEY (`idclass_profile`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `message` (
  `idmessages` int NOT NULL,
  `idstudent_profile` int NOT NULL,
  `idclass_profile` int NOT NULL,
  `date_sent` date NOT NULL,
  `upvotes` int DEFAULT '0',
  `message` longtext NOT NULL,
  PRIMARY KEY (`idmessages`),
  KEY `idstudent_profile1_idx` (`idstudent_profile`),
  KEY `idclass_profile1_idx` (`idclass_profile`),
  CONSTRAINT `idclass_profile1` FOREIGN KEY (`idclass_profile`) REFERENCES `class_profile` (`idclass_profile`),
  CONSTRAINT `idstudent_profile1` FOREIGN KEY (`idstudent_profile`) REFERENCES `student_profile` (`idstudent_profile`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notes_and_more`
--

DROP TABLE IF EXISTS `notes_and_more`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notes_and_more` (
  `objectid` int NOT NULL,
  `idstudent_profile` int NOT NULL,
  `idclass_profile` int NOT NULL,
  `date_poster` date NOT NULL,
  `s3_endpoint` longtext NOT NULL,
  PRIMARY KEY (`objectid`),
  KEY `idstudent_profile_idx` (`idstudent_profile`),
  KEY `idclass_profile3_idx` (`idclass_profile`),
  CONSTRAINT `idclass_profile3` FOREIGN KEY (`idclass_profile`) REFERENCES `class_profile` (`idclass_profile`),
  CONSTRAINT `idstudent_profile3` FOREIGN KEY (`idstudent_profile`) REFERENCES `student_profile` (`idstudent_profile`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `post` (
  `idquestions` int NOT NULL,
  `idstudent_profile` int NOT NULL,
  `idclass_profile` int NOT NULL,
  `questions` longtext NOT NULL,
  `date_sent` date NOT NULL,
  `upvote` int DEFAULT '0',
  `response_id` int DEFAULT NULL,
  PRIMARY KEY (`idquestions`),
  KEY `idclass_profile2_idx` (`idclass_profile`),
  KEY `idstudent_profile2_idx` (`idstudent_profile`),
  CONSTRAINT `idclass_profile2` FOREIGN KEY (`idclass_profile`) REFERENCES `class_profile` (`idclass_profile`),
  CONSTRAINT `idstudent_profile2` FOREIGN KEY (`idstudent_profile`) REFERENCES `student_profile` (`idstudent_profile`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `schedule`
--

DROP TABLE IF EXISTS `schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schedule` (
  `idstudent_profile` int NOT NULL,
  `idclass_profile` int NOT NULL,
  `Term_year` varchar(45) NOT NULL,
  `current_term` tinyint NOT NULL,
  `prof` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idstudent_profile`,`idclass_profile`,`Term_year`),
  KEY `idclass_profile_idx` (`idclass_profile`),
  CONSTRAINT `idclass_profile` FOREIGN KEY (`idclass_profile`) REFERENCES `class_profile` (`idclass_profile`),
  CONSTRAINT `idstudent_profile` FOREIGN KEY (`idstudent_profile`) REFERENCES `student_profile` (`idstudent_profile`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `student_profile`
--

DROP TABLE IF EXISTS `student_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_profile` (
  `idstudent_profile` int NOT NULL,
  `waterloo_id` varchar(50) NOT NULL,
  `account_password` varchar(50) DEFAULT NULL,
  `f_name` varchar(50) DEFAULT NULL,
  `l_name` varchar(50) DEFAULT NULL,
  `validated` tinyint DEFAULT '0',
  PRIMARY KEY (`idstudent_profile`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-16 22:45:34
