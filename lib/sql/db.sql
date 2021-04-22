CREATE TABLE `prediction` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `created_at` timestamp,
  `prediction` varchar(255),
  `api_match_id` int,
  `home_team_name` varchar(255),
  `away_team_name` varchar(255),
  `off_score_home_team` double,
  `def_score_home_team` double,
  `off_score_away_team` double,
  `def_score_away_team` double
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

ALTER TABLE `statistics` ADD FOREIGN KEY (`id_match`) REFERENCES `match` (`id`);
