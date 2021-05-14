def get_H2H(self, first_team_name, second_team_name):
        """
        Get the last results of each teams and the last results of each matchs between them both
        """
        endpoint_action = "get_H2H"
        return self.__get_action(f'action={endpoint_action}&firstTeam={first_team_name}&secondTeam={second_team_name}')