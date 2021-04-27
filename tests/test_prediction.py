#!/usr/bin/python3
"""
The purpose of this script is to see if the class Prediction works correctly
"""
from lib.prediction_class import *

first_team = "Liverpool"
second_team = "Newcastle"

pred = Prediction(first_team, second_team)

print(pred.define_winner())
