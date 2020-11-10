import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt
import scipy.stats as stats
import os
from pathlib import Path
import pickle
from misc_funcs import *

def Influ(out, top, nodes):

    n = 11
    intermat = pickle.load(open('intermat.f', 'rb'))
    N = float(np.count_nonzero(intermat))
    inf = intermat.copy()
    M_max = intermat.copy()
    M_max[M_max != 0] = 1.0
    for i in range(2,n):
        a = np.linalg.matrix_power(intermat, i).astype(float)
        b = np.linalg.matrix_power(M_max, i).astype(float)
        inf = inf + np.divide(a, b, out=np.zeros_like(a), where=b!=0)

    inf = inf/n

    data = pd.DataFrame(data=inf,index=nodes,columns=nodes)
    data = data.loc[top,top]
    inf = np.array(data)

    STATES = pickle.load(open('states.f', 'rb'))
    freq = STATES[:,-1]
    stable_vects = STATES[:,:-1]
    stable_vects[stable_vects < 0] = 0
    stable_vects = stable_vects.astype('int')

    INTERMAT = pd.DataFrame(inf.T, index=top, columns=top)

    for run, vects in enumerate(stable_vects):
        arr = np.array([[0]*len(top)]*len(top))
        for num_i, i in enumerate(top):
            for num_j, j in enumerate(top):
                if INTERMAT[i][j] > 0:
                    arr[num_i][num_j] = 1 if vects[nodes.index(i)] == vects[nodes.index(j)] else -1
                if INTERMAT[i][j] < 0:
                    arr[num_i][num_j] = 1 if vects[nodes.index(i)] != vects[nodes.index(j)] else -1

        fig = plt.figure(figsize=(8,8))
        ax1 = fig.add_subplot(111)
        plt.imshow(arr, cmap='seismic', interpolation='nearest')
        plt.clim(-1,1)
        plt.colorbar()
        ax1.set_yticks(np.arange(len(top)))
        ax1.set_xticks(np.arange(-0.5,len(top),1), minor=True);
        ax1.set_yticks(np.arange(-0.5,len(top),1), minor=True);
        ax1.set_yticklabels(labels=np.arange(1,len(top)+1), minor=False)
        ax1.grid(which='minor', color='w', linestyle='-', linewidth=0.2)
        plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        plt.savefig(Path(out,"freq_{}.png".format(freq[run])))
        plt.close()

if __name__ == '__main__':
    if not os.path.exists('OUTPUT'):
        os.mkdir("OUTPUT")

    nodes,intermat = Interaction('sclcnetwork', 'Ising')

    upper_square = ['ASCL1', 'ATF2', 'CBFA2T2', 'CEBPD','ELF3','ETS2','FOXA1','FOXA2','FLI1','INSM1','KDM5B','LEF1','MYB','OVOL2','PAX5','PBX1','POU3F2','SOX11', 'SOX2', 'TCF12','TCF3','TCF4','NEUROD1']
    lower_square = [i for i in nodes if i not in upper_square]

    upper_square.remove('NEUROD1')
    upper_square.append('NEUROD1')

    top = upper_square + lower_square

    Influ("OUTPUT", top, nodes)        
