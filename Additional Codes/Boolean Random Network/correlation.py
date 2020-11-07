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

def corre(wild_type,out,top,nodes,index,numb):

    STATES = pickle.load(open(Path('OUTPUT',out,'states.f'), 'rb'))
    intermat = pickle.load(open(Path('OUTPUT',out,'intermat.f'), 'rb'))
    freq = STATES[:,-1].astype(int)
    stable_vects = STATES[:,:-1]
    del STATES
    stable_vects[stable_vects < 0] = 0
    stable_vects = stable_vects.astype('int')
    TADA = np.repeat(stable_vects, freq, axis=0)
    ###############################################################################################
    data = pd.DataFrame(data=TADA.T,index=nodes,columns=['run_'+str(i) for i in range(TADA.shape[0])])
    data = data.astype(float)
    data = data.reindex(index=top)

    @nb.jit(nogil = True,cache = True,fastmath = True)
    def correla(array):
        return np.corrcoef(array)

    DATA = correla(np.array(data))

    fig = plt.figure(figsize=(8,8))
    ax1 = fig.add_subplot(111)
    plt.imshow(DATA, cmap='seismic', interpolation='nearest')
    plt.colorbar()
    ax1.set_xticks(np.arange(len(top)))
    ax1.set_yticks(np.arange(len(top)))
    ax1.set_xticklabels(top,rotation=90, fontsize=10)
    ax1.set_yticklabels(top,fontsize=10)
    plt.setp(ax1.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    '''for i in range(len(top)):
        for j in range(len(top)):
            data_corr,data_p = stats.pearsonr(data.T[top[i]], data.T[top[j]])
            if data_p < 0.001:
                text = ax1.text(j, i, '***', ha="center", va="center", color="w", fontsize = 7)
            elif data_p < 0.005:
                text = ax1.text(j, i, '**', ha="center", va="center", color="w", fontsize = 7)
            elif data_p < 0.05:
                text = ax1.text(j, i, '*', ha="center", va="center", color="w", fontsize = 7)'''

    plt.savefig((Path('OUTPUT',out,'corre.png')))
    plt.close()

    ############################################################################################
    DATA = np.array(DATA)
    DATA[DATA > 0] = 1
    DATA[DATA < 0] = -1

    @nb.jit(nogil = True,cache = True,fastmath = True)
    def metric(DATA):
        a1 = np.sum(DATA[:22, :22])
        a2 = np.sum(DATA[23:, 23:])
        a3 = np.sum(DATA[23:,:22]) + np.sum(DATA[:22,23:])
        num = a1 + a2 - a3
        return num

    num = metric(DATA)

    Intermat = pickle.load(open(Path('OUTPUT',wild_type,'intermat.f'), 'rb'))
    Boolean = np.all(intermat == Intermat)

    if index == 0:
        f = open(Path('OUTPUT','corre.txt'),'w')
        num = len(stable_vects)
        f.write(str(index) + "\t" + str(num) + "\t" + str(num) + "\t" + str(Boolean) + "\n")
        f.close()
        return num
    else:
        f = open(Path('OUTPUT','corre.txt'),'a')
        f.write(str(index) + "\t" + str(numb) + "\t" + str(num) + "\t" + str(Boolean) + "\n")
        f.close()
        return
    ################################################################################################
