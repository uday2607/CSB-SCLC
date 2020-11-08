import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import betainc
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

with open('racipe_up.data1','rb') as f:
    Data = pickle.load(f)
Data = np.array(Data.astype(float))
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

fig = plt.figure(figsize=(8,8))
ax1 = fig.add_subplot(111)
plt.imshow(DATA, cmap='seismic', interpolation='nearest')
plt.colorbar()
ax1.set_yticks(np.arange(len(top)))
ax1.set_xticks(np.arange(-0.5,len(top),1), minor=True);
ax1.set_yticks(np.arange(-0.5,len(top),1), minor=True);
ax1.set_yticklabels(labels=np.arange(1,len(top)+1), minor=False)
ax1.grid(which='minor', color='w', linestyle='-', linewidth=0.2)
plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

@nb.jit(nogil = True,cache = True,fastmath = True)
def metric(DATA):
    a1 = np.sum(DATA[:22, :22])
    a2 = np.sum(DATA[23:, 23:])
    a3 = np.sum(DATA[23:,:22]) + np.sum(DATA[:22,23:])
    num = a1 + a2 - a3
    return num

num = metric(DATA)

plt.savefig('racipe_corre.jpeg', dpi = 300)
