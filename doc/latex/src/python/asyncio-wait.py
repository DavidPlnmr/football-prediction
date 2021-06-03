async def __async_wait_all_predictions(self, matches, out_list):
        """
        Wait for all the predictions to be completed
        """
        
        await asyncio.wait([self.make_prediction(match[0], match[1], match[2], match[3], match[4], match[5], out_list) for match in matches])