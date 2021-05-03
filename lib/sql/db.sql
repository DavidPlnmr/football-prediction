CREATE TABLE `prediction` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `created_at` timestamp,
  `prediction` varchar(255),
  `api_match_id` int,
  `home_team_name` varchar(255),
  `away_team_name` varchar(255),
  `league_id` int,
  `league_name` varchar(255),
  `date_of_game` date
);

CREATE TABLE `match` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `date` date,
  `time` time,
  `league_id` int,
  `league_name` varchar(255),
  `home_team_name` varchar(255),
  `away_team_name` varchar(255),
  `home_team_score` int,
  `away_team_score` int
);

CREATE TABLE `statistic` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `type` varchar(255),
  `home` varchar(255),
  `away` varchar(255),
  `id_match` int
);

ALTER TABLE `statistic` ADD FOREIGN KEY (`id_match`) REFERENCES `match` (`id`);
