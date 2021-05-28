#!/usr/bin/python3
import os
import sys

# insert the "football-prediction" directory into the sys.path
sys.path.insert(1, os.path.abspath(".."))

from lib.provider_class import *

prov = Provider("../log/app.log")

async def main():
    #print(await prov.get_all_stats_from_teams_api("Chelsea", "Burnley"))
    #print(prov.get_all_stats_from_teams_db("Chelsea", "Burnley"))

    print(await prov.get_all_stats_from_teams("Chelsea", "Burnley"))

    # print(prov.get_api_call_from_today("Newcastle", "Tottenham"))
    
if __name__ == '__main__':
    asyncio.run(main())
    