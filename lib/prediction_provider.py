#!/usr/bin/python3
import os
from dotenv import load_dotenv
from soccerPronostic.api import api_facade

class PredictionProvider():
    def __init__(self):
        load_dotenv()
        self.facade = ApiFacade(os.getenv("API_KEY"))
        
prov = PredictionProvider()