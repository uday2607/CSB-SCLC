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

@nb.jit(nogil = True,cache = True,fastmath = True)
def random_matrix(arr):
    arr = np.where(arr > 0,np.random.uniform(0.004,1,arr.shape),arr)
    arr = np.where(arr < 0,np.random.uniform(-1,-0.004,arr.shape),arr)

    return arr

def matrices1000(mat,vals):
    for i in range(vals.shape[0]):
        arr = np.copy(mat)
        vals[i] = metric(random_matrix(arr))

    return vals

def random_corre(top,nodes):

    with open('racipe_up.data','rb') as f:
        Data = pickle.load(f)

    data = Data.loc[nodes]
    data = data.astype('float64')
    data = data.loc[top]

    DATA, P = corrcoef(np.array(data))

    J_vas = np.zeros(1000)
    return matrices1000(DATA,J_vas)

def Discrete(top,nodes):

    with open('racipe_up.data','rb') as f:
        Data = pickle.load(f)

    data = Data.loc[nodes]
    data = data.astype('float64')
    data = data.loc[top]

    DATA, P = corrcoef(np.array(data))
    DATA[DATA > 0] = 1
    DATA[DATA < 0] = -1

    print((metric(DATA)-33)/2)

if __name__ == '__main__':

    nodes = []
    for node in open('sclcnetwork.ids').readlines():
        nodes.append(str(node.split('\t')[0].strip()))
    nodes = sorted(nodes)
    tada = ['ASCL1', 'ATF2', 'CBFA2T2', 'CEBPD','ELF3','ETS2','FOXA1','FOXA2','FLI1','INSM1','KDM5B','LEF1','MYB','OVOL2','PAX5','PBX1','POU3F2','SOX11', 'SOX2', 'TCF12','TCF3','TCF4','NEUROD1']
    ting = [i for i in nodes if i not in tada]
    top = tada+ting

    J_vals = pd.DataFrame(index = np.arange(1000), columns = [1])
    J_vals[1] = random_corre(top,nodes)
    J_vals.to_excel("RACIPE_J_vals.xlsx")
    Discrete(top,nodes)
