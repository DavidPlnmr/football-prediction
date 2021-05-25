"""
Class to make a prediction on a whole competition
"""
def __init__(self, league_id, log_path=""):
	self.standings =  []
	prov = Provider(log_path)
	teams = prov.get_teams_from_league(int(league_id))
	self.history = []
	self.standing_computed = False
	
	# for team in teams:
	for i in range(len(teams)):
		# We must put this line because there is a bug with the API 
		if teams[i]["team_name"] == "Manchester United":
			teams[i]["team_name"] = "Manchester Utd"
		self.standings.append({
			"Name" : teams[i]["team_name"],
			"Badge" : teams[i]["team_badge"],
			"Games" : 0,
			"Wins" : 0,
			"Draws" : 0,
			"Losses" : 0,
			"Points" : 0
		})
	