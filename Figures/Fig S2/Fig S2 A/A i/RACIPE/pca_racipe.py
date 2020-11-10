import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import betainc
from sklearn.preprocessing import scale
from misc_funcs import *
import pickle
import os
from pathlib import Path
import numba as nb

nodes,intermat = Interaction('sclcnetwork', 'Ising')

upper_square = ['ASCL1', 'ATF2', 'CBFA2T2', 'CEBPD','ELF3','ETS2','FOXA1','FOXA2','FLI1','INSM1','KDM5B','LEF1','MYB','OVOL2','PAX5','PBX1','POU3F2','SOX11', 'SOX2', 'TCF12','TCF3','TCF4','NEUROD1']
lower_square = [i for i in nodes if i not in upper_square]

upper_square.remove('NEUROD1')
upper_square.append('NEUROD1')

top = upper_square + lower_square

with open('racipe_up.data','rb') as f:
    Data = pickle.load(f)
    Data = np.array(Data)
data = pd.DataFrame(data=Data,index=nodes,columns=['run_'+str(i) for i in range(Data.shape[1])])
data = data.reindex(index=top)
data = np.array(data)

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

DATA, P = corrcoef(data)

with open("racipe_corre.data",'wb') as f:
    pickle.dump(DATA, f)

with open("racipe_p.data",'wb') as f:
    pickle.dump(P, f)
