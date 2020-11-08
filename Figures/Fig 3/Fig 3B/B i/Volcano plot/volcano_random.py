import os, pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns
from scipy.stats import pearsonr
from scipy.stats import gaussian_kde
from Influ.influence import Influ
from misc_funcs import *

with open('RACIPE' + '/' + 'racipe_corre.data','rb') as f:
    racipe = pickle.load(f)


def Formula(top, nodes):

    up = np.triu_indices(len(top))
    low = np.tril_indices(len(top))

    p_vals, R_vals = [], []
    C = [] #Colors to differentiate between R1 and R2

    legend_elements = [Line2D([0], [0], marker='o', color='b', label='R1',
                          markerfacecolor='b', markersize=5),
                       Line2D([0], [0], marker='o', color='orange', label='R2',
                          markerfacecolor='orange', markersize=5)]

    with open('intermat.f', 'rb') as f:
        intermat = pickle.load(f)

    influ = Influ(top, nodes, 11, intermat)

    i_up = influ[up]
    r_up = racipe[up]

    R, p = pearsonr(i_up,r_up)

    R_vals.append(R)
    p_vals.append(-np.log10(p+10**(-30)))
    C.append('b')

    i_low = influ[low]
    r_low = racipe[low]

    R, p = pearsonr(i_low,r_low)

    R_vals.append(R)
    p_vals.append(-np.log10(p+10**(-30)))
    C.append('orange')

    for i in range(1,1001):

        with open(Path('Random_network_intermat','intermat_{}.f'.format(i)), 'rb') as f:
            intermat = pickle.load(f)

        influ = Influ(top, nodes, 11, intermat)

        i_up = influ[up]
        r_up = racipe[up]

        R, p = pearsonr(i_up,r_up)

        R_vals.append(R)
        p_vals.append(-np.log10(p+10**(-30)))
        C.append('b')

        i_low = influ[low]
        r_low = racipe[low]

        R, p = pearsonr(i_low,r_low)

        R_vals.append(R)
        p_vals.append(-np.log10(p+10**(-30)))
        C.append('orange')

    ## R and p scatter plot #

    sns.set_context("paper", font_scale=1.5)
    plt.scatter(R_vals, p_vals, c = C, s = 5)
    plt.ylim(-2,40)
    plt.axhline(y=-np.log10(0.05),ls='--')
    plt.xlabel("R values")
    plt.ylabel("-log10(p values)")
    plt.suptitle("R vs p volcano")
    plt.legend(handles=legend_elements, loc='upper left')
    plt.savefig("Rvsp", dpi = 300)
    plt.close()

if __name__ == '__main__':

    nodes,intermat = Interaction('sclcnetwork', 'Ising')

    upper_square = ['ASCL1', 'ATF2', 'CBFA2T2', 'CEBPD','ELF3','ETS2','FOXA1','FOXA2','FLI1','INSM1','KDM5B','LEF1','MYB','OVOL2','PAX5','PBX1','POU3F2','SOX11', 'SOX2', 'TCF12','TCF3','TCF4','NEUROD1']
    lower_square = [i for i in nodes if i not in upper_square]

    upper_square.remove('NEUROD1')
    upper_square.append('NEUROD1')

    top = upper_square + lower_square

    Formula(top, nodes)
