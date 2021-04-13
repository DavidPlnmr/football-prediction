#!/usr/bin/python3
# Use : python3 test_facade.py | jq
#   jq is a pretty printer for json format in the terminal. Make sure to not print anything but json
#   sudo apt install jq
from api_facade import ApiFacade
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

myFacade = ApiFacade(os.getenv("wAPI_KEY"))

#Head To Head
'''response = myFacade.getH2H("Chelsea", "Arsenal")
print(response)'''

# Countries
response = myFacade.getCountries()
#print(response)

# Competitions
'''response = myFacade.getCompetitions()
print(response)'''

# Competitions without param
'''response = myFacade.getCompetitions()
print(response)'''

# Upcoming matches
'''response = myFacade.getUpcomingMatches("2021-03-30", "2021-04-02")
print(response)'''

# Teams
'''response = myFacade.getTeams(148)
print(response)'''