def get_upcoming_matches_predictions(from_date, to_date, league_id):
    """
    Get the upcoming matches
    """
    response = prov.get_predictions_in_interval_from_db(from_date, to_date, league_id)
    next_matches = prov.get_matches_in_interval(from_date, to_date, league_id)
    
    result = []
    
    array_match_ids = []
    for prediction in response:
        array_match_ids.append(prediction["api_match_id"])
        
    
    is_response_empty = len(response) > 0    
    #If there is no predictions in the db for this interval of time
    if is_response_empty:
        # For each match of the api
        for match in next_matches:
            for prediction in response:
                        
                if int(prediction["api_match_id"]) == int(match["match_id"]):
                    game = {
                        "Home" : prediction["home_team_name"],
                        "Away" : prediction["away_team_name"],
                        "Prediction winner" : prediction["prediction"],
                        "Date": prediction["date_of_game"],
                    }
                    result.append(game)
                
                else:
                    
                    if int(match["match_id"]) not in array_match_ids:

                        result.append(make_prediction(match["match_hometeam_name"], match["match_awayteam_name"], int(match["league_id"]), match["league_name"], int(match["match_id"]), match["match_date"]))
                        array_match_ids.append(int(match["match_id"]))
    else:
        # For each match of the api
        for match in next_matches:  
            # Make a prediction for this match
            result.append(make_prediction(match["match_hometeam_name"], match["match_awayteam_name"], int(match["league_id"]), match["league_name"], int(match["match_id"]), match["match_date"]))
    
    return result