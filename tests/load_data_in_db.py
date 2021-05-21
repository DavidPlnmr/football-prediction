#!/usr/bin/python3
"""
This script is here to insert matches in the DB
"""
import os
import sys
# insert the "football-prediction" directory into the sys.path
sys.path.insert(1, os.path.abspath(".."))
from lib.provider import Provider
import os
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta

load_dotenv()

prov = Provider("../log/app.log")

now = datetime.now()

three_months_before = now - relativedelta(months=9)

now = now.strftime("%Y-%m-%d")
three_months_before = three_months_before.strftime("%Y-%m-%d")

response = prov.get_matches_in_interval(three_months_before, now, 148) # Specify a league_id if you want to load a certain league. Careful with a 500 error from the API

for match in response:
    id = int(match["match_id"])
    date = match["match_date"]
    time = match["match_time"]
    league_id = int(match["league_id"])
    league_name = match["league_name"]
    hometeam_name = match["match_hometeam_name"]
    awayteam_name = match["match_awayteam_name"]
    hometeam_score = match["match_hometeam_score"]
    awayteam_score = match["match_awayteam_score"]
    stats = match["statistics"]
    
    formatted_stats = {}
    for i in range(len(stats)-1):
        formatted_stats[stats[i]["type"]] = {
            "home" : stats[i]["home"],
            "away" : stats[i]["away"]
        }
    
    if len(formatted_stats)>0 and len(hometeam_score)>0 and len(awayteam_score)>0:
        if (prov.save_match_with_stats(id, date, time, league_id, league_name, hometeam_name, awayteam_name, hometeam_score,awayteam_score, formatted_stats)):
            print(f"Row with id {id} inserted.")
        else:
            print("Error with queries")
    