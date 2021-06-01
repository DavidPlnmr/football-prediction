#!/usr/bin/python3
import os
import sys
import time

# insert the "football-prediction" directory into the sys.path
sys.path.insert(1, os.path.abspath(".."))

from lib.provider_class import *

prov = Provider("../log/app.log")

async def main():
    
    start = time.perf_counter() 
    print(await prov.get_all_stats_from_teams("Manchester City", "Burnley"))
    #print(await prov.get_all_stats_from_teams_api("Manchester Utd", "Newcastle"))
    #print(prov.get_all_stats_from_teams_db("Chelsea", "Burnley"))
    # print(prov.get_api_call_from_today("Newcastle", "Tottenham"))
    end = time.perf_counter()
    print(f"Time elapsed : {end-start} second(s)")
    
    
if __name__ == '__main__':
    asyncio.run(main())
    