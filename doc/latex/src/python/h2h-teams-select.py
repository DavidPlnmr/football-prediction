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