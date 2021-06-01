async def get_all_stats_from_teams(self, first_team_name, second_team_name):
	"""
	This method try to get games from the two teams in the DB. If there is no data in the DB, it will get data from the API and then save it in the DB.
	"""
	response = ""
	
	try:
		now = datetime.now().date()
		three_months_before = now - relativedelta(months=lib.constants.DELTA_MONTHS_TO_GET_GAMES)
		now = now.strftime("%Y-%m-%d")
		three_months_before = three_months_before.strftime("%Y-%m-%d")
		if len(self.get_api_call_from_today(first_team_name,second_team_name))>0:
			# Try catch cause the method below can throw an exception if we haven't enought stats
			try:
				response = self.get_all_stats_from_teams_db(first_team_name, second_team_name, three_months_before, now)
			except Exception:
				raise Exception("Data unavailable for this prediction")
				
		else:
			raise APICallNotFound("No API call made today")
		# We must make an await because the method is an async else it will create an error
		await asyncio.sleep(0)
		
	except APICallNotFound:
		response = await self.get_all_stats_from_teams_api(first_team_name, second_team_name)
		self.save_api_call(first_team_name, second_team_name)
		for result in response:
			for match in response[result]:
				try:
					self.save_match_with_stats(match["api_match_id"], 
											match["date"],
											match["time"],
											match["league_id"],
											match["league_name"],
											match["home_team"],
											match["away_team"],
											match["home_team_score"], 
											match["away_team_score"], 
											match["stats"])
				except Exception:
					logging.warning("Could not save the match")

	return response