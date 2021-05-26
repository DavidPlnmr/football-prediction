def get_standing(self):
	"""
	Get the standing with the self.__history var. It will return the standing of the competition sorted by points
	"""
	if not self.standing_computed:   
		self.__history = self.compute_competition() 
		for team in self.standings:
			team_name = team["Name"]
			for i in range(len(self.__history)):
				game = self.__history[i]
				if team_name == game["Home"] or team_name == game["Away"]:
					team["Games"] += 1
					if team_name == game["Prediction"]:
						team["Wins"] += 1
						team["Points"] += lib.constants.POINTS_FOR_A_WIN
					elif game["Prediction"] == "Draw":
						team["Draws"] += 1
						team["Points"] += lib.constants.POINTS_FOR_A_DRAW
					else:
						team["Losses"] += 1
						team["Points"] += lib.constants.POINTS_FOR_A_LOSE
		self.standings = sorted(self.standings, key=sort_by_team_points, reverse=True)
	
	return self.standings
	
def sort_by_team_points(team):
    return team.get("Points")