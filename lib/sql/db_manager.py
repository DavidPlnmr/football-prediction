#!/usr/bin/python3
import mysql.connector
import logging

class DbManager:
    """
    This class only works with the structure set in the db.sql file
    """
    def __init__(self, hostname, username, pwd, log_path):
        """
        Method to initialize the class
        """
        logging.basicConfig(filename=log_path, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
        self.__db = mysql.connector.connect(host=hostname, user=username, password=pwd, database="footballPrediction")
        self.__cursor = self.__db.cursor(dictionary=True) # Used to have a dictionary for each row
        
        logging.info("Connector to the DB correctly made")
        
    def get_all_predictions(self):
        """
        Get all the rows in the table
        """
        return self.__query("SELECT * FROM prediction")
    
    def get_predictions_in_interval(self, from_date, to_date):
        """
        Get all the rows in the table
        """
        query = f"""SELECT * 
                            FROM prediction p 
                            WHERE p.date_of_game >= "{from_date}" AND p.date_of_game <= "{to_date}" AND p.api_match_id IS NOT NULL ORDER BY date_of_game ;"""
        return self.__query(query)
        
    
    def get_prediction_with_specific_teams(self, first_team_name, second_team_name):
        """
        Get the prediction with specific teams
        """
        return self.__query(f"""SELECT * FROM prediction p 
                          WHERE (home_team_name="{first_team_name}" OR away_team_name="{first_team_name}") 
                          AND (home_team_name="{second_team_name}" OR away_team_name="{second_team_name}");""")
    
    def get_prediction_with_api_id(self, api_match_id):
        """
        Get predictions with a specifi api_match_id
        """
        return self.__query(f"""SELECT * FROM prediction p WHERE api_match_id={api_match_id};""")
    
    def get_matches_with_specific_teams(self, first_team_name, second_team_name, from_date="", to_date=""):
        """
        Get matches with specific teams [before the date specified in params if it is specified]
        """
        query = f"""SELECT m.id, m.date, m.time, m.league_id, m.league_name, m.home_team_name, m.away_team_name, m.home_team_score, m.away_team_score
                    FROM `match` m 
                    WHERE (m.home_team_name="{first_team_name}" OR m.away_team_name="{first_team_name}" OR m.home_team_name="{second_team_name}" OR m.away_team_name="{second_team_name}") """
        if len(from_date)>0 and len(to_date)>0:
            query += f'AND m.date > "{from_date}" AND m.date < "{to_date}"'
        
        query += ";"
        return self.__query(query)
    
    def get_matches_from_to(self, from_date, to_date, league_id=""):
        """
        Get matches from a date to an other
        """
        query = f"""SELECT m.id, m.date, m.time, m.league_id, m.league_name, m.home_team_name, m.away_team_name, m.home_team_score, m.away_team_score
                    FROM `match` m 
                    WHERE m.date > "{from_date}" AND m.date < "{to_date}" """
        if type(league_id)==int:
            query+= f" AND m.league_id={league_id}"            
        
        query += ";"
        return self.__query(query)
    
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
                                OR m.away_team_name="{second_team_name}"
                                AND m.`date` < "2019-09-19" """
        
        if len(from_date)>0 and len(to_date)>0:
            query += f'AND m.date > "{from_date}" AND m.date < {to_date}'
            
        query += ";"
        
        return self.__query(query)
    
    def __query(self, your_query):
        """
        Make your own query in the specified table. Make sure to only give a SELECT statement, otherwise your query won't work.
        """
        self.__cursor.execute(your_query)
        return self.__cursor.fetchall()
    
    def insert_prediction(self, prediction, home_team_name, away_team_name, off_score_home_team, def_score_home_team, off_score_away_team, def_score_away_team, date_of_game="NULL", api_match_id="NULL"):
        """
        Insert a prediction in the database with the parameters given.
        """
        self.__cursor.execute(f"""INSERT INTO prediction (
                            `prediction`, 
                            `api_match_id`, 
                            `home_team_name`, 
                            `away_team_name`, 
                            `off_score_home_team`,
                            `def_score_home_team`,
                            `off_score_away_team`,
                            `def_score_away_team`,
                            `date_of_game`)
                            VALUES ( "{prediction}", {api_match_id},  "{home_team_name}", "{away_team_name}", {off_score_home_team}, {def_score_home_team}, {off_score_away_team}, {def_score_home_team}, "{date_of_game}");""")
        
        self.__db.commit() # Save the changes
        logging.info(f"Inserted prediction in the DB with params : {prediction}, {api_match_id}, {home_team_name}, {away_team_name}, {off_score_home_team}, {def_score_home_team}, {off_score_away_team}, {def_score_away_team}, {date_of_game}")
        return True
    
    def delete_at(self, id):
        """
        Delete the row with the id in parameter
        """
        self.__cursor.execute(f"DELETE FROM prediction WHERE id={id}")
        self.__db.commit() # Save the changes
        logging.info(f"Deleted row with id = {id}")
        return True
    
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
        
        except mysql.connector.Error as error: # If something happens in our queries
            self.__db.rollback() # We cancel our queries
            logging.warning(f"Rolled back the transaction : {error}")
            return False
            pass
        
    def disconnect(self):
        """
        Close the connection to the db
        """
        self.__cursor.close()
        self.__db.close()
        logging.info("Disconnected the connector to the DB")