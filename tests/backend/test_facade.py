#!/usr/bin/python3
# Use : python3 test_facade.py | jq
#   jq is a pretty printer for json format in the terminal. Make sure to not print anything but json
#   sudo apt install jq
import os
import sys

# insert the "football-prediction" directory into the sys.path
sys.path.insert(1, os.path.abspath(".."))

from lib.api.api_facade import ApiFacade
from dotenv import load_dotenv
from datetime import datetime
import os
import asyncio

load_dotenv()

myFacade = ApiFacade(os.getenv("API_KEY"), '../log/app.log')

async def async_main():
    #Head To Head
    response = await myFacade.get_H2H("Chelsea", "Arsenal")
    print(response)

    # # Countries
    response = await myFacade.get_countries()
    print(response)

    # Competitions
    response = await myFacade.get_competitions(124)
    print(response)

    # Competitions without param
    response = await myFacade.get_competitions()
    print(response)

    # Upcoming matches
    response = await myFacade.get_matches_in_interval("2018-04-01", "2020-04-01", 148)
    print(response)

    # Teams
    response = await myFacade.get_teams_from_league(148)
    print(response)

    # Statistic from match
    response = await myFacade.get_stats_from_match(24562)
    print(response)
    
if __name__ == '__main__':
    asyncio.run(async_main())
    