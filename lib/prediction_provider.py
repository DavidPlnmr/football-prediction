#!/usr/bin/python3
import os
from dotenv import load_dotenv
import logging
from api.api_facade import ApiFacade
from sql.db_manager import DbManager
import constants



class PredictionProvider:
    def __init__(self):
        load_dotenv()
        logging.basicConfig(filename='./log/app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
        self.api_facade = ApiFacade(os.getenv("API_KEY"))
        self.db_manager = DbManager("127.0.0.1", os.getenv("DB_USER"), os.getenv("DB_PASSWORD"))
        
    def getAllStatsFromTeams(self, first_team_name, second_team_name):
        """
        Make a call to the API using getH2H and make a treatment to have the stats for each match of the two different teams
        """
        reqresult = self.api_facade.getH2H(first_team_name, second_team_name)
        
        result = {}
        stats_matches_two_team = []
        stats_first_team = []
        stats_second_team = []
        
        if len(reqresult["firstTeam_lastResults"]) > 0 and len(reqresult["secondTeam_lastResults"]) > 0:
            
            for match in reqresult["firstTeam_VS_secondTeam"]:
                
                api_match_id = match["match_id"]
                reqstatsresult = self.api_facade.getStatsFromMatch(api_match_id)
                
                if self.__checkArrayIsOtherArray(constants.STATISTICS_TO_GET, reqstatsresult[api_match_id]["statistics"], "type"):
                    self.__insertStatsInArray(match, stats_matches_two_team, reqstatsresult[api_match_id]["statistics"], constants.STATISTICS_TO_GET)
                    
            for match in reqresult["firstTeam_lastResults"]:
                
                api_match_id = match["match_id"]
                reqstatsresult = self.api_facade.getStatsFromMatch(api_match_id)
                
                if self.__checkArrayIsOtherArray(constants.STATISTICS_TO_GET, reqstatsresult[api_match_id]["statistics"], "type"):
                    self.__insertStatsInArray(match, stats_first_team, reqstatsresult[api_match_id]["statistics"], constants.STATISTICS_TO_GET)
                
            for match in reqresult["secondTeam_lastResults"]:
                
                api_match_id = match["match_id"]
                reqstatsresult = self.api_facade.getStatsFromMatch(api_match_id)
                
                if self.__checkArrayIsOtherArray(constants.STATISTICS_TO_GET, reqstatsresult[api_match_id]["statistics"], "type"):
                    self.__insertStatsInArray(match, stats_second_team, reqstatsresult[api_match_id]["statistics"], constants.STATISTICS_TO_GET)
                
            result["firstTeam_VS_secondTeam"]=stats_matches_two_team
            result["firstTeam_lastResults"]=stats_first_team
            result["secondTeam_lastResults"]=stats_second_team
                    
            return result
        else:
            logging.error("No results for one of the two teams selected")
            raise Exception("No results for one of the two team selected")
    
    def __insertStatsInArray(self, match, array, statsArray, requiredStatsArray):
        """
        Create a dictionary of stats to insert in the array param
        """
        api_match_id = match["match_id"]
        
        elem = {"api_match_id" : api_match_id,
                "home_team" : match["match_hometeam_name"], 
                "away_team" : match["match_awayteam_name"],
                "home_team_score" : match["match_hometeam_score"],
                "away_team_score" : match["match_awayteam_score"],
        }
        for stat in statsArray:
            if stat["type"] in requiredStatsArray:
                elem[stat["type"]]={"home": stat["home"], "away": stat["away"]}
        array.append(elem)
            
    def __checkArrayIsOtherArray(self, array, second_array, key):
        """
        This method permits you to check if all the data in the first array is in the second array which us a 2d array with dictionary
        """
        count = len(array)
        i = 0
        for elem in array:
            for second_elem in second_array:
                if second_elem[key] == elem:
                    i+=1
        if i==count:
            return True
        else:
            return False
        
    def getUpcomingMatches(self, from_date, to_date):
        # Get the upcoming matches from DATE to DATE
        pass
    
    def save(self, prediction_winner, home_team_name, away_team_name, off_score_home_team, def_score_home_team, off_score_away_team, def_score_away_team, api_match_id="NULL"):
        """
        Save the prediction in the DB
        """
        return self.db_manager.insert(prediction_winner, home_team_name, away_team_name, off_score_home_team, def_score_home_team, off_score_away_team, def_score_away_team, api_match_id)
        pass