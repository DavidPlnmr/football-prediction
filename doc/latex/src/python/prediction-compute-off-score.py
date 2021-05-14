def __compute_off_score(self, team_result):
        
        score = 0
        
        score += team_result.average_goal_scored_per_game()*lib.constants.WEIGHT_GOALS
        score += team_result.average_dangerous_attacks_per_game()*lib.constants.WEIGHT_DANGEROUS_ATTACKS
        score += team_result.average_shots_on_goal_per_game()*lib.constants.WEIGHT_SHOTS_ON_GOAL
        score += team_result.average_attacks_per_game()*lib.constants.WEIGHT_ATTACKS
        score += team_result.average_goal_attempts_per_game()*lib.constants.WEIGHT_GOAL_ATTEMPTS
        score += team_result.average_ball_possession_per_game()*lib.constants.WEIGHT_BALL_POSSESSION

        return score