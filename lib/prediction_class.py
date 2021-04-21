#!/usr/bin/python3
from provider import Provider
import constants

class Prediction:
    """
    Class to make a prediction on a match between two football teams
    """
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team
        self.provider = Provider()
        self.results = self.provider.getAllStatsFromTeams(self.home_team, self.away_team)
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
        print (f"Nombre de buts marqués : {team_result.goals_count}")
        print (f"Nombre de matchs joués : {team_result.games_count}")
        print (f"Moyenne de but par match : {team_result.average_goal_per_game()}")
        pass


    def __insertDataTeamResult(self, team_result_obj, last_results):
        for match in self.results[last_results]:
                team_result_obj.goals_count += int(match["home_team_score"]) if team_result_obj.team_name == match["home_team"] else int(match["away_team_score"])
                team_result_obj.games_count += 1
        

class TeamResult:
    def __init__(self, team_name):
        self.team_name = team_name
        self.games_count = 0
        self.goals_count = 0
        self.ball_possession = 0
        self.goal_attempts = 0
        self.goalkeeper_saves = 0
        self.fouls = 0
        self.yellow_cards = 0
        self.tackles = 0
        self.attacks = 0
        self.dangerous_attacksé = 0
        
    def average_goal_per_game(self):
        return self.goals_count/self.games_count
        