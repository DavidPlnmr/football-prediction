def get_upcoming_matches_multiple_leagues(from_date, to_date, multiple_leagues_array):
    """
    Get the upcoming matches for multiple leagues give in param
    """
    result = {}
    for key in multiple_leagues_array:
        try:
            result[key] = get_upcoming_matches_predictions(from_date, to_date, multiple_leagues_array[key])            
        except Exception:
            print("Pas de match pour cette ligue")
            pass
        
        pass
    return result 