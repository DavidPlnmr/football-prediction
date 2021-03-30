# Use : python3 ApiFacade.py | jq
#   jq is a pretty printer for json format in the terminal. Make sure to not print anything but json
#   sudo apt install jq
import requests
from dotenv import load_dotenv
import os
load_dotenv()
    
class ApiFacade:
    def __init__(self, api_key):
        self.api_key = api_key
        
        
    def getAction(self, request_params):
        response = requests.get('https://apiv2.apifootball.com/?APIkey={key}&{params}'.format(key=self.api_key, params=request_params))

        if response.status_code == 200: # Code 200 = OK. Healthy connection
            return response.content.decode('utf-8') # decode to get the content in string
        
    def getH2H(self, first_team_name, second_team_name):
        endpoint_action = "get_H2H"
        return self.getAction('action={action}&firstTeam={first_team}&secondTeam={second_team}'.format(action=endpoint_action, first_team = first_team_name, second_team = second_team_name))
    
    def getUpcomingMatches(self, from_date, to_date, league_id):
        pass
    
    def getCountries(self):
        endpoint_action = "get_countries"
        return self.getAction('action={action}'.format(action=endpoint_action))
    
    def getCompetitions(self, country_id):
        endpoint_action = "get_leagues"
        return self.getAction('action={action}&'.format(action=endpoint_action))
    
    def getTeams(self, league_id):
        pass
        

myFacade = ApiFacade(os.getenv("API_KEY"))

#Head To Head
'''response = myFacade.getH2H("Chelsea", "Arsenal")
print(response)'''

# Countries
'''response = myFacade.getCountries()
print(response)'''