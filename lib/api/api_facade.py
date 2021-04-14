#!/usr/bin/python3
import requests
import os
import json
from dotenv import load_dotenv
import logging

class ApiFacade:
    """
    Facade to call the endpoints of the API.
    """
    def __init__(self, api_key):
        self.api_key = api_key
        logging.basicConfig(filename='./log/app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
        logging.info("Correctly found the log file")
        
    def __getAction(self, request_params):
        """
        Private method to call any endpoint of the API
        """
        response = requests.get(f'https://apiv2.apifootball.com/?APIkey={self.api_key}&{request_params}')

        if response.status_code == 200: # Code 200 = OK. Healthy connection
            obj = json.loads(response.content.decode('utf-8'))
            # Check if obj contains error so there is problem in the API side
            if 'error' in obj:
                logging.error(f"Error {obj['error']} returned from the API with message : {obj['message']}")    
                raise Exception(f"Error with the API : {obj['message']}")
            else: # No error from the API we can return the result
                logging.info(f"Request to the API with the params: {request_params}")
                return obj # decode to get the content in string
        else:
            # Error from the library
            logging.error("Happened during the request to the API")
            raise Exception("Could not connect to the API.")
        
    def getH2H(self, first_team_name, second_team_name):
        """
        Get the last results of each teams and the last results of each matchs between them both
        """
        endpoint_action = "get_H2H"
        return self.__getAction(f'action={endpoint_action}&firstTeam={first_team_name}&secondTeam={second_team_name}')
    
    def getMatchesInInterval(self, from_date, to_date):
        """
        Get the matches in an interval of two dates
        """
        #The format of the must be yyyy-mm--dd
        endpoint_action = "get_events"
        return self.__getAction(f'action={endpoint_action}&from={from_date}&to={to_date}')
    
    def getCountries(self):
        """
        Get countries available in the API
        """
        endpoint_action = "get_countries"
        return self.__getAction(f'action={endpoint_action}')
    
    def getCompetitions(self, country_id):
        """
        Get competitions in a specific country
        """
        endpoint_action = "get_leagues"
        return self.__getAction(f'action={endpoint_action}&country_id={country_id}')
    
    def getCompetitions(self):
        """
        Get all the competitions available with your plan
        """
        endpoint_action = "get_leagues"
        return self.__getAction(f'action={endpoint_action}')
    
    def getTeams(self, league_id):
        """
        Get all the teams in the specified league_id
        """
        endpoint_action = "get_teams"
        return self.__getAction(f'action={endpoint_action}&league_id={league_id}')
    
    def getStatsFromMatch(self, match_id):
        """
        Get the statistics of a specific match
        """
        endpoint_action = "get_statistics"
        return self.__getAction(f'action={endpoint_action}&match_id={match_id}')