#!/usr/bin/python3
import os
from dotenv import load_dotenv
import logging
from api.api_facade import ApiFacade
from sql.db_manager import DbManager
import constants



class Provider:
    def __init__(self, log_path='./log/app.log'):
        load_dotenv()
        logging.basicConfig(filename=log_path, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
        self.api_facade = ApiFacade(os.getenv("API_KEY"), log_path)
        self.db_manager = DbManager("127.0.0.1", os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), log_path)
        
    def getAllStatsFromTeamsApi(self, first_team_name, second_team_name):
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
                
                if self.__checkArrayIsInOtherArray(constants.STATISTICS_TO_GET, reqstatsresult[api_match_id]["statistics"], "type"):
                    self.__insertStatsInArrayForApi(match, stats_matches_two_team, reqstatsresult[api_match_id]["statistics"], constants.STATISTICS_TO_GET)
                    
            for match in reqresult["firstTeam_lastResults"]:
                
                api_match_id = match["match_id"]
                reqstatsresult = self.api_facade.getStatsFromMatch(api_match_id)
                
                if self.__checkArrayIsInOtherArray(constants.STATISTICS_TO_GET, reqstatsresult[api_match_id]["statistics"], "type"):
                    self.__insertStatsInArrayForApi(match, stats_first_team, reqstatsresult[api_match_id]["statistics"], constants.STATISTICS_TO_GET)
                
            for match in reqresult["secondTeam_lastResults"]:
                
                api_match_id = match["match_id"]
                reqstatsresult = self.api_facade.getStatsFromMatch(api_match_id)
                
                if self.__checkArrayIsInOtherArray(constants.STATISTICS_TO_GET, reqstatsresult[api_match_id]["statistics"], "type"):
                    self.__insertStatsInArrayForApi(match, stats_second_team, reqstatsresult[api_match_id]["statistics"], constants.STATISTICS_TO_GET)
                
            result["firstTeam_VS_secondTeam"]=stats_matches_two_team
            result["firstTeam_lastResults"]=stats_first_team
            result["secondTeam_lastResults"]=stats_second_team
                    
            return result
        else:
            logging.error("No results for one of the two teams selected")
            raise Exception("No results for one of the two team selected")
        
    def getAllStatsFromTeamsDB(self, first_team_name, second_team_name, date=""):
        """
        Get all the matches between the two teams in params with the stats of each matches
        """
        reqmatch = self.db_manager.getMatchesWithSpecificTeams(first_team_name, second_team_name, date)
        reqstats = self.db_manager.getStatsOfMatchesWithSpecificTeams(first_team_name, second_team_name, date)
        
        result = {}
        stats_matches_two_team = []
        stats_first_team = []
        stats_second_team = []
        
        
        if len(reqmatch) > 0 and len(reqstats) > 0:
            for match in reqmatch:
                #Check for the game with the two teams
                if (match["home_team_name"] == first_team_name or match["away_team_name"] == first_team_name) and (match["home_team_name"] == second_team_name or match["away_team_name"] == second_team_name):
                    if self.__checkArrayIsContainedWithSpecificId(constants.STATISTICS_TO_GET, reqstats, "type", match["id"]):
                        self.__insertStatsInArrayForDB(match, stats_matches_two_team, reqstats, constants.STATISTICS_TO_GET)
                        
                elif (match["home_team_name"] == first_team_name or match["away_team_name"] == first_team_name):
                    if self.__checkArrayIsContainedWithSpecificId(constants.STATISTICS_TO_GET, reqstats, "type", match["id"]):
                        self.__insertStatsInArrayForDB(match, stats_first_team, reqstats, constants.STATISTICS_TO_GET)
                    
                elif (match["home_team_name"] == second_team_name or match["away_team_name"] == second_team_name):    
                    if self.__checkArrayIsContainedWithSpecificId(constants.STATISTICS_TO_GET, reqstats, "type", match["id"]):
                        self.__insertStatsInArrayForDB(match, stats_second_team, reqstats, constants.STATISTICS_TO_GET)
                
            result["firstTeam_VS_secondTeam"]=stats_matches_two_team
            result["firstTeam_lastResults"]=stats_first_team
            result["secondTeam_lastResults"]=stats_second_team
                    
            return result
        else:
            logging.error("No results for one of the two teams selected")
            raise Exception("No results for one of the two team selected")
        pass
    
   
        
    def getMatchesInInterval(self, from_date, to_date, league_id=""):
        """
        Get the matches from a date to an other [in a specific a league]
        """
        return self.api_facade.getMatchesInInterval(from_date,to_date,league_id)
    
    def saveMatchWithStats(self, match_id, match_date, match_time, league_id, league_name, hometeam_name, awayteam_name, hometeam_score, awayteam_score, stats_array):
        """
        Save the match in the DB with its stats
        """
        return self.db_manager.insertMatchWithStats(match_id, match_date, match_time, league_id, league_name, hometeam_name, awayteam_name, hometeam_score, awayteam_score, stats_array)
        
    
    def savePrediction(self, prediction_winner, home_team_name, away_team_name, off_score_home_team, def_score_home_team, off_score_away_team, def_score_away_team, api_match_id="NULL"):
        """
        Save the prediction in the DB
        """
        return self.db_manager.insertPrediction(prediction_winner, home_team_name, away_team_name, off_score_home_team, def_score_home_team, off_score_away_team, def_score_away_team, api_match_id)
        pass
    
    def __insertStatsInArrayForApi(self, match, array, stats_array, required_stats_array):
        """
        Create a dictionary of stats to insert in the array param. Use with api names
        The structure of the API is not the same as the DB
        """

        elem = {"api_match_id" : match["match_id"],
                "home_team" : match["match_hometeam_name"], 
                "away_team" : match["match_awayteam_name"],
                "home_team_score" : match["match_hometeam_score"],
                "away_team_score" : match["match_awayteam_score"],
        }
        for stat in stats_array:
            if stat["type"] in required_stats_array:
                elem[stat["type"]]={"home": stat["home"], "away": stat["away"]}
        array.append(elem)
    
    def __insertStatsInArrayForDB(self, match, array, stats_array, required_stats_array):
        """
        Create a dictionary to insert in the array param. Use with the db names
        The structure of the DB is not the same as the API
        """
        
        elem = {"api_match_id" : match["id"],
                "home_team" : match["home_team_name"], 
                "away_team" : match["away_team_name"],
                "home_team_score" : match["home_team_score"],
                "away_team_score" : match["away_team_score"],
        }
        
        for stat in stats_array:
            if stat["id_match"] == match["id"]:
                if stat["type"] in required_stats_array:
                    elem[stat["type"]]={"home": stat["home"], "away": stat["away"]}
        array.append(elem)
        
            
    def __checkArrayIsInOtherArray(self, array, second_array, key):
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
        
    def __checkArrayIsContainedWithSpecificId(self, array, second_array, key, id):
        """
        This method permits you to check if all the data in the first array is in the second array with the specific id
        """
        count = len(array)
        
        i = 0
        for elem in array:
            for second_elem in second_array:
                if second_elem[key] == elem and second_elem["id_match"]==id:
                    i+=1
        if i==count:
            return True
        else:
            return False