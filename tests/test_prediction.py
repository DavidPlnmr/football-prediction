#!/usr/bin/python3
"""
The purpose of this script is to see if the class Prediction works correctly
"""
import os
import sys

# insert the "football-prediction" directory into the sys.path
sys.path.insert(1, os.path.abspath(".."))

from lib.prediction_class import *

first_team = "Juventus"
second_team = "Lazio"

pred = Prediction(first_team, second_team, "../log/app.log")

print(pred.define_winner())
