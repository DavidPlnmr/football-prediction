#!/usr/bin/python3
from .provider_class import Provider
from .prediction_class import Prediction, TeamResult
import lib.constants

import multiprocessing
import time

class Competition:
    """
    Class to make a prediction on a whole competition
    """
    def __init__(self, league_id, log_path=""):
        self.standings =  []
        prov = Provider(log_path)
        teams = prov.get_teams_from_league(int(league_id))
        self.history = []
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
        
    def compute_competition(self):
        """
        Compute the whole competitions using multiprocessing
        """
        if len(self.history) <= 0:
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
            
            #start = time.perf_counter()
            
            threads = len(matches)   # Number of threads to create
            manager = multiprocessing.Manager()
            out_list = manager.list()
            
            # Create a list of jobs and then iterate through
            # the number of threads appending each thread to
            # the job list 
            jobs = []
            
            for i in range(0, threads):
                thread = multiprocessing.Process(target=self.make_prediction, 
                                            args=(matches[i][0], matches[i][1], out_list))
                jobs.append(thread)

            # Start the threads 
            for j in jobs:
                j.start()
                time.sleep(0.1)

            # Ensure all of the threads have finished
            for j in jobs:
                
                j.join()    
            
            #end = time.perf_counter()
            #print(f"Finished in {end-start} seconds")
            print(len(out_list))
            print(threads)
            self.history = out_list
        return self.history

    def get_standing(self):
        """
        Get the standing with the self.history var. It will return the standing of the competition sorted by points
        """
        if not self.standing_computed:    
            for team in self.standings:
                team_name = team["Name"]
                for i in range(len(self.history)):
                    game = self.history[i]
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
        
    def make_prediction(self, first_team, second_team, out_list):
        """
        Method called by each process. Out_list is Manager.list() to share the memory for each process
        """
        # try:
        pred = Prediction(first_team, second_team)
        winner = pred.define_winner()
        game = {
            "Home" : first_team,
            "Away" : second_team,
            "Prediction" : winner
        }
        out_list.append(game)
            
        # except Exception:
        #     print(f"Unable to make the prediction between the team {first_team} and {second_team}")
        #     pass
    
def sort_by_team_points(team):
    return team.get("Points")
    