def insert_prediction(self, prediction, home_team_name, away_team_name, league_id="NULL", league_name="NULL", date_of_game="NULL", api_match_id="NULL"):
        """
        Insert a prediction in the database with the parameters given.
        """
        try:
            self.__cursor.execute(f"""INSERT INTO prediction (
                            `prediction`, 
                            `api_match_id`, 
                            `home_team_name`, 
                            `away_team_name`, 
                            `league_id`,
                            `league_name`,
                            `date_of_game`)
                            VALUES ( "{prediction}", {api_match_id},  "{home_team_name}", "{away_team_name}", {league_id}, "{league_name}", "{date_of_game}");""")
        
            self.__db.commit() # Save the changes
            logging.info(f"Inserted prediction in the DB with params : {prediction}, {api_match_id}, {home_team_name}, {away_team_name}, {league_id}, {league_name}, {date_of_game}")
            return True
        except mysql.connector.Error as error: # If something happens in our insert
            logging.warning(f"Error with insert predicitons : {error}")
            return False
            pass