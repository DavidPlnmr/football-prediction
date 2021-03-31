CREATE DATABASE `soccerPronostic` CHARACTER SET utf8 COLLATE utf8_general_ci; /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `soccerPronostic`

CREATE TABLE `prediction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `prediction` varchar(255) NOT NULL,
  `api_match_id` int(11) DEFAULT NULL,
  `hometeam_name` varchar(255) NOT NULL,
  `awayteam_name` varchar(255) NOT NULL,
  `off_score_hometeam` int(11) NOT NULL,
  `def_score_hometeam` int(11) NOT NULL,
  `off_score_awayteam` int(11) NOT NULL,
  `def_score_awayteam` int(11) NOT NULL,
  `real_match` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
