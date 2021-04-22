#!/usr/bin/python3
from provider import Provider

prov = Provider()
#print(prov.getAllStatsFromTeamsApi("Chelsea", "Burnley"))
print(prov.getAllStatsFromTeamsDB("Chelsea", "Burnley"))
#prov.save("Home", "Manchester United", "Southampton", 2000, 1090, 2090, 1000)