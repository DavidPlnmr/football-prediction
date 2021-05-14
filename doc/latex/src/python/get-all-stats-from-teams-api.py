def get_all_stats_from_teams_api(self, first_team_name, second_team_name):
        """
        Make a call to the API using getH2H and make a treatment to have the stats for each match of the two different teams
        """
        reqresult = self.api_facade.get_H2H(first_team_name, second_team_name)
        
        result = {}
        stats_matches_two_team = []
        stats_first_team = []
        stats_second_team = []
        
        # We check the last results of the teams aren't empty
        if len(reqresult["firstTeam_lastResults"]) > 0 and len(reqresult["secondTeam_lastResults"]) > 0:
            
            for match in reqresult["firstTeam_VS_secondTeam"]:
                
                api_match_id = match["match_id"]
                reqstatsresult = self.api_facade.get_stats_from_match(api_match_id)
                
                if self.__check_array_is_in_other_array(lib.constants.STATISTICS_TO_GET, reqstatsresult[api_match_id]["statistics"], "type"):
                    self.__insert_stats_in_array_for_api(match, stats_matches_two_team, reqstatsresult[api_match_id]["statistics"], lib.constants.STATISTICS_TO_GET)
                    
            for match in reqresult["firstTeam_lastResults"]:
                
                api_match_id = match["match_id"]
                reqstatsresult = self.api_facade.get_stats_from_match(api_match_id)
                
                if self.__check_array_is_in_other_array(lib.constants.STATISTICS_TO_GET, reqstatsresult[api_match_id]["statistics"], "type"):
                    self.__insert_stats_in_array_for_api(match, stats_first_team, reqstatsresult[api_match_id]["statistics"], lib.constants.STATISTICS_TO_GET)
                
            for match in reqresult["secondTeam_lastResults"]:
                
                api_match_id = match["match_id"]
                reqstatsresult = self.api_facade.get_stats_from_match(api_match_id)
                
                if self.__check_array_is_in_other_array(lib.constants.STATISTICS_TO_GET, reqstatsresult[api_match_id]["statistics"], "type"):
                    self.__insert_stats_in_array_for_api(match, stats_second_team, reqstatsresult[api_match_id]["statistics"], lib.constants.STATISTICS_TO_GET)
                
            result["firstTeam_VS_secondTeam"]=stats_matches_two_team
            result["firstTeam_lastResults"]=stats_first_team
            result["secondTeam_lastResults"]=stats_second_team
                    

            return result
        else:
            logging.error("No results for one of the two teams selected")
            raise Exception("No results for one of the two team selected")
    