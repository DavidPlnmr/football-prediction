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