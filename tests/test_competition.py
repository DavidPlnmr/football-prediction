#!/usr/bin/python3
"""
The purpose of this script is to see if the class Competition works correctly
"""
import os
import sys

# insert the "football-prediction" directory into the sys.path
sys.path.insert(1, os.path.abspath(".."))

from lib.competition_class import Competition

comp = Competition(148, "../log/app.log")