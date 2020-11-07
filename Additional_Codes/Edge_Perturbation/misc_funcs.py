import os
import numpy as np
import math
import numba as nb
from pathlib import Path
import pandas as pd
import pickle

################################################################################################################

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

################################################################################################################

def num2vect(num,node_num):
    '''Converts a binary number into Vector.'''

    string = format(num, 'b').zfill(node_num)
    arr = np.fromiter(string, dtype=int)
    arr = np.where(arr <= 0, -1.0, arr)
    return arr.astype(np.float32)

def col2vect(arr,node_num):

    vect_arr = []
    for num in arr:
        num = int(num)
        vect_arr.append(num2vect(num,node_num))

    return np.array(vect_arr)

################################################################################################################

@nb.jit(nopython=True, cache=True, nogil=True, fastmath=True)
def bin2num(arr):

    num = 0
    n = len(arr)
    for i in range(n):
        num = num + arr[i]*(2**(n-i-1))

    return num

def vect2num(input):
    '''Converts Vector to a binary number for easy Graph creation'''

    arr = np.copy(input).astype(np.int8)
    arr = np.where(arr < 0, 0 ,arr)
    num = bin2num(arr)
    return num

def rows2num(arr):

    array = []
    for i in arr:
        array.append(vect2num(i))

    return np.array(array)

################################################################################################################

def load_data(file_name): #You may dump multiple objects to pickle file using 'ab' (append binary) attribute in the above function
    #This function can retrive multiple objects dumped to a single file
    with open(file_name, "rb") as f:
        while True:
            try:
                yield pickle.load(f) #if there's a single object dumped you can retrive it using pickle.load(file)
            except EOFError: #Once all the appended data is retrived, we get no data encounter error. So using try except we can break once we get all the data
                break

def pickle_file(arr, file_name):

    with open(file_name, 'wb') as file: #Always open file with 'wb' attributes when pickling. (wb -> write binary)
        pickle.dump(arr, file, protocol=pickle.HIGHEST_PROTOCOL) #HIGHEST_PROTOCOL -> fast and less memory

################################################################################################################
class STATES:
    def __init__(self,OR,n_rounds):
        self.n = len(OR)
        self.bool = OR[:,0:-1]
        self.num = rows2num(OR[:,0:-1])
        self.freq = OR[:,-1]/(2**n_rounds)
        self.len = len(OR.T)-1

def removal(in_mat,in_node,state,rem):
    if state == 1:
        N = []
        out_node = in_node.copy()
        out_mat = np.copy(in_mat)
        for node in rem:
            N.append(in_node.index(node))
            out_node.remove(node)
        out_mat = np.delete(out_mat,N,axis = 1)
        out_mat = np.delete(out_mat,N,axis = 0)
        return out_mat,out_node
    else:
        return in_mat,in_node
