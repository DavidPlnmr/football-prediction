@app.route('/competitions/<int:league_id>/<int:team_id>')
async def competitions_history(league_id, team_id):
    history_of_selected_team = []
    teams_from_league = await prov.get_teams_from_league(league_id)
    team_info = await prov.get_teams_with_team_id(team_id)
    team_name = team_info[0]["team_name"]
    team_badge = team_info[0]["team_badge"]
    
    team_is_in_league = False
    # Check that both of the teams are in the same league
    for team in teams_from_league:
        if team["team_key"] == team_info[0]["team_key"]:
            team_is_in_league = True
    
    if team_is_in_league:
        for match in cache["history"]:
            if match["Home Name"] == team_name or match["Away Name"] == team_name :
                history_of_selected_team.append(match)
        
        return render_template("competitions.html", team_badge=team_badge, team_name=team_name, league_id=league_id, history=history_of_selected_team, history_count=len(history_of_selected_team))
    else:
        response = make_response(redirect(url_for("competitions_make_prediction", league_id=league_id)))
        response.set_cookie("error", "This team is not in the league.", max_age=1)
        return response