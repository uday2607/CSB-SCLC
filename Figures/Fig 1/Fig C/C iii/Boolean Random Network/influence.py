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

def Influ(out,top,nodes):

    n = 10
    STATES = pickle.load(open(Path('OUTPUT',out,'states.f'), 'rb'))
    intermat = np.array(pickle.load(open(Path('OUTPUT',out,'intermat.f'), 'rb')))
    intermat = intermat.astype(float)

    freq = STATES[:,-1]
    stable_vects = STATES[:,:-1]
    del STATES

    stable_vects[stable_vects < 0] = 0
    stable_vects = stable_vects.astype('int')

    inf = intermat.copy()

    @nb.jit(nogil=True,cache = True,fastmath = True)
    def pathlength(inf,intermat,n):
        for i in range(n-2):
            inf = inf + np.linalg.matrix_power(intermat, i+2)/(i+2)
        return inf

    inf = pathlength(inf,intermat,n)
    inf[inf > 0] = 1
    inf[inf < 0] = -1
    ###############################################################################################
    temp = [[0]*len(top) for _ in range(len(top))]
    INTERMAT = pd.DataFrame(temp, index=top, columns=top)
    for i in top:
        for j in top:
            INTERMAT[i][j] = inf[nodes.index(i)][nodes.index(j)]

    arr = np.array([[0]*len(top)]*len(top))
    for run, vects in enumerate(stable_vects):
        vect = []
        for num_i,i in enumerate(top):
            vect.append(vects[nodes.index(i)])
            for num_j,j in enumerate(top):
                if INTERMAT[i][j] == 1:
                    arr[num_i][num_j] += 1*freq[run] if vects[nodes.index(i)] == vects[nodes.index(j)] else -1*freq[run]
                if INTERMAT[i][j] == -1:
                    arr[num_i][num_j] += 1*freq[run] if vects[nodes.index(i)] != vects[nodes.index(j)] else -1*freq[run]

    arr = arr/sum(freq)
    vect = np.array(vect)
    fig = plt.figure(figsize=(8,8))
    ax1 = fig.add_subplot(111)
    plt.imshow(arr, cmap='seismic', interpolation='nearest')
    plt.clim(-1,1)
    plt.colorbar()
    ting = str(np.array2string(vect,separator=','))
    ax1.set_xticks(np.arange(len(top)))
    ax1.set_yticks(np.arange(len(top)))
    ax1.set_xticklabels(top,rotation=90, fontsize=10)
    ax1.set_yticklabels(top,fontsize=10)
    plt.setp(ax1.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    plt.title('n: ' +str(n)+'influence')
    plt.savefig(Path('OUTPUT',out,'influence.png'))
    plt.close()
