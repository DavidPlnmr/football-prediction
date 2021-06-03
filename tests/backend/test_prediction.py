#!/usr/bin/python3
"""
The purpose of this script is to see if the class Prediction works correctly
"""
import os
import sys

# insert the "football-prediction" directory into the sys.path
sys.path.insert(1, os.path.abspath(".."))

from lib.prediction_class import *

first_team = "Chelsea"
second_team = "Tottenham"

async def main():
    pred = Prediction(first_team, second_team, "../log/app.log")
    await pred.create_prediction()
    print(pred.define_winner())
    
if __name__ == '__main__':
    asyncio.run(main())
    
