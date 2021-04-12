#!/usr/bin/python3
import os
import mysql.connector
from dotenv import load_dotenv
import logging

class DbManager:
    """
    This class only works with the structure set in the db.sql file
    """
    def __init__(self, hostname, username, pwd):
        """
        Method to initialize the class
        """
        logging.basicConfig(filename='../log/app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
        self.__db = mysql.connector.connect(host=hostname, user=username, password=pwd, database="soccerPronostic")
        self.__cursor = self.__db.cursor(dictionary=True) # Used to have a dictionary for each row
        
        logging.info("Connector to the DB correctly made")
        
    def query(self):
        """
        Make a query in the specified table
        """
        return self.own_query("SELECT * FROM prediction")
    
    
    def own_query(self, your_query):
        """
        Make your own query in the specified table. Make sure to only give a SELECT statement, otherwise your query won't work.
        """
        self.__cursor.execute(your_query)
        return self.__cursor.fetchall()
    
    def insert(self, prediction, hometeam, awayteam, off_score_hometeam, def_score_hometeam, off_score_awayteam, def_score_awayteam, api_match_id="NULL"):
        """
        Insert in the database with the parameters given.
        """
        self.__cursor.execute(f"""INSERT INTO prediction (
                            `prediction`, 
                            `api_match_id`, 
                            `hometeam_name`, 
                            `awayteam_name`, 
                            `off_score_hometeam`,
                            `def_score_hometeam`,
                            `off_score_awayteam`,
                            `def_score_awayteam`)
                            VALUES ( "{prediction}", {api_match_id},  "{hometeam}", "{awayteam}", {off_score_hometeam}, {def_score_hometeam}, {off_score_awayteam}, {def_score_hometeam});""")
        
        self.__db.commit() # Save the changes
        logging.info(f"Inserted in the DB with params : {prediction}, {api_match_id}, {hometeam}, {awayteam}, {off_score_hometeam}, {def_score_hometeam}, {off_score_awayteam}, {def_score_awayteam}")
        return True
    
    def delete_at(self, id):
        """
        Delete the row with the id in parameter
        """
        self.__cursor.execute(f"DELETE FROM prediction WHERE id={id}")
        self.__db.commit() # Save the changes
        logging.info(f"Deleted row with id = {id}")
        return True
        
        
    def disconnect(self):
        """
        Close the connection to the db
        """
        self.__cursor.close()
        self.__db.close()
        logging.info("Disconnected the connector to the DB")