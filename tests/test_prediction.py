#!/usr/bin/python3
"""
The purpose of this script is to see if the class Prediction works correctly
"""
import os
import sys

# insert the "import_test" directory into the sys.path
sys.path.insert(1, os.path.abspath(".."))

from lib.prediction_class import *

first_team = "Tottenham"
second_team = "Sheffield Utd"

pred = Prediction(first_team, second_team)

print(pred.define_winner())
