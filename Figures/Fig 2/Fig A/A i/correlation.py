import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.special import betainc
import os, pickle
from pathlib import Path
import numba as nb
import seaborn as sns
from misc_funcs import *

def corre():

    STATES = pickle.load(open(Path('states1.f'), 'rb'))
    nodes, intermat = Interaction('sclcnetwork','Ising')

    tada = ['ASCL1', 'ATF2', 'CBFA2T2', 'CEBPD','ELF3','ETS2','FOXA1','FOXA2','FLI1','INSM1','KDM5B','LEF1','MYB','OVOL2','PAX5','PBX1','POU3F2','SOX11', 'SOX2', 'TCF12','TCF3','TCF4','NEUROD1']
    ting = [i for i in nodes if i not in tada]
    top = tada+ting

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

    DATA, P = corrcoef(np.array(data))

    np.nan_to_num(DATA,copy = False,nan = 0)

    corr_df = pd.DataFrame(data = np.array(DATA))
    df_lt = corr_df.where(np.tril(np.ones(corr_df.shape)).astype(np.bool))
    sns.set(font_scale=6)
    with sns.axes_style("white"):
        fig, ax = plt.subplots(figsize=(50,50))
        hmap=sns.heatmap(df_lt,cmap="seismic",square = True,linewidths=.3,clim=[-1,1],xticklabels=False)
        ax.set_yticklabels(range(1,34),rotation=360)
        hmap.figure.savefig("corr.png",format='png')
        plt.close()

if __name__ == '__main__':
    corre()
