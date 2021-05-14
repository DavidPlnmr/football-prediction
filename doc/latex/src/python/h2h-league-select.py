@app.route('/h2h/league/select', methods=["POST"])
def h2h_league_select():
    league_id = request.form["leagueId"]
    return redirect(url_for('h2h_league_selected', league_id=league_id))