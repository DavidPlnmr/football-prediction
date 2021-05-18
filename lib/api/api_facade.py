#!/usr/bin/python3
import requests
import os
import json
from dotenv import load_dotenv
import logging
import time

class ApiFacade:
    """
    Facade to call the endpoints of the API.
    """
    def __init__(self, api_key, log_path):
        self.api_key = api_key
        logging.basicConfig(filename=log_path, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
        
    def __get_action(self, request_params):
        """
        Private method to call any endpoint of the API
        """
        start_time = time.perf_counter()
        response = requests.get(f'https://apiv2.apifootball.com/?APIkey={self.api_key}&{request_params}')
        end_time = time.perf_counter()
        
        if response.status_code == 200: # Code 200 = OK. Healthy connection
            obj = json.loads(response.content.decode('utf-8'))
            # Check if obj contains error so there is problem in the API side
            if 'error' in obj:
                logging.error(f"Error {obj['error']} returned from the API with message : {obj['message']}")    
                raise Exception(f"Error with the API : {obj['message']}")
            else: # No error from the API we can return the result
                logging.info(f"Request to the API with the params: {request_params}. Time lapsed {end_time-start_time}")
                return obj # decode to get the content in string
        else:
            # Error from the library
            logging.error(f"Could not connect to the API. Error : {response.status_code} | Params : {request_params}")
            raise Exception("Could not connect to the API.")
    
    def get_match_infos(self, match_id):
        """
        Get the last results of each teams and the last results of each matchs between them both
        """
        endpoint_action = "get_events"
        return self.__get_action(f'action={endpoint_action}&match_id={match_id}')
        
    def get_H2H(self, first_team_name, second_team_name):
        """
        Get the last results of each teams and the last results of each matchs between them both
        """
        endpoint_action = "get_H2H"
        return self.__get_action(f'action={endpoint_action}&firstTeam={first_team_name}&secondTeam={second_team_name}')
    
    def get_matches_in_interval(self, from_date, to_date, league_id=""):
        """
        Get the matches in an interval of two dates
        """
        #The format of the must be yyyy-mm--dd
        endpoint_action = "get_events"
        params = f'action={endpoint_action}&from={from_date}&to={to_date}'
        params += f"&league_id={league_id}" if (type(league_id) == int) else ''
        return self.__get_action(params)
    
    def get_countries(self):
        """
        Get countries available in the API
        """
        endpoint_action = "get_countries"
        return self.__get_action(f'action={endpoint_action}')
    
    def get_competitions(self, country_id = ""):
        """
        Get competitions in a specific country
        """
        endpoint_action = "get_leagues"
        if type(country_id)==int:
            endpoint_action+=f"&country_id={country_id}"
        return self.__get_action(f'action={endpoint_action}')
    
    def get_teams_from_league(self, league_id):
        """
        Get all the teams in the specified league_id
        """
        endpoint_action = "get_teams"
        return self.__get_action(f'action={endpoint_action}&league_id={league_id}')
    
    def get_teams_with_team_id(self, team_id):
        """
        Get all the teams in the specified league_id
        """
        endpoint_action = "get_teams"
        return self.__get_action(f'action={endpoint_action}&team_id={team_id}')
    
    def get_stats_from_match(self, match_id):
        """
        Get the statistics of a specific match
        """
        endpoint_action = "get_statistics"
        return self.__get_action(f'action={endpoint_action}&match_id={match_id}')