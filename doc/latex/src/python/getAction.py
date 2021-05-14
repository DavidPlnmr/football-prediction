def __get_action(self, request_params):
        """
        Private method to call any endpoint of the API
        """
        response = requests.get(f'https://apiv2.apifootball.com/?APIkey={self.api_key}&{request_params}')

        if response.status_code == 200: # Code 200 = OK. Healthy connection
            obj = json.loads(response.content.decode('utf-8'))
            # Check if obj contains error so there is problem in the API side
            if 'error' in obj:
                logging.error(f"Error {obj['error']} returned from the API with message : {obj['message']}")    
                raise Exception(f"Error with the API : {obj['message']}")
            else: # No error from the API we can return the result
                logging.info(f"Request to the API with the params: {request_params}")
                return obj # decode to get the content in string
        else:
            # Error from the library
            logging.error(f"Happened during the request to the API with error : {response.status_code}")
            raise Exception("Could not connect to the API.")