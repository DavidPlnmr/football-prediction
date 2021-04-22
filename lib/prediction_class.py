#!/usr/bin/python3
from provider import Provider
import constants

class Prediction:
    """
    Class to make a prediction on a match between two football teams
    """
    def __init__(self, home_team, away_team):
        self.home_team_result = TeamResult(home_team)
        self.away_team_result = TeamResult(away_team)

        self.provider = Provider()
        
        self.results = self.provider.get_all_stats_from_teams_db(home_team, away_team, "2018-08-10")
        
        self.home_team_result.heat_of_moment = self.__compute_heat_moment(home_team, self.results["firstTeam_lastResults"])
        self.away_team_result.heat_of_moment = self.__compute_heat_moment(away_team, self.results["secondTeam_lastResults"])
        
        self.__insert_data_team_result(self.home_team_result, "firstTeam_lastResults")
        self.__insert_data_team_result(self.away_team_result, "secondTeam_lastResults")
        
        self.__insert_data_team_result(self.home_team_result, "firstTeam_VS_secondTeam")
        self.__insert_data_team_result(self.away_team_result, "firstTeam_VS_secondTeam")
    
    def define_winner(self):
        home_team_final_score = self.__compute_off_score(self.home_team_result)
        away_team_final_score = self.__compute_off_score(self.away_team_result)
        
        home_team_final_score += self.__compute_def_score(self.home_team_result)
        away_team_final_score += self.__compute_def_score(self.away_team_result)
        
        home_team_final_score += self.__compute_heat_moment_score(self.home_team_result)
        away_team_final_score += self.__compute_heat_moment_score(self.away_team_result)
        
        print(f"{self.get_home_team_name()} Final Score : {home_team_final_score}")
        print(f"{self.get_away_team_name()} Final Score : {away_team_final_score}")
        
        pass
        
    def get_home_team_name(self):
        return self.home_team_result.team_name
        pass
    
    def get_away_team_name(self):
        return self.away_team_result.team_name
        pass
        
    def __compute_heat_moment_score(self, team_result):
        return team_result.average_points_per_game()*constants.WEIGHT_HEAT_OF_MOMENT
        pass
        
    def __compute_heat_moment(self, team_name, last_results):
        """
        Compute the heat of the moment of the team with its results
        """
        heat_of_moment = ""
        for index in range(constants.NB_GAMES_HEAT_OF_THE_MOMENT):
            result = int(last_results[index]["home_team_score"]) - int(last_results[index]["away_team_score"])
            if result == 0:
                heat_of_moment += 'D' # D for Draw
            else:
                if last_results[index]["home_team"] == team_name:
                    heat_of_moment += 'W' if result > 0 else 'L' # W for Win, L for Lose
                else:
                    heat_of_moment += 'L' if result > 0 else 'W' # W for Win, L for Lose
        return heat_of_moment
        pass       
    
    def __compute_off_score(self, team_result):
        
        score = 0
        
        score += team_result.average_goal_scored_per_game()*constants.WEIGHT_GOALS
        score += team_result.average_dangerous_attacks_per_game()*constants.WEIGHT_DANGEROUS_ATTACKS
        score += team_result.average_shots_on_goal_per_game()*constants.WEIGHT_SHOTS_ON_GOAL
        score += team_result.average_attacks_per_game()*constants.WEIGHT_ATTACKS
        score += team_result.average_goal_attempts_per_game()*constants.WEIGHT_GOAL_ATTEMPTS
        score += team_result.average_ball_possession_per_game()*constants.WEIGHT_BALL_POSSESSION

        return score
        pass

    def __compute_def_score(self, team_result):
        
        score = 0
        #Bonus
        score += team_result.average_tackles_per_game()*constants.WEIGHT_TACKLES
        score += team_result.average_goalkeeper_saves_per_game()*constants.WEIGHT_GOALKEEPER_SAVES
        
        #Malus
        score -= team_result.average_goal_conceded_per_game()*constants.WEIGHT_GOALS
        score -= team_result.average_fouls_per_game()*constants.WEIGHT_FOULS
        score -= team_result.average_yellow_cards_per_game()*constants.WEIGHT_YELLOW_CARDS
        
        return score
        pass

    def __insert_data_team_result(self, team_result_obj, last_results):
        for match in self.results[last_results]:
                team_result_obj.games_count += 1
                
                team_result_obj.goals_scored_count += int(match["home_team_score"]) if team_result_obj.team_name == match["home_team"] else int(match["away_team_score"])
                # This line is the reverse of the top one
                team_result_obj.goals_conceded_count += int(match["home_team_score"]) if team_result_obj.team_name != match["home_team"] else int(match["away_team_score"])
                
                #These 2 lines are here to remove the "%" char of the Ball Possession Stat
                match["Ball Possession"]["home"] = match["Ball Possession"]["home"].replace('%', '')
                match["Ball Possession"]["away"] = match["Ball Possession"]["away"].replace('%', '')
                team_result_obj.ball_possession += int(match["Ball Possession"]["home"]) if team_result_obj.team_name == match["home_team"] else int(match["Ball Possession"]["away"])
                
                team_result_obj.goal_attempts += int(match["Goal Attempts"]["home"]) if team_result_obj.team_name == match["home_team"] else int(match["Goal Attempts"]["away"])
                
                team_result_obj.shots_on_goal += int(match["Shots on Goal"]["home"]) if team_result_obj.team_name == match["home_team"] else int(match["Shots on Goal"]["away"])
                
                team_result_obj.goalkeeper_saves += int(match["Goalkeeper Saves"]["home"]) if team_result_obj.team_name == match["home_team"] else int(match["Goalkeeper Saves"]["away"])
                
                team_result_obj.fouls += int(match["Fouls"]["home"]) if team_result_obj.team_name == match["home_team"] else int(match["Fouls"]["away"])
                
                team_result_obj.yellow_cards += int(match["Yellow Cards"]["home"]) if team_result_obj.team_name == match["home_team"] else int(match["Yellow Cards"]["away"])
                
                team_result_obj.tackles += int(match["Tackles"]["home"]) if team_result_obj.team_name == match["home_team"] else int(match["Tackles"]["away"])
                
                team_result_obj.attacks += int(match["Attacks"]["home"]) if team_result_obj.team_name == match["home_team"] else int(match["Attacks"]["away"])
                
                team_result_obj.dangerous_attacks += int(match["Dangerous Attacks"]["home"]) if team_result_obj.team_name == match["home_team"] else int(match["Dangerous Attacks"]["away"])
        

class TeamResult:
    def __init__(self, team_name):
        self.team_name = team_name
        self.heat_of_moment = ""
        self.games_count = 0
        self.goals_scored_count = 0
        self.goals_conceded_count = 0
        self.ball_possession = 0
        self.goal_attempts = 0
        self.shots_on_goal = 0
        self.goalkeeper_saves = 0
        self.fouls = 0
        self.yellow_cards = 0
        self.tackles = 0
        self.attacks = 0
        self.dangerous_attacks = 0
        
    def average_goal_scored_per_game(self):
        return self.goals_scored_count/self.games_count
    
    def average_goal_conceded_per_game(self):
        return self.goals_conceded_count/self.games_count
    
    def average_ball_possession_per_game(self):
        return self.ball_possession/self.games_count
    
    def average_goal_attempts_per_game(self):
        return self.goal_attempts/self.games_count
    
    def average_shots_on_goal_per_game(self):
        return self.shots_on_goal/self.games_count
    
    def average_goalkeeper_saves_per_game(self):
        return self.goalkeeper_saves/self.games_count
    
    def average_fouls_per_game(self):
        return self.fouls/self.games_count
    
    def average_yellow_cards_per_game(self):
        return self.yellow_cards/self.games_count
    
    def average_tackles_per_game(self):
        return self.tackles/self.games_count
    
    def average_attacks_per_game(self):
        return self.attacks/self.games_count
    
    def average_dangerous_attacks_per_game(self):
        return self.dangerous_attacks/self.games_count  
    
    def average_points_per_game(self):
        """
        Make an average of the points won per game with the heat of the moment
        """
        result = 0
        for char in self.heat_of_moment:
            if char=='W':
                result+=constants.POINTS_FOR_A_WIN
            elif char=='D':
                result+=constants.POINTS_FOR_A_DRAW
            elif char=='L':
                result+=constants.POINTS_FOR_A_LOSE
        return result/self.games_count