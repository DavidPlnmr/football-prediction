async def make_prediction(self, first_team_key, second_team_key, first_team_name, second_team_name, first_team_badge, second_team_badge, out_list):
        """
        Method called by each process. Out_list is simple list
        """
        try:
            pred = Prediction(first_team_name, second_team_name)
            await pred.create_prediction()

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