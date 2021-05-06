#!/usr/bin/python3
import os
from dotenv import load_dotenv
import logging
from .api.api_facade import ApiFacade
from .sql.db_manager import DbManager
import lib.constants
import datetime



class Provider:
    """
    This provider is used in the app.py file and in the prediction_class.py
    """
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Provider, cls).__new__(cls)    
            load_dotenv()
            log_path = './log/app.log'
            logging.basicConfig(filename=log_path, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
            cls.__api_facade = ApiFacade(os.getenv("API_KEY"), log_path)
            cls.__db_manager = DbManager("127.0.0.1", os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), log_path)
        return cls.__instance
    
    def get_matches_from_to_db(self, from_date, to_date, league_id=""):
        """
        Get matches from date to date from the db
        """
        return self.__db_manager.get_matches_from_to(from_date, to_date, league_id)
            
    def get_teams_from_league(self, league_id):
        """
        Get the team list from a league
        """
        return self.__api_facade.get_teams_from_league(league_id)
    
    def get_teams_with_team_id(self, team_id):
        """
        Get the team list from a league
        """
        return self.__api_facade.get_teams_with_team_id(team_id)
    
    def get_all_stats_from_teams_api(self, first_team_name, second_team_name):
        """
        Make a call to the API using getH2H and make a treatment to have the stats for each match of the two different teams
        """
        reqresult = self.__api_facade.get_H2H(first_team_name, second_team_name)
        
        result = {}
        stats_matches_two_team = []
        stats_first_team = []
        stats_second_team = []
        
        # We check the last results of the teams aren't empty
        if len(reqresult["firstTeam_lastResults"]) > 0 and len(reqresult["secondTeam_lastResults"]) > 0:
            
            for match in reqresult["firstTeam_VS_secondTeam"]:
                
                api_match_id = match["match_id"]
                reqstatsresult = self.__api_facade.get_stats_from_match(api_match_id)
                
                if self.__check_array_is_in_other_array(lib.constants.STATISTICS_TO_GET, reqstatsresult[api_match_id]["statistics"], "type"):
                    self.__insert_stats_in_array_for_api(match, stats_matches_two_team, reqstatsresult[api_match_id]["statistics"], lib.constants.STATISTICS_TO_GET)
                    
            for match in reqresult["firstTeam_lastResults"]:
                
                api_match_id = match["match_id"]
                reqstatsresult = self.__api_facade.get_stats_from_match(api_match_id)
                
                if self.__check_array_is_in_other_array(lib.constants.STATISTICS_TO_GET, reqstatsresult[api_match_id]["statistics"], "type"):
                    self.__insert_stats_in_array_for_api(match, stats_first_team, reqstatsresult[api_match_id]["statistics"], lib.constants.STATISTICS_TO_GET)
                
            for match in reqresult["secondTeam_lastResults"]:
                
                api_match_id = match["match_id"]
                reqstatsresult = self.__api_facade.get_stats_from_match(api_match_id)
                
                if self.__check_array_is_in_other_array(lib.constants.STATISTICS_TO_GET, reqstatsresult[api_match_id]["statistics"], "type"):
                    self.__insert_stats_in_array_for_api(match, stats_second_team, reqstatsresult[api_match_id]["statistics"], lib.constants.STATISTICS_TO_GET)
                
            result["firstTeam_VS_secondTeam"]=stats_matches_two_team
            result["firstTeam_lastResults"]=stats_first_team
            result["secondTeam_lastResults"]=stats_second_team
                    

            return result
        else:
            logging.error("No results for one of the two teams selected")
            raise Exception("No results for one of the two team selected")
        
    def get_all_stats_from_teams_db(self, first_team_name, second_team_name, from_date="", to_date=""):
        """
        Get all the matches between the two teams in params with the stats of each matches
        """
        reqmatch = self.__db_manager.get_matches_with_specific_teams(first_team_name, second_team_name, from_date, to_date)
        reqstats = self.__db_manager.get_stats_of_matches_with_specific_teams(first_team_name, second_team_name, from_date, to_date)
        
        
        result = {}
        stats_matches_two_team = []
        stats_first_team = []
        stats_second_team = []
        
        # We check if the requests aren't empty
        
        if len(reqmatch) > 0 and len(reqstats) > 0:
            for match in reqmatch:
                #Check for the game with the two teams
                if (match["home_team_name"] == first_team_name or match["away_team_name"] == first_team_name) and (match["home_team_name"] == second_team_name or match["away_team_name"] == second_team_name):
                    if self.__check_array_is_contained_with_specific_id(lib.constants.STATISTICS_TO_GET, reqstats, "type", match["id"]):
                        self.__insert_stats_in_array_for_db(match, stats_matches_two_team, reqstats, lib.constants.STATISTICS_TO_GET)
                        
                elif (match["home_team_name"] == first_team_name or match["away_team_name"] == first_team_name):
                    if self.__check_array_is_contained_with_specific_id(lib.constants.STATISTICS_TO_GET, reqstats, "type", match["id"]):
                        self.__insert_stats_in_array_for_db(match, stats_first_team, reqstats, lib.constants.STATISTICS_TO_GET)
                    
                elif (match["home_team_name"] == second_team_name or match["away_team_name"] == second_team_name):    
                    if self.__check_array_is_contained_with_specific_id(lib.constants.STATISTICS_TO_GET, reqstats, "type", match["id"]):
                        self.__insert_stats_in_array_for_db(match, stats_second_team, reqstats, lib.constants.STATISTICS_TO_GET)
                
            if len(stats_first_team)>0 and len(stats_second_team)>0 :
        
                result["firstTeam_VS_secondTeam"]=stats_matches_two_team
                result["firstTeam_lastResults"]=stats_first_team
                result["secondTeam_lastResults"]=stats_second_team
            else:
                logging.error("No results for one of the two teams selected")
                return None
            
            return result
        else:
            logging.error("No results for one of the two teams selected")
            raise Exception("No results for one of the two team selected")
    
    def get_previous_matches_predictions(self, from_date, to_date, league_id=""):
        """
        Get the predictions of the previous matches with their result
        """
        response = self.get_predictions_in_interval_from_db(from_date, to_date, league_id)
        
        result = []
        for prediction in response:
            match_info = self.__api_facade.get_match_infos(prediction["api_match_id"])
            
            if len(match_info)>0: # Check if we got some data from the API
                
                
                date_match = datetime.datetime.strptime(match_info[0]["match_date"], "%Y-%m-%d").date()
                if date_match < to_date:
                    match = {
                        "Home" : prediction["home_team_name"],
                        "Away" : prediction["away_team_name"],
                        "Prediction winner" : prediction["prediction"],
                        "Real home score" : match_info[0]["match_hometeam_score"],
                        "Real away score" : match_info[0]["match_awayteam_score"],
                        "League" : prediction["league_name"],
                        "Date" : date_match
                    }
                    result.append(match)
        return result
    
    def get_predictions_in_interval_from_db(self, from_date, to_date, league_id=""):
        """
        Get the predictions from a date to an other [only with an api_match_id]
        """
        return self.__db_manager.get_predictions_in_interval(from_date, to_date, league_id)
        
    def get_matches_in_interval(self, from_date, to_date, league_id=""):
        """
        Get the matches from a date to an other [in a specific a league]
        """
        return self.__api_facade.get_matches_in_interval(from_date,to_date,league_id)
    
    def save_match_with_stats(self, match_id, match_date, match_time, league_id, league_name, hometeam_name, awayteam_name, hometeam_score, awayteam_score, stats_array):
        """
        Save the match in the DB with its stats
        """
        return self.__db_manager.insert_match_with_stats(match_id, match_date, match_time, league_id, league_name, hometeam_name, awayteam_name, hometeam_score, awayteam_score, stats_array)
        
    def save_prediction(self, prediction_winner, home_team_name, away_team_name, league_id="NULL", league_name="NULL", date_of_game="NULL", api_match_id="NULL"):
        """
        Save the prediction in the DB
        """
        return self.__db_manager.insert_prediction(prediction_winner, home_team_name, away_team_name, league_id, league_name, date_of_game, api_match_id)
        pass
    
    def get_prediction_with_specific_teams_after_date(self, first_team_name, second_team_name, creation_date):
        """
        Returns one prediction made at a specific date
        """
        return self.__db_manager.get_one_prediction_with_specific_teams_after_date(first_team_name, second_team_name, creation_date)
    
    def get_one_prediction_per_day_with_specific_teams(self, first_team_name, second_team_name):
        return self.__db_manager.get_one_prediction_per_day_with_specific_teams(first_team_name, second_team_name)
        
    
    def __insert_stats_in_array_for_api(self, match, array, stats_array, required_stats_array):
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
    
    def __insert_stats_in_array_for_db(self, match, array, stats_array, required_stats_array):
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
        
            
    def __check_array_is_in_other_array(self, array, second_array, key):
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
        
    def __check_array_is_contained_with_specific_id(self, array, second_array, key, id):
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