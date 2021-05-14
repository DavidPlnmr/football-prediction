def get_previous_matches_multiple_leagues(from_date, to_date, multiple_leagues_array):
    """
    Get the previous matches for multiple leagues give in param
    """
    result = {}
    for key in multiple_leagues_array:
        result[key] = prov.get_previous_matches_predictions(from_date, to_date, multiple_leagues_array[key])            
        pass
    return result