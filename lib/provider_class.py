#!/usr/bin/python3
import os
from dotenv import load_dotenv
import logging

from .api.api_facade import ApiFacade
from .sql.db_manager import DbManager
import lib.constants

from dateutil.relativedelta import relativedelta
from datetime import datetime
import asyncio


class Provider:
    """
    This provider is used in the app.py file and in the prediction_class.py
    """
    __instance = None
    def __new__(cls, log_path='./log/app.log'):
        if cls.__instance is None:
            cls.__instance = super(Provider, cls).__new__(cls)    
            load_dotenv()
            logging.basicConfig(filename=log_path, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
            cls.__api_facade = ApiFacade(os.getenv("API_KEY"), log_path)
            cls.__db_manager = DbManager("127.0.0.1", os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), log_path)
        return cls.__instance
    
    async def get_matches_from_to_db(self, from_date, to_date, league_id=""):
        """
        Get matches from date to date from the db
        """
        return self.__db_manager.get_matches_from_to(from_date, to_date, league_id)
            
    async def get_teams_from_league(self, league_id):
        """
        Get the team list from a league
        """
        response = await self.__api_facade.get_teams_from_league(league_id)
        for team in response:
            # We must put this line because there is a bug with the API 
            if team["team_name"] == "Manchester United":
                team["team_name"] = "Manchester Utd"
        return response
    
    async def get_teams_with_team_id(self, team_id):
        """
        Get the team list from a league
        """
        response = await self.__api_facade.get_teams_with_team_id(team_id)
        for team in response:
            # We must put this line because there is a bug with the API 
            if team["team_name"] == "Manchester United":
                team["team_name"] = "Manchester Utd"
        
        return response
    
    async def get_all_stats_from_teams(self, first_team_name, second_team_name):
        """
        This method try to get games from the two teams in the DB. If there is no data in the DB, it will get data from the API and then save it in the DB.
        """
        response = ""
        
        try:
            now = datetime.now().date()
            three_months_before = now - relativedelta(months=6)
            now = now.strftime("%Y-%m-%d")
            three_months_before = three_months_before.strftime("%Y-%m-%d")
            if len(self.get_api_call_from_today(first_team_name,second_team_name))>0:
                # Try catch cause the method below can throw an exception if we haven't enought stats
                try:
                    response = self.get_all_stats_from_teams_db(first_team_name, second_team_name, three_months_before, now)
                except Exception:
                    raise Exception("Data unavailable for this prediction")
                    
            else:
                raise APICallNotFound("No API call made today")
            # We must make an await because the method is an async else it will create an error
            await asyncio.sleep(0)
            
        except APICallNotFound:
            if len(self.get_api_call_from_today(first_team_name,second_team_name)) <= 0:    
                response = await self.get_all_stats_from_teams_api(first_team_name, second_team_name)
                self.save_api_call(first_team_name, second_team_name)
                for result in response:
                    for match in response[result]:
                        try:
                            self.save_match_with_stats(match["api_match_id"], 
                                                    match["date"],
                                                    match["time"],
                                                    match["league_id"],
                                                    match["league_name"],
                                                    match["home_team"],
                                                    match["away_team"],
                                                    match["home_team_score"], 
                                                    match["away_team_score"], 
                                                    match["stats"])
                        except Exception:
                            logging.warning("Could not save the match")
        
        return response
          
    async def get_all_stats_from_teams_api(self, first_team_name, second_team_name):
        """
        Make a call to the API using getH2H and make a treatment to have the stats for each match of the two different teams
        """
        reqresult = await self.__api_facade.get_H2H(first_team_name, second_team_name)

        result = {}
        stats_matches_two_team = []
        stats_first_team = []
        stats_second_team = []
        
        
        # We check the last results of the teams aren't empty
        if len(reqresult["firstTeam_lastResults"]) > lib.constants.MIN_OF_GAMES_TO_MAKE_PREDICTION and len(reqresult["secondTeam_lastResults"]) > lib.constants.MIN_OF_GAMES_TO_MAKE_PREDICTION:
            
            
            reqstatsresult_firstTeam_vs_secondTeam = await asyncio.wait([self.__api_facade.get_stats_from_match(match["match_id"]) for match in reqresult["firstTeam_VS_secondTeam"]])
            reqstatsresult_firstTeam_lastResults = await asyncio.wait([self.__api_facade.get_stats_from_match(match["match_id"]) for match in reqresult["firstTeam_lastResults"]])
            reqstatsresult_secondTeam_lastResults = await asyncio.wait([self.__api_facade.get_stats_from_match(match["match_id"]) for match in reqresult["secondTeam_lastResults"]])
            

            for match in reqresult["firstTeam_VS_secondTeam"]:   
                api_match_id = match["match_id"]
                # Reqstatsresult is an array of Set but we only want the first one (which contains the tasks)
                for task in reqstatsresult_firstTeam_vs_secondTeam[0]:
                    stats_of_match = task.result()
                    for stat_match_id in task.result():
                        if stat_match_id == api_match_id:                            
                            if  self.__check_array_is_in_other_array(lib.constants.STATISTICS_TO_GET, stats_of_match[stat_match_id]["statistics"], "type"):
                                self.__insert_stats_in_array_for_api(match, stats_matches_two_team, stats_of_match[stat_match_id]["statistics"], lib.constants.STATISTICS_TO_GET)
                    
            for match in reqresult["firstTeam_lastResults"]:   
                api_match_id = match["match_id"]
                # Reqstatsresult is an array of Set but we only want the first one (which contains the tasks)
                for task in reqstatsresult_firstTeam_lastResults[0]:
                    stats_of_match = task.result()
                    for stat_match_id in task.result():
                        if stat_match_id == api_match_id:                            
                            if  self.__check_array_is_in_other_array(lib.constants.STATISTICS_TO_GET, stats_of_match[stat_match_id]["statistics"], "type"):
                                self.__insert_stats_in_array_for_api(match, stats_first_team, stats_of_match[stat_match_id]["statistics"], lib.constants.STATISTICS_TO_GET)
                
            for match in reqresult["secondTeam_lastResults"]:
                api_match_id = match["match_id"]
                # Reqstatsresult is an array of Set but we only want the first one (which contains the tasks)
                for task in reqstatsresult_secondTeam_lastResults[0]:
                    stats_of_match = task.result()
                    for stat_match_id in task.result():
                        if stat_match_id == api_match_id:                            
                            if  self.__check_array_is_in_other_array(lib.constants.STATISTICS_TO_GET, stats_of_match[stat_match_id]["statistics"], "type"):
                                self.__insert_stats_in_array_for_api(match, stats_second_team, stats_of_match[stat_match_id]["statistics"], lib.constants.STATISTICS_TO_GET)
                
                
            result["firstTeam_VS_secondTeam"]=stats_matches_two_team
            result["firstTeam_lastResults"]=stats_first_team
            result["secondTeam_lastResults"]=stats_second_team

            return result
        else:
            logging.error("No results for one of the two teams selected")
            raise NoMatchError("No results for one of the two team selected")
        
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
                logging.error("No stats for one of the two teams selected")
                raise StatsError("No stats for one of the two team selected")
            
            return result
        else:
            logging.error("No results for one of the two teams selected")
            raise NoMatchError("No results for one of the two team selected")
    
    def get_api_call_from_today(self, first_team_name, second_team_name):
        """
        Get the API call from today
        """
        now = datetime.now().date()
        return self.__db_manager.get_api_call(first_team_name, second_team_name, now)
        
    async def get_previous_matches_predictions(self, from_date, to_date, league_id, league_name, out_dict):
        """
        Get the predictions of the previous matches with their result
        """
        response = self.get_predictions_in_interval_from_db(from_date, to_date, league_id)
        result = []
        
        resp_async = await asyncio.wait([self.__api_facade.get_match_infos(prediction["api_match_id"]) for prediction in response])
        array_of_matchs = []
        for item in resp_async[0]:
            array_of_matchs.append(item.result())
        
        for prediction in response:
            for list_of_match in array_of_matchs:
                match_info = list_of_match[0]
                print(match_info["match_id"], "==", prediction["api_match_id"])
                if len(match_info)>0 and int(match_info["match_id"]) == int(prediction["api_match_id"]): # Check if we got some data from the API
                    date_match = datetime.strptime(match_info["match_date"], "%Y-%m-%d").date()
                    print(date_match)
                    if date_match < to_date:
                        match = {
                            "Home" : prediction["home_team_name"],
                            "Away" : prediction["away_team_name"],
                            "Prediction winner" : prediction["prediction"],
                            "Real home score" : match_info["match_hometeam_score"],
                            "Real away score" : match_info["match_awayteam_score"],
                            "League" : prediction["league_name"],
                            "Date" : date_match
                        }
                        print(match)
                        result.append(match)
                    
                        
        out_dict[league_name] = result
        return result
    
    def get_predictions_in_interval_from_db(self, from_date, to_date, league_id=""):
        """
        Get the predictions from a date to an other [only with an api_match_id]
        """
        return self.__db_manager.get_predictions_in_interval(from_date, to_date, league_id)
        
    async def get_matches_in_interval(self, from_date, to_date, league_id=""):
        """
        Get the matches from a date to an other [in a specific a league]
        """
        return await self.__api_facade.get_matches_in_interval(from_date,to_date,league_id)
    
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
    
    def save_api_call(self, first_team_name, second_team_name):
        self.__db_manager.insert_api_call_in_history(first_team_name, second_team_name)
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
                "date" : match["match_date"],
                "time" : match["match_time"],
                "league_id" : match["league_id"],
                "league_name" : match["league_name"],
                "stats" : {}
        }
        
        for stat in stats_array:
            if stat["type"] in required_stats_array:
                elem["stats"][stat["type"]]={"home": stat["home"], "away": stat["away"]}
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
                "date" : match["date"],
                "time" : match["time"],
                "stats" : {}
        }
        
        for stat in stats_array:
            if stat["id_match"] == match["id"]:
                if stat["type"] in required_stats_array:
                    elem["stats"][stat["type"]]={"home": stat["home"], "away": stat["away"]}
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
        
        for second_elem in second_array:
            if second_elem[key] in array and second_elem["id_match"]==id:
                i+=1                    
        if i==count:
            return True
        else:
            return False
        
    def disconnect(self):
        self.__db_manager.disconnect()

class StatsError(Exception):
    pass

class NoMatchError(Exception):
    pass

class APICallNotFound(Exception):
    pass