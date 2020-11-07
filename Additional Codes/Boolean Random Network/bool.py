import os, sys, time, random
import numpy as np
from pathlib import Path

from Utilities.Parser import *


random.seed(os.urandom(10))  # Best Random seed

''' I am trying to automize everything. Let's Hope it is faster '''
''' Using many parts from SimpleBool package '''
'''I am using Class which makes I think makes my life a lot easier. Let's See'''
''' Using Class for these operations is a terible Idea. Never do it!!! '''
'''I hope Iron Man is with me throughout the Journey'''

# global variables. Nodes record names of all nodes. InterMat record edge
# weights of all the interactions
global NODES, INTERMAT

def main(rules_file, output_file):
    in_file = 'bool.in'  # takes in the default file

    INPUT = InputParser(in_file)
    NODES, INTERMAT = ReadRules(rules_file, INPUT['model'])
    IniState, FixedState, TurnState = PreDefine(INPUT, NODES)

    if INPUT['mode'] == 'Sync':
        from Methods.Sync import SummarySync
        SummarySync(
            NODES, INTERMAT,
            INPUT, IniState,
            FixedState, TurnState,
            folder=output_file)
        #print("All the analysis is done. Bye ;)")
    elif INPUT['mode'] == 'Async':
        from Methods.Async import SummaryAsync
        SummaryAsync(
            NODES, INTERMAT,
            INPUT, IniState,
            FixedState, TurnState,
            folder=output_file)
        #print("All the analysis is done. Bye ;)")
