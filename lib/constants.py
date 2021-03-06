STATISTICS_TO_GET = ["Ball Possession", 
                     "Goal Attempts",
                     "Shots on Goal",
                     "Attacks", 
                     "Dangerous Attacks",
                     "Tackles", 
                     "Fouls",
                     "Goalkeeper Saves",
                     "Yellow Cards"]

NB_GAMES_HEAT_OF_THE_MOMENT=5

TIMEOUT_IN_SECONDS = 45

MULTIPLE_LEAGUES = {
    "Premier League" : 148,
    "Liga NOS" : 391,
    "Ligue 1" : 176,
    "LaLiga" : 468,
    "Serie A" : 262
                    }
DELTA_DAY_PREVIOUS = 14
DELTA_DAY_UPCOMING = 3
DELTA_HOUR_FOR_CACHE_REFRESH = 12
DELTA_MONTHS_TO_GET_GAMES=6

MIN_OF_GAMES_TO_MAKE_PREDICTION=5

DELTA_TO_DETERMINE_DRAW = 1.01

WEIGHT_GOALS=8
WEIGHT_DANGEROUS_ATTACKS=5
WEIGHT_SHOTS_ON_GOAL=3
WEIGHT_ATTACKS=2
WEIGHT_GOAL_ATTEMPTS=1
WEIGHT_BALL_POSSESSION=1

WEIGHT_YELLOW_CARDS=2
WEIGHT_FOULS=3

WEIGHT_TACKLES=WEIGHT_FOULS
WEIGHT_GOALKEEPER_SAVES=1

WEIGHT_HEAT_OF_MOMENT=13

POINTS_FOR_A_WIN=3
POINTS_FOR_A_DRAW=1
POINTS_FOR_A_LOSE=0