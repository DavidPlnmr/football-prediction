#!/usr/bin/python3
"""
The purpose of this script is to see if the class Competition works correctly
"""
import os
import sys
import asyncio

# insert the "football-prediction" directory into the sys.path
sys.path.insert(1, os.path.abspath(".."))


from lib.competition_class import Competition

comp = Competition(148, "../log/app.log")

out_list = []

async def main():
    await asyncio.wait([comp.make_prediction("Arsenal", "Tottenham", out_list), comp.make_prediction("Chelsea", "Leeds", out_list)])
    
if __name__ == '__main__':
    asyncio.run(main())
    print(out_list)
    
# match_history = comp.compute_competition()
# standing = comp.get_standing()

# print(match_history)
# print(len(match_history))

