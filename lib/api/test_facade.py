#!/usr/bin/python3
# Use : python3 test_facade.py | jq
#   jq is a pretty printer for json format in the terminal. Make sure to not print anything but json
#   sudo apt install jq
from api_facade import ApiFacade
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

myFacade = ApiFacade(os.getenv("API_KEY"), '../log/app.log')

#Head To Head
'''response = myFacade.getH2H("Chelsea", "Arsenal")
print(response)'''

# Countries
'''response = myFacade.getCountries()
print(response)'''

# Competitions
'''response = myFacade.getCompetitions()
print(response)'''

# Competitions without param
'''response = myFacade.getCompetitions()
print(response)'''

# Upcoming matches
'''response = myFacade.getMatchesInInterval("2018-04-01", "2020-04-01", 148)
print(response)'''

# Teams
'''response = myFacade.getTeams(148)
print(response)'''

# Statistic from match
'''response = myFacade.getStatsFromMatch(24562)
print(response['24562']['statistics'][0])'''