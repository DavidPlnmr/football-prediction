def insert_match_with_stats(self, match_id, match_date, match_time, league_id, league_name, home_team_name, away_team_name, home_team_score, away_team_score, stats_array):
        """
        Insert a match with its stats in the database with the parameters given.
        """
        #We try to make our queries
        try:
            self.__cursor.execute(f"""INSERT INTO `match` (
                            `id`, 
                            `date`, 
                            `time`, 
                            `league_id`, 
                            `league_name`, 
                            `home_team_name`,
                            `away_team_name`,
                            `home_team_score`,
                            `away_team_score`)
                            VALUES ( {match_id},  STR_TO_DATE("{match_date}", "%Y-%m-%d"), "{match_time}", {league_id}, "{league_name}", "{home_team_name}", "{away_team_name}", {home_team_score}, {away_team_score} );""")
        
            for stat in stats_array:
                type = stat["type"]
                home = stat["home"]
                away = stat["away"]
                self.__cursor.execute(f"""INSERT INTO `statistic` (
                                    `type`,
                                    `home`,
                                    `away`,
                                    `id_match`)
                                    VALUES ( "{type}", "{home}", "{away}", {match_id});""")
                
            self.__db.commit() # Save the changes
            logging.info(f"Inserted match in the DB with params : {match_id},  {match_date}, {match_time}, {league_id}, {league_name}, {home_team_name}, {away_team_name}, {home_team_score}, {away_team_score}, {stats_array}")
            return True
        
        except mysql.connector.Error as error: # If something happens in our insert
            self.__db.rollback() # We cancel our insert
            logging.warning(f"Rolled back the transaction : {error}")
            return False
            pass