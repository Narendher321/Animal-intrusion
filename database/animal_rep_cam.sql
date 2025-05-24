-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 05, 2023 at 01:28 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `animal_rep_cam`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`, `mobile`) VALUES
('sham', '9999', 0);

-- --------------------------------------------------------

--
-- Table structure for table `animal_detect`
--

CREATE TABLE `animal_detect` (
  `id` int(11) NOT NULL,
  `user` varchar(20) NOT NULL,
  `animal` varchar(20) NOT NULL,
  `image_name` varchar(40) NOT NULL,
  `dtime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `animal_detect`
--

INSERT INTO `animal_detect` (`id`, `user`, `animal`, `image_name`, `dtime`) VALUES
(1, 'suresh', 'Sheep', 'c_49.jpg', '2022-04-26 14:27:52'),
(2, 'suresh', 'Goat', 'c_74.jpg', '2022-04-26 14:28:11'),
(3, 'suresh', 'Bear', 'c_2.jpg', '2022-04-26 14:28:53'),
(4, 'suresh', 'Bear', 'c_14.jpg', '2022-05-09 14:52:50'),
(5, 'suresh', 'Cow', 'c_30.jpeg', '2022-05-09 14:53:08'),
(6, 'suresh', 'Bear', 'c_1.jpg', '2022-05-09 14:53:36'),
(7, 'suresh', 'Sheep', 'c_8.jpg', '2022-05-09 14:54:22'),
(8, 'suresh', 'Sheep', 'c_8.jpg', '2022-12-15 11:48:00'),
(9, 'suresh', 'Horse', 'c_86.jpeg', '2023-01-23 14:37:33'),
(10, 'suresh', 'Elephant', 'c_35.jpg', '2023-01-23 14:40:07'),
(11, 'suresh', 'Goat', 'c_72.jpg', '2023-01-23 14:40:38'),
(12, 'suresh', 'Sheep', 'c_4.jpg', '2023-01-23 14:43:40'),
(13, 'suresh', 'Bears', 'r13.jpg', '2023-06-19 15:20:26'),
(14, 'suresh', 'Bears', 'r14.jpg', '2023-06-19 15:20:37'),
(15, 'suresh', 'Bears', 'r15.jpg', '2023-06-19 15:20:47'),
(16, 'suresh', 'Bears', 'r16.jpg', '2023-06-19 15:20:58'),
(17, 'suresh', 'Bears', 'r17.jpg', '2023-06-19 15:21:08'),
(18, 'suresh', 'Bears', 'r18.jpg', '2023-06-19 15:21:19'),
(19, 'suresh', 'Bears', 'r19.jpg', '2023-06-19 15:21:29'),
(20, 'suresh', 'Bears', 'r20.jpg', '2023-06-19 15:21:40'),
(21, 'suresh', 'Bears', 'r21.jpg', '2023-06-19 15:21:51'),
(22, 'suresh', 'Bears', 'r22.jpg', '2023-06-19 15:22:01'),
(23, 'suresh', 'Bears', 'r23.jpg', '2023-06-19 15:22:11'),
(24, 'suresh', 'Bears', 'r24.jpg', '2023-06-19 15:22:22'),
(25, 'suresh', 'Elephant', 'r25.jpg', '2023-06-19 15:38:32'),
(26, 'suresh', 'Cheetah', 'r26.jpg', '2023-06-19 15:53:12'),
(27, 'suresh', '1_40.jpg', 'r27.jpg', '2023-07-05 18:32:52'),
(28, 'suresh', '1_40.jpg', 'r28.jpg', '2023-07-05 18:33:02'),
(29, 'suresh', '1_40.jpg', 'r29.jpg', '2023-07-05 18:33:13'),
(30, 'suresh', '1_40.jpg', 'r30.jpg', '2023-07-05 18:33:23'),
(31, 'suresh', '1_40.jpg', 'r31.jpg', '2023-07-05 18:33:34'),
(32, 'suresh', '1_40.jpg', 'r32.jpg', '2023-07-05 18:33:45'),
(33, 'suresh', '1_40.jpg', 'r33.jpg', '2023-07-05 18:33:55'),
(34, 'suresh', 'Elephant', 'r34.jpg', '2023-07-05 18:38:00'),
(35, 'suresh', 'Elephant', 'r35.jpg', '2023-07-05 18:38:10'),
(36, 'suresh', 'Elephant', 'r36.jpg', '2023-07-05 18:45:01'),
(37, 'suresh', 'Elephant', 'r37.jpg', '2023-07-05 18:45:12'),
(38, 'suresh', 'Elephant', 'r38.jpg', '2023-07-05 18:45:22'),
(39, 'suresh', 'Elephant', 'r39.jpg', '2023-07-05 18:45:33'),
(40, 'suresh', 'Elephant', 'r40.jpg', '2023-07-05 18:45:43'),
(41, 'suresh', 'Elephant', 'r41.jpg', '2023-07-05 18:45:54'),
(42, 'suresh', 'Elephant', 'r42.jpg', '2023-07-05 18:46:04'),
(43, 'suresh', 'Elephant', 'r43.jpg', '2023-07-05 18:46:14'),
(44, 'suresh', 'Elephant', 'r44.jpg', '2023-07-05 18:47:14');

-- --------------------------------------------------------

--
-- Table structure for table `animal_img`
--

CREATE TABLE `animal_img` (
  `id` int(11) NOT NULL,
  `vid` int(11) NOT NULL,
  `animal_img` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `animal_img`
--


-- --------------------------------------------------------

--
-- Table structure for table `animal_info`
--

CREATE TABLE `animal_info` (
  `id` int(11) NOT NULL,
  `animal` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `animal_info`
--

INSERT INTO `animal_info` (`id`, `animal`) VALUES
(1, 'Bear'),
(2, 'Horse'),
(3, 'Cow'),
(4, 'Elephant'),
(5, 'Goat'),
(6, 'Pig'),
(7, 'Sheep');

-- --------------------------------------------------------

--
-- Table structure for table `farmer`
--

CREATE TABLE `farmer` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `location` varchar(50) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `farmer`
--

INSERT INTO `farmer` (`id`, `name`, `mobile`, `email`, `location`, `uname`, `pass`) VALUES
(1, 'Suresh', 9894442716, 'suresh@gmail.com', 'Chennai', 'suresh', '1234'),
(2, 'vijay', 6383436185, 'vijayaragavanvijay2001@gmail.com', 'karur', 'vijayrak', '12345');

-- --------------------------------------------------------

--
-- Table structure for table `train_data`
--

CREATE TABLE `train_data` (
  `id` int(11) NOT NULL,
  `animal` varchar(30) NOT NULL,
  `fimg` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `train_data`
--

