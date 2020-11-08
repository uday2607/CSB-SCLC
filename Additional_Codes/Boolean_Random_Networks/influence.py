import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt
import scipy.stats as stats
import os
from pathlib import Path
import pickle
import numba as nb
from numba import prange

def Influ(out,top,nodes,index,num_i):

    n = 11
    STATES = pickle.load(open(Path('OUTPUT',out,'states.f'), 'rb'))
    intermat = np.array(pickle.load(open(Path('OUTPUT',out,'intermat.f'), 'rb')))
    intermat = intermat.astype(float)

    freq = STATES[:,-1]
    stable_vects = STATES[:,:-1]
    del STATES

    stable_vects[stable_vects < 0] = 0
    stable_vects = stable_vects.astype('int')

    inf = intermat.copy()
    M_max = intermat.copy()
    M_max[M_max != 0] = 1.0
    for i in range(2,11):
        a = np.linalg.matrix_power(intermat, i).astype(float)
        b = np.linalg.matrix_power(M_max, i).astype(float)
        inf = inf + np.divide(a, b, out=np.zeros_like(a), where=b!=0)

    inf = inf/11
    inf[inf > 0] = 1
    inf[inf < 0 ] = -1

    data = pd.DataFrame(data=inf,index=nodes,columns=nodes)
    data = data.loc[top,top]
    inf = np.array(data)

    @nb.jit(nogil = True,cache = True,fastmath = True)
    def metric(DATA):
        a1 = np.sum(DATA[:22, :22])
        a2 = np.sum(DATA[23:, 23:])
        a3 = np.sum(DATA[23:,:22]) + np.sum(DATA[:22,23:])
        num = a1 + a2 - a3
        return num

    num = metric(inf.copy())

    fig, ax1 = plt.subplots()
    plt.imshow(inf, cmap='seismic', interpolation='nearest')
    plt.clim(-1,1)
    plt.colorbar()
    ax1.set_xticks(np.arange(len(top)))
    ax1.set_yticks(np.arange(len(top)))
    ax1.set_xticklabels(top,rotation=90, fontsize=10)
    ax1.set_yticklabels(top,fontsize=10)
    plt.setp(ax1.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    plt.title('n: ' +str(n)+'influence'+" | Metric J = "+str(num))
    plt.savefig(Path('OUTPUT',out,'influence.png'))
    plt.close()

    if index == 0:
        f = open(Path('OUTPUT','influ.txt'),'w')
        f.write(str(index) + "\t" + str(num) + "\t" + str(num) + "\n")
        f.close()
        return num
    else:
        f = open(Path('OUTPUT','influ.txt'),'a')
        f.write(str(index) + "\t" + str(num_i) + "\t" + str(num) + "\n")
        f.close()
        return
