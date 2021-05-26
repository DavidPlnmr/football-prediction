#!/usr/bin/python3
"""
The purpose of this script is to see if the class Competition works correctly
"""
import os
import sys

# insert the "football-prediction" directory into the sys.path
sys.path.insert(1, os.path.abspath("."))


from lib.competition_class import Competition

comp = Competition(262, "./log/app.log")

match_history = comp.compute_competition()
standing = comp.get_standing()

#print(match_history)
#print(len(match_history))

print(standing)