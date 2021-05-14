@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    now = datetime.now()
    three_days_before = now - relativedelta(days=lib.constants.DELTA_DAY)
    three_days_after = now + relativedelta(days=lib.constants.DELTA_DAY)

    if "previous_matches" not in cache:
            
        cache["previous_matches"] = get_previous_matches_multiple_leagues(three_days_before.date(), 
                                                                          now.date(), 
                                                                          lib.constants.MULTIPLE_LEAGUES)
        #Check if all the keys in the dict are empty
        if not any(cache["previous_matches"].values()):
            cache["previous_matches"]=[]
            
    if "upcoming_matches" not in cache:
        cache["upcoming_matches"] = get_upcoming_matches_multiple_leagues(now.date(), 
                                                                          three_days_after.date(), 
                                                                          lib.constants.MULTIPLE_LEAGUES)
        #Check if all the keys in the dict are empty
        if not any(cache["upcoming_matches"].values()):
            cache["upcoming_matches"]=[]
    
    return render_template("index.html", 
                           previous_matches=cache["previous_matches"], 
                           upcoming_matches=cache["upcoming_matches"])