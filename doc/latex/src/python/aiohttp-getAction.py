async def __get_action(self, request_params):
        """
        Private method to call any endpoint of the API
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://apiv2.apifootball.com/?APIkey={self.api_key}&{request_params}') as response:
                    
                result = await response.text()

                if response.status == 200: # Code 200 = OK. Healthy connection
                    obj = json.loads(result)
                    # Check if obj contains error so there is problem in the API side
                    if 'error' in obj:
                        logging.error(f"Error {obj['error']} returned from the API with message : {obj['message']}. Request made : {request_params}")    
                        raise Exception(f"Error with the API : {obj['message']}. Request made : {request_params}")
                    else: # No error from the API we can return the result
                        logging.info(f"Request to the API with the params: {request_params}. Time lapsed {end_time-start_time}")
                        return obj # decode to get the content in string
                else:
                    # Error from the library
                    logging.error(f"Could not connect to the API. Error : {response.status} | Params : {request_params}")
                    raise Exception("Could not connect to the API.")