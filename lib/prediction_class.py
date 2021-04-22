#!/usr/bin/python3
from provider import Provider
import constants
import re

class Prediction:
    """
    Class to make a prediction on a match between two football teams
    """
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team
        self.provider = Provider()
        self.results = self.provider.getAllStatsFromTeamsDB(self.home_team, self.away_team, "2018-08-10")
        self.home_heat_of_moment = self.__compute_heat_moment(self.home_team, self.results["firstTeam_lastResults"])
        self.away_heat_of_moment = self.__compute_heat_moment(self.away_team, self.results["secondTeam_lastResults"])
        self.__compute_off_score(self.home_team)
        self.__compute_off_score(self.away_team)
        
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
    
    def __compute_off_score(self, team_name):
        team_result = TeamResult(team_name)
        if team_name == self.home_team:    
            self.__insertDataTeamResult(team_result, "firstTeam_lastResults")
        else:
            self.__insertDataTeamResult(team_result, "secondTeam_lastResults")
        
        self.__insertDataTeamResult(team_result, "firstTeam_VS_secondTeam")
        
        print (f"{team_name}")
        print ("===================")
        print (f"Nombre de matchs joués : {team_result.games_count}")
        print (f"Moyenne de but par match : {team_result.average_goal_per_game()}")
        print (f"Moyenne de tir par match : {team_result.average_goal_attempts_per_game()}")
        print (f"Moyenne de tir cadrés par match : {team_result.average_shots_on_goal_per_game()}")
        print (f"Moyenne d'arrêts du gardien par match : {team_result.average_goalkeeper_saves_per_game()}")
        print (f"Moyenne de fautes par match : {team_result.average_fouls_per_game()}")
        print (f"Moyenne de cartons jaunes par match : {team_result.average_yellow_cards_per_game()}")
        print (f"Moyenne de tacles par match : {team_result.average_tackles_per_game()}")
        print (f"Moyenne d'attaques par match : {team_result.average_attacks_per_game()}")
        print (f"Moyenne d'attaques dangereuses par match : {team_result.average_dangerous_attacks_per_game()}")
        pass


    def __insertDataTeamResult(self, team_result_obj, last_results):
        for match in self.results[last_results]:
                team_result_obj.games_count += 1
                
                team_result_obj.goals_count += int(match["home_team_score"]) if team_result_obj.team_name == match["home_team"] else int(match["away_team_score"])
                
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
        self.games_count = 0
        self.goals_count = 0
        self.ball_possession = 0
        self.goal_attempts = 0
        self.shots_on_goal = 0
        self.goalkeeper_saves = 0
        self.fouls = 0
        self.yellow_cards = 0
        self.tackles = 0
        self.attacks = 0
        self.dangerous_attacks = 0
        
    def average_goal_per_game(self):
        return self.goals_count/self.games_count
    
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