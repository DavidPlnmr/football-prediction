#!/usr/bin/python3
# Use : python3 ApiFacade.py | jq
#   jq is a pretty printer for json format in the terminal. Make sure to not print anything but json
#   sudo apt install jq
import requests
import os
import json
from dotenv import load_dotenv
import logging

class ApiFacade:
    def __init__(self, api_key):
        self.api_key = api_key
        logging.basicConfig(filename='../log/app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
        logging.info("Correctly found the log file")
        
    def __getAction(self, request_params):
        response = requests.get(f'https://apiv2.apifootball.com/?APIkey={self.api_key}&{request_params}')

        if response.status_code == 200: # Code 200 = OK. Healthy connection
            obj = json.loads(response.content.decode('utf-8'))
            logging.info(f"Request to the API with the params: {request_params}")
            return obj # decode to get the content in string
        else:
            logging.error("Happened during the request to the API")
            raise Exception("Could not connect to the API")
            
        #TODO : Manage other status code -> Exception
        
    def getH2H(self, first_team_name, second_team_name):
        endpoint_action = "get_H2H"
        return self.__getAction(f'action={endpoint_action}&firstTeam={first_team_name}&secondTeam={second_team_name}')
    
    def getUpcomingMatches(self, from_date, to_date):
        #The format of the must be yyyy-mm--dd
        endpoint_action = "get_events"
        return self.__getAction(f'action={endpoint_action}&from={from_date}&to={to_date}')
    
    def getCountries(self):
        endpoint_action = "get_countries"
        return self.__getAction(f'action={endpoint_action}')
    
    def getCompetitions(self, country_id):
        endpoint_action = "get_leagues"
        return self.__getAction(f'action={endpoint_action}&country_id={country_id}')
    
    def getCompetitions(self):
        endpoint_action = "get_leagues"
        return self.__getAction(f'action={endpoint_action}')
    
    def getTeams(self, league_id):
        endpoint_action = "get_teams"
        return self.__getAction(f'action={endpoint_action}&league_id={league_id}')
    
    def getStatsFromMatch(self, match_id):
        endpoint_action = "get_statistics"
        return self.__getAction(f'action={endpoint_action}&match_id={match_id}')