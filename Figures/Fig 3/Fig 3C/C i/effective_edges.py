import os, copy
import numpy as np
import math
import numba as nb
from pathlib import Path
import pandas as pd
import pickle
import matplotlib.pyplot as plt

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

nodes,intermat = Interaction('sclcnetwork', 'Ising')

upper_square = ['ASCL1', 'ATF2', 'CBFA2T2', 'CEBPD','ELF3','ETS2','FOXA1','FOXA2','FLI1','INSM1','KDM5B','LEF1','MYB','OVOL2','PAX5','PBX1','POU3F2','SOX11', 'SOX2', 'TCF12','TCF3','TCF4','NEUROD1']
lower_square = [i for i in nodes if i not in upper_square]

top = upper_square + lower_square

n = 10 #path length
inf = intermat.copy()
M_max = intermat.copy()
M_max[M_max != 0] = 1.0
for i in range(2,n):
    a = np.linalg.matrix_power(intermat, i).astype(float)
    b = np.linalg.matrix_power(M_max, i).astype(float)
    inf = inf + np.divide(a, b, out=np.zeros_like(a), where=b!=0)

inf = inf/n
inf[inf > 0] = 1.0
inf[inf < 0] = -1.0

#intermat = pd.DataFrame(intermat.T,index = nodes, columns = nodes)
intermat = pd.DataFrame(inf.T, index = nodes, columns = nodes) #Use this for influence matrix


Grouping = [['NEUROD1'],
            ['ELF3'],
            ]
A = copy.deepcopy(upper_square)
B = copy.deepcopy(lower_square)
for j,nj in enumerate(Grouping):
    globals()[chr(j+67)] = nj
    for i,ni in enumerate(nj):
        if ni in A:
            A.remove(ni)
        else:
            B.remove(ni)
name = []

Intermat = copy.deepcopy(intermat)
Inter_one = copy.deepcopy(Intermat)
Inter_one[Inter_one != 0] = 1

for i in range(len(Grouping)+2):
    name.append(chr(65+i))

Inf_Fin = [[0 for i in range(len(name))] for j in range(len(name))]
#ENTER THRESHOLD HERE
tsh = 0.05
for ni,i in enumerate(name):
    for nj,j in enumerate(name):
        temp1 = np.sum(np.array(intermat[globals()[j]].T[globals()[i]].T))
        temp2 = np.sum(np.array(Inter_one[globals()[j]].T[globals()[i]].T))
        if temp2 != 0 and abs(temp1/temp2) >= tsh:
            Inf_Fin[ni][nj] = temp1/temp2
            Inf_Fin[ni][nj] = Inf_Fin[ni][nj]/abs(Inf_Fin[ni][nj])
        elif temp2 != 0 and abs(temp1/temp2) < tsh:
            Inf_Fin[ni][nj] = 0
        else:
            Inf_Fin[ni][nj] = temp1

INF = pd.DataFrame(Inf_Fin,index = name, columns = name)

print(INF)
groups = [A,B]
for i in Grouping:
    groups.append(i)
file_name = "reduced_model1"
INF.to_excel(file_name+".xlsx")
with open(file_name+".txt", 'w') as f:
    for item in groups:
        f.write("{}\n".format(item))
