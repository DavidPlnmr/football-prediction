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
		
def sort_by_team_name(team):
    """
    This method is useful to sort the teams in the select 
    """
    return team.get("name")