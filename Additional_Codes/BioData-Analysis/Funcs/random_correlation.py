import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.special import betainc
import os, pickle
from pathlib import Path
import numba as nb
from copy import deepcopy

@nb.jit(nogil = True,cache = True,fastmath = True)
def correla(array):
    return np.corrcoef(array)

def corrcoef(matrix):
    r = correla(matrix)
    rf = r[np.triu_indices(r.shape[0], 1)]
    df = matrix.shape[1] - 2
    ts = rf * rf * (df / (1 - rf * rf))
    pf = betainc(0.5 * df, 0.5, df / (df + ts))
    p = np.zeros(shape=r.shape)
    p[np.triu_indices(p.shape[0], 1)] = pf
    p[np.tril_indices(p.shape[0], -1)] = p.T[np.tril_indices(p.shape[0], -1)]
    p[np.diag_indices(p.shape[0])] = np.zeros(p.shape[0])
    return r, p

@nb.jit(nogil = True,cache = True,fastmath = True)
def metric(DATA):
    a1 = np.sum(DATA[:22, :22])
    a2 = np.sum(DATA[23:, 23:])
    a3 = np.sum(DATA[23:,:22]) + np.sum(DATA[:22,23:])
    num = a1 + a2 - a3
    return num + 1

def Discrete_corre1(data,nodes): # Al discrete

    DATA, P = corrcoef(np.array(data))
    DATA[DATA > 0] = 1
    DATA[DATA < 0] = -1
    DATA = np.nan_to_num(DATA,nan=0,copy=True)
    
    return (metric(DATA)-len(nodes))/2

def Discrete_corre2(data,nodes): #Only stat sig discrete and rest zero

    DATA, P = corrcoef(np.array(data))
    DATA = np.nan_to_num(DATA,nan=0,copy=True)
    matrix = np.zeros(shape = DATA.shape)
    Ones = np.ones(shape = DATA.shape)
    matrix[np.logical_and(DATA > 0, P.T < 0.05)] = Ones[np.logical_and(DATA > 0, P.T < 0.05)]
    matrix[np.logical_and(DATA < 0, P.T < 0.05)] = -1*Ones[np.logical_and(DATA < 0, P.T < 0.05)]

    return (metric(matrix)-len(nodes))/2

def Discrete_corre3(data,nodes): #Only stat sig discrete and rest same

    DATA, P = corrcoef(np.array(data))
    DATA = np.nan_to_num(DATA,nan=0,copy=True)
    matrix = DATA.copy()
    Ones = np.ones(shape = DATA.shape)
    matrix[np.logical_and(DATA > 0, P.T < 0.05)] = Ones[np.logical_and(DATA > 0, P.T < 0.05)]
    matrix[np.logical_and(DATA < 0, P.T < 0.05)] = -1*Ones[np.logical_and(DATA < 0, P.T < 0.05)]

    return (metric(matrix)-len(nodes))/2

def Random_corre(Data,title,folder,**kwargs):

    Nodes = []
    for node in open('sclcnetwork.ids').readlines():
        Nodes.append(str(node.split('\t')[0].strip()))
    Nodes = sorted(Nodes)

    upper_square = ['ASCL1', 'ATF2', 'CBFA2T2', 'CEBPD','ELF3','ETS2','FOXA1','FOXA2','FLI1','INSM1','KDM5B','LEF1','MYB','OVOL2','PAX5','PBX1','POU3F2','SOX11', 'SOX2', 'TCF12','TCF3','TCF4','NEUROD1']
    lower_square = [i for i in Nodes if i not in upper_square]

    top = upper_square + lower_square

    Remove = []
    for node in Nodes:
        if not node in list(Data.index):
            Remove.append(node)

    for node in Remove:
        Nodes.remove(node)

    if len(Remove) > 0:
        with open(Path(folder,'Nodes_not_found.txt'),'w') as f:
            f.write("The nodes of SCLC which are not found in dataset are \n\n")
            for node in Remove:
                f.write(node+'\n')

    DaTa = Data.loc[Nodes].copy()
    DaTa = np.array(DaTa.astype('float64'))

    data = pd.DataFrame(data=DaTa,index=Nodes,columns=['run_'+str(i) for i in range(Data.shape[1])])
    for node in Remove:
        data.loc[node] = np.zeros(Data.shape[1])
    data = data.reindex(index=top)
    data = np.array(data)

    J_vals = pd.DataFrame(index = ['J_vals'], columns = [1,2,3])
    J_vals[1] = Discrete_corre1(data,Nodes)
    J_vals[2] = Discrete_corre2(data,Nodes)
    J_vals[3] = Discrete_corre3(data,Nodes)

    J_vals.to_excel("{}_discrete_J.xlsx".format(title))
