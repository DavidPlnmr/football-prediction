#!/usr/bin/python3
"""
The purpose of this script is to make many predictions and to see how precise the algorithm is
To use it : ./test_many_prediction.py > my_file.csv
It will write your data in the csv in this order :
Correct predictions count; Games count; Percent of the delta
"""
import sys
import os

# insert the "football-prediction" directory into the sys.path
sys.path.insert(1, os.path.abspath(".."))

from lib.prediction_class import Prediction
from lib.provider import Provider
from datetime import date
import lib.constants
from dateutil.relativedelta import relativedelta # $ pip install python-dateutil

prov = Provider("../lib/log/app.log")

response = prov.get_matches_from_to_db("2019-08-09", "2020-07-26")

for index in range(9):
    games_count = 0
    good_predictions_count = 0
    
    for match in response:
        try:
            pred = Prediction(match["home_team_name"], match["away_team_name"], str(match["date"] + relativedelta(years=-1)), str(match["date"]))
            prediction_winner = pred.define_winner()
            result = int(match["home_team_score"]) - int(match["away_team_score"])
        
            real_winner = ""
            
            if result == 0:
                real_winner = 'Draw' # D for Draw
            elif result > 0:
                real_winner = match["home_team_name"]
            else:
                real_winner = match["away_team_name"]

            if prediction_winner == real_winner:
                good_predictions_count +=1

            games_count +=1
        except Exception:
            #print("Problem with Prediction")
            pass
        
    
    print(f"{good_predictions_count};{games_count};{(lib.constants.DELTA_TO_DETERMINE_DRAW-1)*100}")
    
    lib.constants.DELTA_TO_DETERMINE_DRAW += 0.01
        
        
        
        
        
        


# TO DO : Get the games from 2019-20 Season and make prediction for each of these matches and compare with the real result

# Take games from DB using get all matches from teams db