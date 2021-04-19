#!/usr/bin/python3
from prediction_provider import PredictionProvider

prov = PredictionProvider()
print(prov.getAllStatsFromTeams("Chelsea", "Burnley"))
#prov.save("Home", "Manchester United", "Southampton", 2000, 1090, 2090, 1000)