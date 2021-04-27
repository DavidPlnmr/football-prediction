#!/usr/bin/python3
from lib.provider import *

prov = Provider("../lib/log/app.log")
print(prov.get_all_stats_from_teams_api("Chelsea", "Burnley"))
print(prov.get_all_stats_from_teams_db("Chelsea", "Burnley"))
prov.save_prediction("Home", "Manchester United", "Southampton", 2000, 1090, 2090, 1000)