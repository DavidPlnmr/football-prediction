#!/usr/bin/python3
from .provider import Provider
import lib.constants

class Competition:
    """
    Class to make a prediction on a whole competition
    """
    def __init__(self, league_id, log_path=""):
        self.standings = {}
        prov = Provider(log_path)
        response = prov.get_teams_from_league(int(league_id))
        print(response)
        pass