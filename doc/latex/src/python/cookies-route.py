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