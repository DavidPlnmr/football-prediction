#!/usr/bin/python3
import os
import sys

# insert the "football-prediction" directory into the sys.path
sys.path.insert(1, os.path.abspath(".."))

from lib.provider import *

prov = Provider("../log/app.log")
#print(prov.get_all_stats_from_teams_api("Chelsea", "Burnley"))
#print(prov.get_all_stats_from_teams_db("Chelsea", "Burnley"))

print(prov.get_all_stats_from_teams("Chelsea", "Tottenham"))