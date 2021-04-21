#!/usr/bin/python3
import os
from db_manager import DbManager
from dotenv import load_dotenv

load_dotenv()
db = DbManager(os.getenv("DB_HOST"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), '../log/app.log')

#db.delete(6) # Delete at a specific id

#db.insertPrediction("Home", "Tottenham", "Burnley", 1900, 1800, 2202, 1000) # Insert row in the table

#print (db.getAllPredictions()) # Get all the predictions

#print(db.getPredictionWithSpecificTeams("Tottenham", "Burnley")) # Returns prediction with 2 specific teams

#print (db.getPredictionWithApiId(201908))



print(db.getStatsOfMatches("Chelsea", "Burnley"))

"""for match in response:
      print(match["id"], match["date"], match["time"])"""



"""stats = [
      {
        "type": "Ball Possession",
        "home": "65%",
        "away": "35%"
      },
      {
        "type": "Goal Attempts",
        "home": "16",
        "away": "4"
      },
      {
        "type": "Shots on Goal",
        "home": "7",
        "away": "1"
      },
      {
        "type": "Shots off Goal",
        "home": "7",
        "away": "3"
      },
      {
        "type": "Blocked Shots",
        "home": "2",
        "away": "0"
      },
      {
        "type": "Free Kicks",
        "home": "12",
        "away": "18"
      },
      {
        "type": "Corner Kicks",
        "home": "9",
        "away": "0"
      },
      {
        "type": "Offsides",
        "home": "3",
        "away": "2"
      },
      {
        "type": "Goalkeeper Saves",
        "home": "1",
        "away": "3"
      },
      {
        "type": "Fouls",
        "home": "15",
        "away": "12"
      },
      {
        "type": "Yellow Cards",
        "home": "2",
        "away": "1"
      },
      {
        "type": "Total Passes",
        "home": "541",
        "away": "290"
      },
      {
        "type": "Tackles",
        "home": "25",
        "away": "22"
      },
      {
        "type": "Attacks",
        "home": "121",
        "away": "94"
      },
      {
        "type": "Dangerous Attacks",
        "home": "68",
        "away": "12"
      }
    ]

db.insertMatchWithStats(273385, "2020-03-09", "21:00", 148, "Premier League", "Leicester", "Aston Villa", 4,0, stats)"""