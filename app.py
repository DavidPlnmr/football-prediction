from flask import Flask, redirect, url_for, request, render_template

from lib.prediction_class import Prediction
from lib.provider import Provider
import lib.constants

import json
from dateutil.relativedelta import relativedelta
from datetime import datetime
import os

dir = "./log"
log_path = os.path.join(dir, "app.log")
if not os.path.isdir(dir):
    os.mkdir(dir)
if not os.path.isfile(log_path):
    f = open(log_path, "w")
    f.close()

app = Flask(__name__)
prov = Provider()
cache = {}



"""
INDEX ROUTE
"""
@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    #now = datetime.now()
    now = datetime.strptime("2020-01-01", "%Y-%m-%d")
    three_days_before = now - relativedelta(days=lib.constants.DELTA_DAY)
    three_days_after = now + relativedelta(days=lib.constants.DELTA_DAY)

    if "previous_matches" not in cache:
            
        cache["previous_matches"] = get_previous_matches_multiple_leagues(three_days_before.date(), 
                                                                          now.date(), 
                                                                          lib.constants.MULTIPLE_LEAGUES)
        #Check if all the keys in the dict are empty
        if not any(cache["previous_matches"].values()):
            cache["previous_matches"]=[]
            
    if "upcoming_matches" not in cache:
        cache["upcoming_matches"] = get_upcoming_matches_multiple_leagues(now.date(), 
                                                                          three_days_after.date(), 
                                                                          lib.constants.MULTIPLE_LEAGUES)
        #Check if all the keys in the dict are empty
        if not any(cache["upcoming_matches"].values()):
            cache["upcoming_matches"]=[]
    
    return render_template("index.html", 
                           previous_matches=cache["previous_matches"], 
                           upcoming_matches=cache["upcoming_matches"])



"""
HEAD TO HEAD ROUTES
"""
@app.route('/h2h')
def h2h():
    leagues = lib.constants.MULTIPLE_LEAGUES
    if "error" in cache:
        return render_template("h2h.html", leagues=leagues, error=cache["error"])
    else:
        return render_template("h2h.html", leagues=leagues)
    
@app.route('/h2h/<int:league_id>/<int:first_team>')
def h2h_one_team_selected(league_id, first_team):
    first_team=prov.get_teams_with_team_id(first_team)
    
    team_infos={
        "key" : first_team[0]["team_key"],
        "name" : first_team[0]["team_name"],
        "badge" : first_team[0]["team_badge"],
    }
    return render_template("h2h.html", league_id=league_id, teams=cache["teams"], first_team=team_infos)

@app.route('/h2h/<int:league_id>/<int:first_team>/<int:second_team>')
def h2h_two_teams_selected(league_id, first_team, second_team):
    first_team=prov.get_teams_with_team_id(first_team)
    second_team=prov.get_teams_with_team_id(second_team)
    
    first_team_infos={
        "key" : first_team[0]["team_key"],
        "name" : first_team[0]["team_name"],
        "badge" : first_team[0]["team_badge"],
    }
    
    second_team_infos={
        "key" : second_team[0]["team_key"],
        "name" : second_team[0]["team_name"],
        "badge" : second_team[0]["team_badge"],
    }
    
    return render_template("h2h.html", league_id=league_id, first_team=first_team_infos, second_team=second_team_infos)

@app.route('/h2h/teams/select', methods=["POST"])
def h2h_teams_select():
    first_team = request.form["teamIdHome"]
    league_id = request.form["leagueId"]

    if "teamIdAway" in request.form:
        second_team = request.form["teamIdAway"]
        
        return redirect(url_for('h2h_two_teams_selected', league_id=league_id, first_team=first_team, second_team=second_team))
    else:
        return redirect(url_for('h2h_one_team_selected', league_id=league_id, first_team=first_team))
        pass

@app.route('/h2h/<int:league_id>')
def h2h_league_selected(league_id):
    if league_id in lib.constants.MULTIPLE_LEAGUES.values():
        response = prov.get_teams_from_league(league_id)
        teams = []
        
        for team in response:
            team_info = {
                "key" : team["team_key"],
                "name" : team["team_name"],
                "badge" : team["team_badge"]
            }
            teams.append(team_info)
        
        sorted_teams = sorted(teams, key=sort_by_team_name)
        
        cache["teams"] = sorted_teams
        
        return render_template("h2h.html", league_id=league_id, teams=cache["teams"])
    else:
        cache["error"] = "Unknown league."
        return redirect(url_for("h2h"))
        
@app.route('/h2h/league/select', methods=["POST"])
def h2h_league_select():
    league_id = request.form["leagueId"]
    return redirect(url_for('h2h_league_selected', league_id=league_id))

@app.route('/h2h/make', methods=["POST"])
def h2h_make_prediction():
    
    first_team = int(request.form["teamIdHome"])
    second_team = int(request.form["teamIdAway"])
    league_id = int(request.form["leagueId"])
    if first_team != second_team:
        teams_from_league = prov.get_teams_from_league(league_id)
        first_team = prov.get_teams_with_team_id(first_team)
        second_team = prov.get_teams_with_team_id(second_team)
        
        count = 0
        for team in teams_from_league:
            
            if team["team_name"] == first_team[0]["team_name"] or team["team_name"] == second_team[0]["team_name"]:
                count+=1
            
        if count==2:
            # Clear the error in the cache
            if "error" in cache:        
                cache.pop("error")
                
            first_team_infos={
                "key" : first_team[0]["team_key"],
                "name" : first_team[0]["team_name"],
                "badge" : first_team[0]["team_badge"],
            }
            
            second_team_infos={
                "key" : second_team[0]["team_key"],
                "name" : second_team[0]["team_name"],
                "badge" : second_team[0]["team_badge"],
            }
            
            now = datetime.now()
            three_days_before = now - relativedelta(days=lib.constants.DELTA_DAY)
            
            last_predictions = prov.get_one_prediction_per_day_with_specific_teams(first_team_infos["name"], 
                                                                                   second_team_infos["name"])
            predictions = []
            #Reformat the predictions
            if len(last_predictions)>0:
                for prediction in last_predictions:
                    prediction_info = {
                        "Prediction": prediction["prediction"],
                        "Home" : prediction["home_team_name"],
                        "Away" : prediction["away_team_name"],
                        "Creation date" : prediction["creation_date"]
                    }
                    predictions.append(prediction_info)
                    
            last_predictions=predictions
            
            prediction_already_made = prov.get_prediction_with_specific_teams_after_date(first_team_infos["name"], 
                                                                                      second_team_infos["name"], 
                                                                                      three_days_before.date())
            winner=""
            
            #Check if the prediction has been done today
            if len(prediction_already_made) == 0:
                #Try to make the prediction                
                try:
                    pred = Prediction(first_team_infos["name"], second_team_infos["name"])
                    winner = pred.define_winner()
                    pred.save_prediction()
                
                
                except Exception:
                    cache["error"]="Sorry, we had a problem to process your prediction."
                    return redirect(url_for("h2h"))
            else:
                winner = prediction_already_made[0]["prediction"]
            return render_template("h2h.html", 
                                           first_team=first_team_infos, 
                                           second_team=second_team_infos, 
                                           winner=winner,
                                           last_predictions=last_predictions)
        else:
            cache["error"]="Teams not found in this league."
            return redirect(url_for("h2h"))
    else:
        cache["error"]="You cannot pick the same teams to make a prediction."
        return redirect(url_for("h2h"))



"""
COMPETITIONS ROUTE
"""
@app.route('/competitions')
def competitions():   
    return render_template("competitions.html")



"""
USEFUL METHODS
"""
def make_prediction(first_team_name, second_team_name, league_id, league_name, api_match_id, date_of_game):    
    """
    Make a new prediction for the upcoming matches
    """
    
    pred = Prediction(first_team_name, second_team_name)

    pred.save_prediction(league_id, league_name, date_of_game, api_match_id)
    
    game = {
        "Home" : first_team_name,
        "Away" : second_team_name,
        "Prediction winner" : pred.define_winner(),
        "Date": date_of_game,
    }
    return game
    pass

def get_upcoming_matches_predictions(from_date, to_date, league_id):
    """
    Get the upcoming matches
    """
    response = prov.get_predictions_in_interval_from_db(from_date, to_date, league_id)
    next_matches = prov.get_matches_in_interval(from_date, to_date, league_id)
    
    result = []
    
    array_match_ids = []
    for prediction in response:
        array_match_ids.append(prediction["api_match_id"])
        
    
    # For each match of the api
    for match in next_matches:
        
            #If there is no predictions in the db for this interval of time
            if len(response) > 0:

                for prediction in response:
                            
                    if int(prediction["api_match_id"]) == int(match["match_id"]):
                        game = {
                            "Home" : prediction["home_team_name"],
                            "Away" : prediction["away_team_name"],
                            "Prediction winner" : prediction["prediction"],
                            "Date": prediction["date_of_game"],
                        }
                        result.append(game)
                    
                    else:
                        
                        if int(match["match_id"]) not in array_match_ids:

                            result.append(make_prediction(match["match_hometeam_name"], match["match_awayteam_name"], int(match["league_id"]), match["league_name"], int(match["match_id"]), match["match_date"]))
                            array_match_ids.append(int(match["match_id"]))
            else:
                # Make a prediction for this match
                result.append(make_prediction(match["match_hometeam_name"], match["match_awayteam_name"], int(match["league_id"]), match["league_name"], int(match["match_id"]), match["match_date"]))
    
    return result

def get_upcoming_matches_multiple_leagues(from_date, to_date, multiple_leagues_array):
    """
    Get the upcoming matches for multiple leagues give in param
    """
    result = {}
    for key in multiple_leagues_array:
        try:
            result[key] = get_upcoming_matches_predictions(from_date, to_date, multiple_leagues_array[key])            
        except Exception:
            print("Pas de match pour cette ligue")
            pass
        
        pass
    return result
        
def get_previous_matches_multiple_leagues(from_date, to_date, multiple_leagues_array):
    """
    Get the previous matches for multiple leagues give in param
    """
    result = {}
    for key in multiple_leagues_array:
        result[key] = prov.get_previous_matches_predictions(from_date, to_date, multiple_leagues_array[key])            
        pass
    return result

def sort_by_team_name(team):
    """
    This method is useful to sort the teams in the select 
    """
    return team.get("name")
    
app.run(host="127.0.0.1", port=8080, debug=True)   