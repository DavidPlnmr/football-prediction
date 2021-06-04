@app.route('/competitions/<int:league_id>')
async def competitions_make_prediction(league_id):
    if league_id in lib.constants.MULTIPLE_LEAGUES.values():    
        try:
            
            competition = Competition(league_id)
            await competition.create_standing()
            cache["history"] = await competition.compute_competition()
            standings = await competition.get_standing()
            missed_some_predictions = competition.missed_some_predictions
            try:
                error_message = request.cookies.get("error")
                return render_template("competitions.html", league_id=league_id, standings=standings, standings_count=len(standings), missed_some_predictions=missed_some_predictions, error=error_message)
            except Exception:
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