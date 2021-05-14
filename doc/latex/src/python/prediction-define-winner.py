def define_winner(self):
        """
        Returns the winner of the prediction by computing the offensive score, defensive score and the heat of moment
        """
        #This check is here to not compute everything if we already have the name of the winner
        if self.winner== "":
            if self.home_team_result.games_count > 0 and self.away_team_result.games_count > 0:    
                # Adding the off score
                home_team_final_score = self.__compute_off_score(self.home_team_result)
                away_team_final_score = self.__compute_off_score(self.away_team_result)
                
                #Adding the def score
                home_team_final_score += self.__compute_def_score(self.home_team_result)
                away_team_final_score += self.__compute_def_score(self.away_team_result)
                
                #Adding the heat of the moment score
                home_team_final_score += self.__compute_heat_moment_score(self.home_team_result)
                away_team_final_score += self.__compute_heat_moment_score(self.away_team_result)
                
                if home_team_final_score > away_team_final_score * lib.constants.DELTA_TO_DETERMINE_DRAW:
                    self.winner = self.get_home_team_name()    
                elif away_team_final_score > home_team_final_score * lib.constants.DELTA_TO_DETERMINE_DRAW:
                    self.winner = self.get_away_team_name()    
                else:
                    self.winner = "Draw"
                
        return self.winner