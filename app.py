from flask import Flask, redirect, url_for, request, render_template

from lib.prediction_class import Prediction
from lib.provider import Provider
import lib.constants

from dateutil.relativedelta import relativedelta
from datetime import datetime

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
    now = datetime.now()
    three_days_before = now - relativedelta(days=lib.constants.DELTA_DAY)
    three_days_after = now + relativedelta(days=lib.constants.DELTA_DAY)

    if "previous_matches" not in cache:
            
        cache["previous_matches"] = get_previous_matches_multiple_leagues(three_days_before.date(), now.date(), lib.constants.MULTIPLE_LEAGUES)
        #Check if all the keys in the dict are empty
        if not any(cache["previous_matches"].values()):
            cache["previous_matches"]=[]
            
    if "upcoming_matches" not in cache:
        cache["upcoming_matches"] = get_upcoming_matches_multiple_leagues(now.date(), three_days_after.date(), lib.constants.MULTIPLE_LEAGUES)
        #Check if all the keys in the dict are empty
        if not any(cache["upcoming_matches"].values()):
            cache["upcoming_matches"]=[]
    
    return render_template("index.html", app_name="Football Prediction", previous_matches=cache["previous_matches"], upcoming_matches=cache["upcoming_matches"])

"""
HEAD TO HEAD ROUTE
"""
@app.route('/h2h')
def h2h():   
    leagues = lib.constants.MULTIPLE_LEAGUES
    teams = {}
    
    if "teams" not in cache:
        for league_name in leagues:    
            sorted_teams = sorted(prov.get_teams_from_league(leagues[league_name]), key=sort_by_team_name)
            teams[league_name] = sorted_teams
            
        cache["teams"] = teams
    return render_template("h2h.html", app_name="Football Prediction", all_teams=cache["teams"])

@app.route('/h2h/<int:first_team_id>')
def h2h_one_team_selected(first_team_id):
    first_team=prov.get_teams_with_team_id(first_team_id)
    
    team_infos={
        "team_key" : first_team[0]["team_key"],
        "team_name" : first_team[0]["team_name"],
        "team_badge" : first_team[0]["team_badge"],
    }
    return render_template("h2h.html", app_name="Football Prediction", all_teams=cache["teams"], first_team=team_infos)

@app.route('/h2h/<int:first_team_id>/<int:second_team_id>')
def h2h_two_teams_selected(first_team_id, second_team_id):
    first_team=prov.get_teams_with_team_id(first_team_id)
    second_team=prov.get_teams_with_team_id(second_team_id)
    
    first_team_infos={
        "team_key" : first_team[0]["team_key"],
        "team_name" : first_team[0]["team_name"],
        "team_badge" : first_team[0]["team_badge"],
    }
    
    second_team_infos={
        "team_key" : second_team[0]["team_key"],
        "team_name" : second_team[0]["team_name"],
        "team_badge" : second_team[0]["team_badge"],
    }
    
    return render_template("h2h.html", app_name="Football Prediction", all_teams=cache["teams"], first_team=first_team_infos, second_team=second_team_infos)


@app.route('/h2h/select', methods=["POST"])
def h2h_select():
    first_team_id = request.form["teamIdHome"]
    if "teamIdAway" in request.form:
        second_team_id = request.form["teamIdAway"]
        return redirect(url_for('h2h_two_teams_selected', first_team_id=first_team_id, second_team_id=second_team_id))
    else:
        return redirect(url_for('h2h_one_team_selected', first_team_id=first_team_id))

"""
COMPETITIONS ROUTE
"""
@app.route('/competitions')
def competitions():   
    return render_template("competitions.html", app_name="Football Prediction")


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
                            "Date": prediction["date_of_game"].strftime("%d %B %Y"),
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
    return team.get("team_name")
    

app.run(host="127.0.0.1", port=8080, debug=True)
            