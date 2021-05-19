#!/usr/bin/python3
from .provider import Provider
from .prediction_class import Prediction
import lib.constants

import multiprocessing
import time

class Competition:
    """
    Class to make a prediction on a whole competition
    """
    def __init__(self, league_id, log_path=""):
        self.standings = {}
        prov = Provider(log_path)
        response = prov.get_teams_from_league(int(league_id))
        self.history = []
        
        for team in response:
            self.standings[team["team_name"]] = {
                "Badge" : team["team_badge"],
                "Wins" : 0,
                "Draws" : 0,
                "Loses" : 0,
                "Points" : 0
            }
        
    def compute_competition(self):
        """
        Compute the whole competitions using multiprocessing
        """
        matches = []
        for first_team in self.standings:
            for second_team in self.standings:
                exist = False
                
                if [first_team,second_team] in matches or [second_team,first_team] in matches:
                    exist = True
                    
                if first_team != second_team and not exist:    
                    matches.append([
                        first_team,
                        second_team
                    ])
                pass
            pass
        
        start = time.perf_counter()
        
        threads = len(matches)   # Number of threads to create

        # Create a list of jobs and then iterate through
        # the number of threads appending each thread to
        # the job list 
        jobs = []
        out_list = []
        for i in range(0, threads):
            thread = multiprocessing.Process(target=self.make_prediction, 
                                          args=(matches[i][0], matches[i][1], out_list))
            jobs.append(thread)

        # Start the threads 
        for j in jobs:
            j.start()
            time.sleep(1)

        # Ensure all of the threads have finished
        for j in jobs:
            j.join()    
        
        end = time.perf_counter()
        print(f"Finished in {end-start} seconds")
        return out_list
                      

    def make_prediction(self, first_team, second_team, out_list):
        #try:
            pred = Prediction(first_team, second_team)
            winner = pred.define_winner()
            out_list.append({
                "Home" : first_team,
                "Away" : second_team,
                "Prediction" : winner
            })
        #except Exception:
            #print(f"Unable to make the prediction between the team {first_team} and {second_team}")
            pass
        