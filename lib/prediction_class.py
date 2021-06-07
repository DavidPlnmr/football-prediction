#!/usr/bin/python3

##
# @author David Paulino
# @brief Prediction class, Team Result and UnmakeablePrediction Exception
# @date 04.06.2021
# @version 1.0

from .provider_class import Provider, NoMatchError
import lib.constants
import asyncio

class Prediction:
    """
    Class to make a prediction on a match between two football teams
    """
    def __init__(self, home_team, away_team, log_path=""):
        """
        Constructor of the Prediction class.
        """
        self.__home_team_result = TeamResult(home_team)
        self.__away_team_result = TeamResult(away_team)
        self.__winner=""
        self.provider = Provider(log_path)
        
        
    async def create_prediction(self):
        """
        Async call the data for the class. It calls the get_all_stats_from_teams() method from the Provider class.
        """
        try:
            self.__results = await self.provider.get_all_stats_from_teams(self.get_home_team_name(), self.get_away_team_name())
            self.__home_team_result.heat_of_moment = self.__compute_heat_moment(self.get_home_team_name(), self.__results["firstTeam_lastResults"])
            self.__away_team_result.heat_of_moment = self.__compute_heat_moment(self.get_away_team_name(), self.__results["secondTeam_lastResults"])

            self.__insert_data_team_result(self.__home_team_result, self.__results["firstTeam_lastResults"])
            self.__insert_data_team_result(self.__away_team_result, self.__results["secondTeam_lastResults"])
            
            self.__insert_data_team_result(self.__home_team_result, self.__results["firstTeam_VS_secondTeam"])
            self.__insert_data_team_result(self.__away_team_result, self.__results["firstTeam_VS_secondTeam"])
        except Exception:
            raise UnmakeablePrediction("Prediction unmakeable. Not enough stats.")
        
    
    def define_winner(self):
        """
        Returns the winner of the prediction by computing the offensive score, defensive score and the heat of moment.
        """
        #This check is here to not compute everything if we already have the name of the winner
        if self.__winner== "":
            if self.__home_team_result.games_count > 0 and self.__away_team_result.games_count > 0:    
                # Adding the off score
                home_team_final_score = self.__compute_off_score(self.__home_team_result)
                away_team_final_score = self.__compute_off_score(self.__away_team_result)
                
                #Adding the def score
                home_team_final_score += self.__compute_def_score(self.__home_team_result)
                away_team_final_score += self.__compute_def_score(self.__away_team_result)
                
                #Adding the heat of the moment score
                home_team_final_score += self.__compute_heat_moment_score(self.__home_team_result)
                away_team_final_score += self.__compute_heat_moment_score(self.__away_team_result)
                
                if home_team_final_score > away_team_final_score * lib.constants.DELTA_TO_DETERMINE_DRAW:
                    self.__winner = self.get_home_team_name()    
                elif away_team_final_score > home_team_final_score * lib.constants.DELTA_TO_DETERMINE_DRAW:
                    self.__winner = self.get_away_team_name()    
                else:
                    self.__winner = "Draw"
            else :
                raise NoMatchError("No games count")
        return self.__winner
    
    def save_prediction(self, league_id="NULL", league_name="NULL", date_of_game="NULL", api_match_id="NULL"):
        """
        Save the prediction in the DB
        """
        return self.provider.save_prediction(self.define_winner(),
                                             self.get_home_team_name(),
                                             self.get_away_team_name(),
                                             league_id,
                                             league_name,
                                             date_of_game,
                                             api_match_id)
        
    def get_home_team_name(self):
        """
        Get the home team name.
        """
        return self.__home_team_result.team_name
    
    def get_away_team_name(self):
        """
        Get the away team name.
        """
        return self.__away_team_result.team_name
        
    def __compute_heat_moment_score(self, team_result):
        return team_result.average_points_per_game()*lib.constants.WEIGHT_HEAT_OF_MOMENT
        pass
        
    def __compute_heat_moment(self, team_name, last_results):
        """
        Compute the heat of the moment of the team with its last results
        """
        if len(last_results)>0:
            
            heat_of_moment = ""
            if len(last_results) > lib.constants.NB_GAMES_HEAT_OF_THE_MOMENT:    
                for index in range(lib.constants.NB_GAMES_HEAT_OF_THE_MOMENT):
                    result = int(last_results[index]["home_team_score"]) - int(last_results[index]["away_team_score"])
                    if result == 0:
                        heat_of_moment += 'D' # D for Draw
                    else:
                        if last_results[index]["home_team"] == team_name:
                            heat_of_moment += 'W' if result > 0 else 'L' # W for Win, L for Lose
                        else:
                            heat_of_moment += 'L' if result > 0 else 'W' # W for Win, L for Lose
            return heat_of_moment
        else:
            raise NoMatchError("No games in the last results")
    
    def __compute_off_score(self, team_result):
        """
        Compute the score using the offensive stats
        """
        score = 0
        
        score += team_result.average_goal_scored_per_game()*lib.constants.WEIGHT_GOALS
        score += team_result.average_dangerous_attacks_per_game()*lib.constants.WEIGHT_DANGEROUS_ATTACKS
        score += team_result.average_shots_on_goal_per_game()*lib.constants.WEIGHT_SHOTS_ON_GOAL
        score += team_result.average_attacks_per_game()*lib.constants.WEIGHT_ATTACKS
        score += team_result.average_goal_attempts_per_game()*lib.constants.WEIGHT_GOAL_ATTEMPTS
        score += team_result.average_ball_possession_per_game()*lib.constants.WEIGHT_BALL_POSSESSION

        return score
        pass

    def __compute_def_score(self, team_result):
        """
        Compute the score using the defensive stats
        """
        score = 0
        #Bonus
        score += team_result.average_tackles_per_game()*lib.constants.WEIGHT_TACKLES
        score += team_result.average_goalkeeper_saves_per_game()*lib.constants.WEIGHT_GOALKEEPER_SAVES
        
        #Malus
        score -= team_result.average_goal_conceded_per_game()*lib.constants.WEIGHT_GOALS
        score -= team_result.average_fouls_per_game()*lib.constants.WEIGHT_FOULS
        score -= team_result.average_yellow_cards_per_game()*lib.constants.WEIGHT_YELLOW_CARDS
        
        return score
        pass

    def __insert_data_team_result(self, team_result_obj, last_results):
        """
        For each game in the last_results array, we insert the stats in team_result_obj
        """
        for match in last_results:
                team_result_obj.games_count += 1
                
                team_result_obj.goals_scored_count += int(match["home_team_score"]) if team_result_obj.team_name == match["home_team"] else int(match["away_team_score"])
                # This line is the reverse of the top one
                team_result_obj.goals_conceded_count += int(match["home_team_score"]) if team_result_obj.team_name != match["home_team"] else int(match["away_team_score"])
                stats = match["stats"]
                #These 2 lines are here to remove the "%" char of the Ball Possession Stat
                stats["Ball Possession"]["home"] = stats["Ball Possession"]["home"].replace('%', '')
                stats["Ball Possession"]["away"] = stats["Ball Possession"]["away"].replace('%', '')

                team_result_obj.ball_possession += int(stats["Ball Possession"]["home"]) if team_result_obj.team_name == match["home_team"] else int(stats["Ball Possession"]["away"])
                
                team_result_obj.goal_attempts += int(stats["Goal Attempts"]["home"]) if team_result_obj.team_name == match["home_team"] else int(stats["Goal Attempts"]["away"])
                
                team_result_obj.shots_on_goal += int(stats["Shots on Goal"]["home"]) if team_result_obj.team_name == match["home_team"] else int(stats["Shots on Goal"]["away"])
                
                team_result_obj.goalkeeper_saves += int(stats["Goalkeeper Saves"]["home"]) if team_result_obj.team_name == match["home_team"] else int(stats["Goalkeeper Saves"]["away"])
                
                team_result_obj.fouls += int(stats["Fouls"]["home"]) if team_result_obj.team_name == match["home_team"] else int(stats["Fouls"]["away"])
                
                team_result_obj.yellow_cards += int(stats["Yellow Cards"]["home"]) if team_result_obj.team_name == match["home_team"] else int(stats["Yellow Cards"]["away"])
                
                team_result_obj.tackles += int(stats["Tackles"]["home"]) if team_result_obj.team_name == match["home_team"] else int(stats["Tackles"]["away"])
                
                team_result_obj.attacks += int(stats["Attacks"]["home"]) if team_result_obj.team_name == match["home_team"] else int(stats["Attacks"]["away"])
                
                team_result_obj.dangerous_attacks += int(stats["Dangerous Attacks"]["home"]) if team_result_obj.team_name == match["home_team"] else int(stats["Dangerous Attacks"]["away"])
               
class TeamResult:
    """
    This is a class but it works more like a structure because it stores data. Otherwise, it has methods that return the average stats of a team.
    """
    def __init__(self, team_name):
        """
        Constructor of the TeamResult class.
        """
        self.team_name = team_name
        self.heat_of_moment = ""
        self.games_count = 0
        self.goals_scored_count = 0
        self.goals_conceded_count = 0
        self.ball_possession = 0
        self.goal_attempts = 0
        self.shots_on_goal = 0
        self.goalkeeper_saves = 0
        self.fouls = 0
        self.yellow_cards = 0
        self.tackles = 0
        self.attacks = 0
        self.dangerous_attacks = 0
        
    def average_goal_scored_per_game(self):
        """
        Make an average of the goals scored per game
        """
        return self.goals_scored_count/self.games_count
    
    def average_goal_conceded_per_game(self):
        """
        Make an average of the goals conceded per game
        """
        return self.goals_conceded_count/self.games_count
    
    def average_ball_possession_per_game(self):
        """
        Make an average of the ball possession per game
        """
        return self.ball_possession/self.games_count
    
    def average_goal_attempts_per_game(self):
        """
        Make an average of the goal attempts per game
        """
        return self.goal_attempts/self.games_count
    
    def average_shots_on_goal_per_game(self):
        """
        Make an average of the shots on goal per game
        """
        return self.shots_on_goal/self.games_count
    
    def average_goalkeeper_saves_per_game(self):
        """
        Make an average of the saves per game
        """
        return self.goalkeeper_saves/self.games_count
    
    def average_fouls_per_game(self):
        """
        Make an average of the fouls per game
        """
        return self.fouls/self.games_count
    
    def average_yellow_cards_per_game(self):
        """
        Make an average of the yellow cards per game
        """
        return self.yellow_cards/self.games_count
    
    def average_tackles_per_game(self):
        """
        Make an average of the tackles per game
        """
        return self.tackles/self.games_count
    
    def average_attacks_per_game(self):
        """
        Make an average of the attacks per game
        """
        return self.attacks/self.games_count
    
    def average_dangerous_attacks_per_game(self):
        """
        Make an average of the dangerous attacks per game
        """
        return self.dangerous_attacks/self.games_count  
    
    def average_points_per_game(self):
        """
        Make an average of the points won per game with the heat of the moment
        
        3 pts for a win.
        1 pt for a draw.
        0 pts for a loss.
        """
        result = 0
        for char in self.heat_of_moment:
            if char=='W':
                result+=lib.constants.POINTS_FOR_A_WIN
            elif char=='D':
                result+=lib.constants.POINTS_FOR_A_DRAW
            elif char=='L':
                result+=lib.constants.POINTS_FOR_A_LOSE
        return result/self.games_count
    
class UnmakeablePrediction(Exception):
    """
    Class that inherit from Exception. It has no special methods. It is just here to have a more precise Exception.
    """
    pass