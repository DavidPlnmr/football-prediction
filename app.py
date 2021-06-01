from asyncio.streams import start_server
from flask import Flask, json, redirect, url_for, request, render_template, jsonify
from flask.helpers import make_response

from lib.prediction_class import Prediction
from lib.provider_class import Provider
from lib.competition_class import Competition
import lib.constants

from dateutil.relativedelta import relativedelta
from datetime import datetime
import os
import asyncio

import logging

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
logging.basicConfig(filename="./log/app.log", filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

"""
INDEX ROUTE
"""
@app.route('/')
@app.route('/index')
@app.route('/home')
async def index():
    """
    Home route
    """
    now = datetime(2021, 5, 15)
    three_days_before = now - relativedelta(days=lib.constants.DELTA_DAY)
    three_days_after = now + relativedelta(days=lib.constants.DELTA_DAY)
    
    if "previous_matches" not in cache:
        cache["previous_matches"] = await get_previous_matches_multiple_leagues(three_days_before.date(), 
                                                                          now.date(), 
                                                                          lib.constants.MULTIPLE_LEAGUES)
        #Check if all the keys in the dict are empty
        if not any(cache["previous_matches"].values()):
            cache["previous_matches"]=[]
            
    if "upcoming_matches" not in cache:
        cache["upcoming_matches"] = await get_upcoming_matches_multiple_leagues(now.date(), 
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
    """
    Route for the functionnality Head To Head
    """
    leagues = lib.constants.MULTIPLE_LEAGUES
    try:
        error_message = request.cookies.get("error")
        return render_template("h2h.html", leagues=leagues, error=error_message)
    except Exception:
        return render_template("h2h.html", leagues=leagues)
    
@app.route('/h2h/<int:league_id>/<int:first_team>')
async def h2h_one_team_selected(league_id, first_team):
    """
    Route where the user has already selected one team
    """
    try:
        first_team= await prov.get_teams_with_team_id(first_team)
    
        team_infos={
            "key" : first_team[0]["team_key"],
            "name" : first_team[0]["team_name"],
            "badge" : first_team[0]["team_badge"],
        }
        return render_template("h2h.html", league_id=league_id, teams=cache["teams"], first_team=team_infos)
    except Exception:
        response = make_response(redirect(url_for("h2h")))
        response.set_cookie("error", "We encountered a problem while data of the team you selected.", max_age=1)
        return response
    
@app.route('/h2h/<int:league_id>/<int:first_team>/<int:second_team>')
async def h2h_two_teams_selected(league_id, first_team, second_team):
    """
    Route where the user has already selected two teams
    """
    try:
        first_team = await prov.get_teams_with_team_id(first_team)
        second_team = await prov.get_teams_with_team_id(second_team)
        
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

    except Exception:
        response = make_response(redirect(url_for("h2h")))
        response.set_cookie("error", "We encountered a problem while data of the team you selected.", max_age=1)
        return response
    
@app.route('/h2h/teams/select', methods=["POST"])
def h2h_teams_select():
    """
    Action of the form to select the teams.
    """
    first_team = request.form["teamIdHome"]
    league_id = request.form["leagueId"]

    if "teamIdAway" in request.form:
        second_team = request.form["teamIdAway"]
        
        return redirect(url_for('h2h_two_teams_selected', league_id=league_id, first_team=first_team, second_team=second_team))
    else:
        return redirect(url_for('h2h_one_team_selected', league_id=league_id, first_team=first_team))

@app.route('/h2h/<int:league_id>')
async def h2h_league_selected(league_id):
    """
    Route where the user has already selected the league
    """
    if league_id in lib.constants.MULTIPLE_LEAGUES.values():
        try:
            response = await prov.get_teams_from_league(league_id)
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
        except Exception:
            response = make_response(redirect(url_for("h2h")))
            response.set_cookie("error", "We encountered a problem while loading the teams from the league.", max_age=1)
            return response
        
    else:
        response = make_response(redirect(url_for("h2h")))
        response.set_cookie("error", "Unknown league.", max_age=1)
        return response
        
@app.route('/h2h/league/select', methods=["POST"])
def h2h_league_select():
    """
    Action of the form to select the league
    """
    league_id = request.form["leagueId"]
    return redirect(url_for('h2h_league_selected', league_id=league_id))

@app.route('/h2h/make', methods=["POST"])
async def h2h_make_prediction():
    """
    Route to create a prediction
    """
    first_team = request.form["teamIdHome"]
    second_team = request.form["teamIdAway"]
    league_id = request.form["leagueId"]
    
    # We don't wanna make a prediction if the teams are the same
    if first_team != second_team:
        teams_from_league = await prov.get_teams_from_league(league_id)
        first_team = await prov.get_teams_with_team_id(first_team)
        second_team = await prov.get_teams_with_team_id(second_team)
        
        count = 0
        for team in teams_from_league:
            
            if team["team_name"] == first_team[0]["team_name"] or team["team_name"] == second_team[0]["team_name"]:
                count+=1
        
        # Obviously it's an head to head game so we need 2 teams and we check if they are in the league selected
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
                    await pred.call_data()
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
            # Error message because the two teams selected are not in the league selected.
            response = make_response(redirect(url_for("h2h")))
            response.set_cookie("error", "Teams not found in this league.", max_age=1)
            return response
    else:
        # Error message because the user selected the same teams
        response = make_response(redirect(url_for("h2h")))
        response.set_cookie("error", "You cannot pick the same teams to make a prediction.", max_age=1)
        return response



"""
COMPETITIONS ROUTE
"""
@app.route('/competitions')
def competitions():
    """
    Competition first route
    """
    if "history" in cache:
        cache.pop("history")
        
    leagues = lib.constants.MULTIPLE_LEAGUES
    try:
        error_message = request.cookies.get("error")
        return render_template("competitions.html", leagues=leagues, error=error_message)
    except Exception:
        return render_template("competitions.html", leagues=leagues)

@app.route('/competitions/select', methods=["POST"])
def competitions_select():
    """
    Action of the form to select the league
    """
    league_id = request.form["leagueId"]
    return redirect(url_for("competitions_make_prediction", league_id=league_id))

@app.route('/competitions/<int:league_id>')
async def competitions_make_prediction(league_id):
    if league_id in lib.constants.MULTIPLE_LEAGUES.values():    
        try:
            
            competition = Competition(league_id)
            await competition.create()
            cache["history"] = await competition.compute_competition()
            standings = await competition.get_standing()
            missed_some_predictions = competition.missed_some_predictions
            return render_template("competitions.html", league_id=league_id, standings=standings, standings_count=len(standings), missed_some_predictions=missed_some_predictions)
        except Exception as e:
            print(e)
            logging.error(e)
            response = make_response(redirect(url_for("competitions")))
            response.set_cookie("error", "We couldn't process this competition. Please, retry later.", max_age=1)
            return response
    else:
        response = make_response(redirect(url_for("competitions")))
        response.set_cookie("error", "Unknown league.", max_age=1)
        return response
    
@app.route('/competitions/<int:league_id>/<int:team_id>')
async def competitions_history(league_id, team_id):
    history_of_selected_team = []
    team_info = await prov.get_teams_with_team_id(team_id)
    team_name = team_info[0]["team_name"]
    team_badge = team_info[0]["team_badge"]
    for match in cache["history"]:
        if match["Home Name"] == team_name or match["Away Name"] == team_name :
            history_of_selected_team.append(match)
    
    return render_template("competitions.html", team_badge=team_badge, team_name=team_name, league_id=league_id, history=history_of_selected_team, history_count=len(history_of_selected_team))

"""
USEFUL METHODS
"""
async def make_prediction(first_team_name, second_team_name, league_id, league_name, api_match_id, date_of_game):    
    """
    Make a new prediction for the upcoming matches
    """
    
    pred = Prediction(first_team_name, second_team_name)

    await pred.call_data()
    pred.save_prediction(league_id, league_name, date_of_game, api_match_id)
    
    game = {
        "Home" : first_team_name,
        "Away" : second_team_name,
        "Prediction winner" : pred.define_winner(),
        "Date": date_of_game,
    }
    return game

async def get_upcoming_matches_predictions(from_date, to_date, league_id, key, out_dict):
    """
    Get the upcoming matches
    """

    predictions = prov.get_predictions_in_interval_from_db(from_date, to_date, league_id)
    next_matches=""
    
    try:
        next_matches = await prov.get_matches_in_interval(from_date, to_date, league_id)
    except Exception as e:
        print(e)
    
    result = []
    
    array_match_ids = []
    for prediction in predictions:
        array_match_ids.append(prediction["api_match_id"])
        
    
    is_response_not_empty = len(predictions) > 0    
    #If there is no predictions in the db for this interval of time
    if is_response_not_empty:
        # For each match of the api
        for match in next_matches:
            
            for prediction in predictions:
                        
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
                        result.append(await make_prediction(match["match_hometeam_name"], match["match_awayteam_name"], int(match["league_id"]), match["league_name"], int(match["match_id"]), match["match_date"]))
                        array_match_ids.append(int(match["match_id"]))
    else:
        # For each match of the api
        for match in next_matches:  
            # Make a prediction for this match
            result.append(await make_prediction(match["match_hometeam_name"], match["match_awayteam_name"], int(match["league_id"]), match["league_name"], int(match["match_id"]), match["match_date"]))
    
    out_dict[key] = result
    return result

async def get_upcoming_matches_multiple_leagues(from_date, to_date, multiple_leagues_array):
    """
    Get the upcoming matches for multiple leagues give in param
    """
    result = {}
    await asyncio.wait([get_upcoming_matches_predictions(from_date, to_date, multiple_leagues_array[key], key, result) for key in multiple_leagues_array])
    return result

async def get_previous_matches_multiple_leagues(from_date, to_date, multiple_leagues_array):
    """
    Get the previous matches for multiple leagues give in param
    """
    result = {}
    await asyncio.wait([prov.get_previous_matches_predictions(from_date, to_date, multiple_leagues_array[key], key, result) for key in multiple_leagues_array])
    return result

def sort_by_team_name(team):
    """
    This method is useful to sort the teams in the select 
    """
    return team.get("name")
    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)   