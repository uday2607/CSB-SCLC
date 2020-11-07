import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt
import scipy.stats as stats
import numba as nb
from scipy.special import betainc
import os, pickle
from pathlib import Path

def PCA_analysis(Data,title,folder,**kwargs):

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
        return num+1

    out = "PCA"
    if not os.path.exists(Path(folder,out)):
        os.mkdir(Path(folder,out))

    ## Correlation of all the 33 nodes in a custom order ##
    Nodes = []
    for node in open('sclcnetwork.ids').readlines():
        Nodes.append(str(node.split('\t')[0].strip()))
    Nodes = sorted(Nodes)

    upper_square = ['ASCL1', 'ATF2', 'CBFA2T2', 'CEBPD','ELF3','ETS2','FOXA1','FOXA2','FLI1','INSM1','KDM5B','LEF1','MYB','OVOL2','PAX5','PBX1','POU3F2','SOX11', 'SOX2', 'TCF12','TCF3','TCF4','NEUROD1']
    lower_square = [i for i in Nodes if i not in upper_square]

    Top = upper_square + lower_square

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
    data = data.reindex(index=Top)
    data = np.array(data)

    DATA, P = corrcoef(data)
    np.nan_to_num(DATA,copy = False,nan = 0)

    fig = plt.figure(figsize=(8,8))
    ax1 = fig.add_subplot(111)
    plt.imshow(DATA, cmap='seismic', interpolation='nearest')
    plt.colorbar()
    plt.clim(-1,1)
    ax1.set_xticks(np.arange(len(Top)))
    ax1.set_yticks(np.arange(len(Top)))
    ax1.set_xticklabels(Top,rotation=90, fontsize=10)
    ax1.set_yticklabels(Top,fontsize=10)
    plt.setp(ax1.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    num = metric(DATA)

    plt.suptitle("{}: Correlation Plot of Boolean Simulations | Metric J = {}".format(title,num))

    for i in range(len(Top)):
        for j in range(len(Top)):
            data_p = P[i][j]
            if data_p < 0.001:
                text = ax1.text(j, i, '***', ha="center", va="center", color="w", fontsize = 7)
            elif data_p < 0.005:
                text = ax1.text(j, i, '**', ha="center", va="center", color="w", fontsize = 7)
            elif data_p < 0.05:
                text = ax1.text(j, i, '*', ha="center", va="center", color="w", fontsize = 7)

    plt.savefig(Path(folder,title+"_"+'Correlation_All_Nodes.png'))
