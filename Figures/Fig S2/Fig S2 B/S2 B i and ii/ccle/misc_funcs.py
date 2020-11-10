import os
import numpy as np
from pathlib import Path
import pandas as pd
import pickle

def Interaction(file, model):
    ''' Reads .ids and .topo file to get nodes and interactions '''

    path = os.getcwd()  # current working directory
    NODES = [
        x.split('\t')[0] for x in open(
            Path(
                path + '/' +
                file +
                '.ids')).readlines()]  # Contains all the nodes (from .ids)

    INTERMAT = np.ascontiguousarray([[0] * len(NODES)] * len(NODES))  # Interaction matrix

    Models = ['Ising', 'InhibitoryDominant',
              'ActivatoryDominant']  # All Models
    # Differnt edge weights for different models
    Edge_weights = [[1.0, -1.0], [1.0, -1000.0], [1000.0, -1.0]]
    for line in open(
        Path(
            path + '/' +
            file +
            '.topo')).readlines()[
            1:]:  # reads interactions from .topo file
        res = line.split()
        if res[2] == '1':
            INTERMAT[NODES.index(res[1])][NODES.index(
                res[0])] = Edge_weights[Models.index(model)][0]
        if res[2] == '2':
            INTERMAT[NODES.index(res[1])][NODES.index(
                res[0])] = Edge_weights[Models.index(model)][1]

    return NODES, INTERMAT

def num2vect(num,node_num):
    '''Converts a binary number into Vector.'''

    string = format(num, 'b').zfill(node_num)
    arr = np.fromiter(string, dtype=int)
    arr = np.where(arr <= 0, -1.0, arr)
    return arr.astype(np.float32)
