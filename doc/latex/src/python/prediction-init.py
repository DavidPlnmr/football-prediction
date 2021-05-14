def __init__(self, home_team, away_team, from_date="", to_date=""):
        self.home_team_result = TeamResult(home_team)
        self.away_team_result = TeamResult(away_team)
        self.winner=""
        

        self.provider = Provider("../log/app.log")
        
        
        try:
            #Change this line to API when tests are finished
            #self.results = self.provider.get_all_stats_from_teams_api(home_team, away_team)
            # This line down below is here to test the success of the prediction. Making a prediction from a past game
            self.results = self.provider.get_all_stats_from_teams_db(home_team, away_team, from_date, to_date)
            
            self.home_team_result.heat_of_moment = self.__compute_heat_moment(home_team, self.results["firstTeam_lastResults"])
            self.away_team_result.heat_of_moment = self.__compute_heat_moment(away_team, self.results["secondTeam_lastResults"])

            self.__insert_data_team_result(self.home_team_result, "firstTeam_lastResults")
            self.__insert_data_team_result(self.away_team_result, "secondTeam_lastResults")
            
            self.__insert_data_team_result(self.home_team_result, "firstTeam_VS_secondTeam")
            self.__insert_data_team_result(self.away_team_result, "firstTeam_VS_secondTeam")
        except Exception:
            #At the moment we show a print but later WE MUST RAISE AN EXCEPTION OR AN ERROR
            
            raise Exception("Prediction unmakeable. Not enought stats.")