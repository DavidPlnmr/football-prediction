async def get_match_infos(self, match_id):
        """
        Get the last results of each teams and the last results of each matchs between them both
        """
        endpoint_action = "get_events"
        return await self.__get_action(f'action={endpoint_action}&match_id={match_id}')