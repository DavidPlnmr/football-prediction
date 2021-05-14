@app.route('/h2h')
def h2h():
    leagues = lib.constants.MULTIPLE_LEAGUES
    if "error" in cache:
        return render_template("h2h.html", leagues=leagues, error=cache["error"])
    else:
        return render_template("h2h.html", leagues=leagues)