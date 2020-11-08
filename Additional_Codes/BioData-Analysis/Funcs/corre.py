import pandas as pd
import numpy as np
import numba as nb
import matplotlib.pyplot as plt
from scipy.special import betainc
import os, pickle
from pathlib import Path
import seaborn as sns

def Correlation(Data,title,folder,**kwargs):

    if not os.path.exists(Path(folder)):
        os.mkdir(Path(folder))

    ## PCA of 33 nodes of SCLC ##
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
        with open(folder+'/'+'Nodes_not_found.txt','w') as f:
            f.write("The nodes of SCLC which are not found in dataset are \n\n")
            for node in Remove:
                f.write(node+'\n')

    Data = Data.loc[Nodes]
    Data = np.array(Data.astype('float64'))

    data = pd.DataFrame(data=Data,index=Nodes,columns=['run_'+str(i) for i in range(Data.shape[1])])
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
    np.nan_to_num(DATA,copy = False,nan = 0)

    corr_df = pd.DataFrame(data = np.array(DATA))
    df_lt = corr_df.where(np.tril(np.ones(corr_df.shape)).astype(np.bool))
    sns.set(font_scale=6)
    with sns.axes_style("white"):
        fig, ax = plt.subplots(figsize=(50,50))
        hmap=sns.heatmap(df_lt,cmap="seismic",square = True,linewidths=.3,clim=[-1,1],xticklabels=False)
        ax.set_yticklabels(range(1,34),rotation=360)
        hmap.figure.savefig(Path(folder,"{}_corr.png".format(title)),format='png')
        plt.close()
