#!/usr/bin/python3
import os
from db_manager import DbManager
from dotenv import load_dotenv

load_dotenv()
db = DbManager("127.0.0.1", os.getenv("DB_USER"), os.getenv("DB_PASSWORD"))

#db.delete(6) # Delete at a specific id

#print (db.getAll()) # Get all the predictions

#db.insert("Home", "Tottenham", "Burnley", 1900, 1800, 2202, 1000) # Insert row in the table

#print(db.getPredictionWithSpecificTeams("Chelsea", "Arsenal")) # Returns prediction with 2 specific teams

print (db.getPredictionWithApiId(201908))