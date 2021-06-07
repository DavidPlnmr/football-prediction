#!/usr/bin/python3
"""
The purpose of this script is to see if the class Prediction works correctly
"""
import os
import sys

# insert the "football-prediction" directory into the sys.path
path = os.path.abspath(".")
sys.path.insert(1, path)

from lib.prediction_class import *

first_team = "Napoli"
second_team = "AS Roma"

async def main():
    pred = Prediction(first_team, second_team, "./log/app.log")
    await pred.create_prediction()
    print(pred.define_winner())
    
if __name__ == '__main__':
    asyncio.run(main())
    
