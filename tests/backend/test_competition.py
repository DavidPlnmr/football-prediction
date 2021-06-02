#!/usr/bin/python3
"""
The purpose of this script is to see if the class Competition works correctly
"""
import os
import sys
import asyncio
import time

# insert the "football-prediction" directory into the sys.path
sys.path.insert(1, os.path.abspath(".."))


from lib.competition_class import Competition



out_list = []

async def main():
    comp = Competition(176, "../log/app.log")
    await comp.create()
    #await asyncio.wait([comp.make_prediction("Arsenal", "Tottenham", out_list), comp.make_prediction("Chelsea", "Leeds", out_list)])
    start = time.perf_counter()
    await asyncio.wait([comp.compute_competition()])
    standing = await comp.get_standing()
    end = time.perf_counter()
    print(f"Time elapsed : {end-start}")
    print(standing)
    
if __name__ == '__main__':
    asyncio.run(main())
    
# match_history = comp.compute_competition()
# standing = comp.get_standing()

# print(match_history)
# print(len(match_history))

