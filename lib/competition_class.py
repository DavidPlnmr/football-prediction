#!/usr/bin/python3
from .provider_class import Provider
from .prediction_class import Prediction
import lib.constants

import asyncio

class Competition:
    """
    Class to make a prediction on a whole competition
    """
    def __init__(self, league_id, log_path=""):
        self.standings =  []
        self.league_id = league_id
        self.prov = Provider(log_path)
        self.missed_some_predictions = False
    
    async def create(self):
        teams = await self.prov.get_teams_from_league(int(self.league_id))
        self.__history = []
        self.standing_computed = False
        
        for i in range(len(teams)):
            self.standings.append({
                "Key" : teams[i]["team_key"],
                "Name" : teams[i]["team_name"],
                "Badge" : teams[i]["team_badge"],
                "Games" : 0,
                "Wins" : 0,
                "Draws" : 0,
                "Losses" : 0,
                "Points" : 0
            })
        
    async def compute_competition(self):
        """
        Compute the whole competitions using async
        """
        matches = []
        if len(self.__history) <= 0:
            
            for first_team in self.standings:
                for second_team in self.standings:
                    exist = False
                    
                    if [first_team["Key"],
                        second_team["Key"],
                        first_team["Name"],
                        second_team["Name"],
                        first_team["Badge"],
                        second_team["Badge"]] in matches or [second_team["Key"],
                                                            first_team["Key"],
                                                            second_team["Name"],
                                                            first_team["Name"],
                                                            second_team["Badge"],
                                                            first_team["Badge"]] in matches:
                        exist = True
                        
                    if first_team["Name"] != second_team["Name"] and not exist:    
                        matches.append([
                            first_team["Key"],
                            second_team["Key"],
                            first_team["Name"],
                            second_team["Name"],
                            first_team["Badge"],
                            second_team["Badge"]
                        ])
                    pass
                pass
            
            await self.__async_wait_all_predictions(matches, self.__history)

        self.missed_some_predictions = len(self.__history) != len(matches)
        return self.__history
    
        
    async def __async_wait_all_predictions(self, matches, out_list):
        """
        Wait for all the predictions to be completed
        """
        
        await asyncio.wait([self.make_prediction(match[0], match[1], match[2], match[3], match[4], match[5], out_list) for match in matches])
    
    async def make_prediction(self, first_team_key, second_team_key, first_team_name, second_team_name, first_team_badge, second_team_badge, out_list):
        """
        Method called by each process. Out_list is simple list
        """
        try:
            pred = Prediction(first_team_name, second_team_name)
            await pred.call_data()

            winner = pred.define_winner()
            game = {
                "Home Key" : first_team_key,
                "Away Key" : second_team_key,
                "Home Name" : first_team_name,
                "Away Name" : second_team_name,
                "Home Badge" : first_team_badge,
                "Away Badge" : second_team_badge,
                "Prediction" : winner
            }
            out_list.append(game)
            
        except Exception:
            print(f"Unable to make the prediction between the team {first_team} and {second_team}")
            pass
    
    async def get_standing(self):
        """
        Get the standing with the self.__history var. It will return the standing of the competition sorted by points
        """
        if not self.standing_computed:   
            for team in self.standings:
                team_name = team["Name"]
                for i in range(len(self.__history)):
                    game = self.__history[i]
                    if team_name == game["Home Name"] or team_name == game["Away Name"]:
                        team["Games"] += 1
                        if team_name == game["Prediction"]:
                            team["Wins"] += 1
                            team["Points"] += lib.constants.POINTS_FOR_A_WIN
                        elif game["Prediction"] == "Draw":
                            team["Draws"] += 1
                            team["Points"] += lib.constants.POINTS_FOR_A_DRAW
                        else:
                            team["Losses"] += 1
                            team["Points"] += lib.constants.POINTS_FOR_A_LOSE
            self.standings = sorted(self.standings, key=sort_by_team_points, reverse=True)
        
        return self.standings
    
    
def sort_by_team_points(team):
    return team.get("Points")
    