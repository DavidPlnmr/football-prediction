@app.route('/h2h/make', methods=["POST"])
def h2h_make_prediction():
    first_team = request.form["teamIdHome"]
    second_team = request.form["teamIdAway"]
    league_id = request.form["leagueId"]
    
    if first_team != second_team:
        teams_from_league = prov.get_teams_from_league(league_id)
        first_team = prov.get_teams_with_team_id(first_team)
        second_team = prov.get_teams_with_team_id(second_team)
        
        count = 0
        for team in teams_from_league:
            
            if team["team_name"] == first_team[0]["team_name"] or team["team_name"] == second_team[0]["team_name"]:
                count+=1
            
        if count==2:
            # Clear the error in the cache
            if "error" in cache:        
                cache.pop("error")
                
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
            
            now = datetime.now()
            three_days_before = now - relativedelta(days=lib.constants.DELTA_DAY)
            
            last_predictions = prov.get_one_prediction_per_day_with_specific_teams(first_team_infos["name"], 
                                                                                   second_team_infos["name"])
            predictions = []
            #Reformat the predictions
            if len(last_predictions)>0:
                for prediction in last_predictions:
                    prediction_info = {
                        "Prediction": prediction["prediction"],
                        "Home" : prediction["home_team_name"],
                        "Away" : prediction["away_team_name"],
                        "Creation date" : prediction["creation_date"]
                    }
                    predictions.append(prediction_info)
                    
            last_predictions=predictions
            
            prediction_already_made = prov.get_prediction_with_specific_teams_after_date(first_team_infos["name"], 
                                                                                      second_team_infos["name"], 
                                                                                      three_days_before.date())
            winner=""
            
            #Check if the prediction has been done today
            if len(prediction_already_made) == 0:
                #Try to make the prediction                
                try:
                    pred = Prediction(first_team_infos["name"], second_team_infos["name"])
                    winner = pred.define_winner()
                    pred.save_prediction()
                
                
                except Exception:
                    cache["error"]="Sorry, we had a problem to process your prediction."
                    return redirect(url_for("h2h"))
            else:
                winner = prediction_already_made[0]["prediction"]
            return render_template("h2h.html", 
                                           first_team=first_team_infos, 
                                           second_team=second_team_infos, 
                                           winner=winner,
                                           last_predictions=last_predictions)
        else:
            cache["error"]="Teams not found in this league."
            return redirect(url_for("h2h"))
    else:
        cache["error"]="You cannot pick the same teams to make a prediction."
        return redirect(url_for("h2h"))