#!/usr/bin/python3
from .provider_class import Provider
from .prediction_class import Prediction, TeamResult
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
    
    async def create(self):
        teams = await self.prov.get_teams_from_league(int(self.league_id))
        self.__history = []
        self.standing_computed = False
        
        # for team in teams:
        for i in range(len(teams)):
            self.standings.append({
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
        if len(self.__history) <= 0:
            matches = []
            for first_team in self.standings:
                for second_team in self.standings:
                    exist = False
                    
                    if [first_team["Name"],second_team["Name"]] in matches or [second_team["Name"],first_team["Name"]] in matches:
                        exist = True
                        
                    if first_team["Name"] != second_team["Name"] and not exist:    
                        matches.append([
                            first_team["Name"],
                            second_team["Name"]
                        ])
                    pass
                pass
            
            await self.__async_wait_all_predictions(matches, self.__history)

        return self.__history
        
    async def __async_wait_all_predictions(self, matches, out_list):
        """
        Wait for all the predictions to be completed
        """
        
        await asyncio.wait([self.make_prediction(match[0], match[1], out_list) for match in matches])
    
    async def make_prediction(self, first_team, second_team, out_list):
        """
        Method called by each process. Out_list is simple list
        """
        try:
            pred = Prediction(first_team, second_team)
            await pred.call_data()

            winner = pred.define_winner()
            game = {
                "Home" : first_team,
                "Away" : second_team,
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
            await self.compute_competition() 
            for team in self.standings:
                team_name = team["Name"]
                for i in range(len(self.__history)):
                    game = self.__history[i]
                    if team_name == game["Home"] or team_name == game["Away"]:
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
    