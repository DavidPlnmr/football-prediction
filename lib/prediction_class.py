#!/usr/bin/python3
from prediction_provider import PredictionProvider
import constants

class Prediction:
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team
        self.provider = PredictionProvider()
        self.statistics = self.provider.getAllStatsFromTeams(self.home_team, self.away_team)
        self.home_heat_of_moment = self.__compute_heat_moment(self.home_team, self.statistics["firstTeam_lastResults"])
        self.away_heat_of_moment = self.__compute_heat_moment(self.away_team, self.statistics["secondTeam_lastResults"])
        
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
    
    def __compute_off_score(self, ):
        pass
            