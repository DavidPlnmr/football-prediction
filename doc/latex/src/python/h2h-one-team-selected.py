@app.route('/h2h/<int:league_id>/<int:first_team>')
def h2h_one_team_selected(league_id, first_team):
    first_team=prov.get_teams_with_team_id(first_team)
    
    team_infos={
        "key" : first_team[0]["team_key"],
        "name" : first_team[0]["team_name"],
        "badge" : first_team[0]["team_badge"],
    }
    return render_template("h2h.html", league_id=league_id, teams=cache["teams"], first_team=team_infos)