def get_all_stats_from_teams_db(self, first_team_name, second_team_name, from_date="", to_date=""):
        """
        Get all the matches between the two teams in params with the stats of each matches
        """
        reqmatch = self.db_manager.get_matches_with_specific_teams(first_team_name, second_team_name, from_date, to_date)
        reqstats = self.db_manager.get_stats_of_matches_with_specific_teams(first_team_name, second_team_name, from_date, to_date)
        
        
        result = {}
        stats_matches_two_team = []
        stats_first_team = []
        stats_second_team = []
        
        # We check if the requests aren't empty
        
        if len(reqmatch) > 0 and len(reqstats) > 0:
            for match in reqmatch:
                #Check for the game with the two teams
                if (match["home_team_name"] == first_team_name or match["away_team_name"] == first_team_name) and (match["home_team_name"] == second_team_name or match["away_team_name"] == second_team_name):
                    if self.__check_array_is_contained_with_specific_id(lib.constants.STATISTICS_TO_GET, reqstats, "type", match["id"]):
                        self.__insert_stats_in_array_for_db(match, stats_matches_two_team, reqstats, lib.constants.STATISTICS_TO_GET)
                        
                elif (match["home_team_name"] == first_team_name or match["away_team_name"] == first_team_name):
                    if self.__check_array_is_contained_with_specific_id(lib.constants.STATISTICS_TO_GET, reqstats, "type", match["id"]):
                        self.__insert_stats_in_array_for_db(match, stats_first_team, reqstats, lib.constants.STATISTICS_TO_GET)
                    
                elif (match["home_team_name"] == second_team_name or match["away_team_name"] == second_team_name):    
                    if self.__check_array_is_contained_with_specific_id(lib.constants.STATISTICS_TO_GET, reqstats, "type", match["id"]):
                        self.__insert_stats_in_array_for_db(match, stats_second_team, reqstats, lib.constants.STATISTICS_TO_GET)
                
            if len(stats_first_team)>0 and len(stats_second_team)>0 :
        
                result["firstTeam_VS_secondTeam"]=stats_matches_two_team
                result["firstTeam_lastResults"]=stats_first_team
                result["secondTeam_lastResults"]=stats_second_team
            else:
                logging.error("No results for one of the two teams selected")
                return None
            
            return result
        else:
            logging.error("No results for one of the two teams selected")
            raise Exception("No results for one of the two team selected")