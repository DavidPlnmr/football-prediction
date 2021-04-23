#!/usr/bin/python3
"""
The purpose of this script is to see if the class Prediction works correctly
"""
from prediction_class import Prediction

first_team = "Wolves"
second_team = "Burnley"

pred = Prediction(first_team, second_team)

print(pred.define_winner())
