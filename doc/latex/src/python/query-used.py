def get_stats_of_matches_with_specific_teams(self, first_team_name, second_team_name, from_date="", to_date=""):
        """
        This method search all the games of each of the teams and returns the statistics of each match [before the date specified in param if it specified]
        """
        query = f"""SELECT s.`type`, s.home, s.away, s.id_match
                                FROM footballPrediction.statistic s 
                                INNER JOIN footballPrediction.`match` m ON s.id_match  = m.id 
                                WHERE m.home_team_name="{first_team_name}" 
                                OR m.away_team_name="{first_team_name}" 
                                OR m.home_team_name="{second_team_name}" 
                                OR m.away_team_name="{second_team_name}" """
        
        if len(from_date)>0 and len(to_date)>0:
            query += f'AND m.date > "{from_date}" AND m.date < "{to_date}"'
            
        query += ";"
        
        return self.__query(query)