#!/usr/bin/python3
"""
This script is here to insert matches in the DB
"""
from provider import Provider
import os
from dotenv import load_dotenv

load_dotenv()

prov = Provider()

response = prov.get_matches_in_interval("2016-01-01", "2020-12-31", 148) # Specify a league_id if you want to load a certain league. Careful with a 500 error from the API

#response
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
    
    if len(stats)>0 and len(hometeam_score)>0 and len(awayteam_score)>0:
        if (prov.save_match_with_stats(id, date, time, league_id, league_name, hometeam_name, awayteam_name, hometeam_score,awayteam_score, stats)):
            print(f"Row with id {id} inserted.")
        else:
            print("Error with queries")
    