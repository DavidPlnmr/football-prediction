#!/usr/bin/python3
from provider import Provider

prov = Provider()
print(prov.get_all_stats_from_teams_api("Chelsea", "Burnley"))
print(prov.get_all_stats_from_teams_db("Chelsea", "Burnley"))
prov.save_prediction("Home", "Manchester United", "Southampton", 2000, 1090, 2090, 1000)