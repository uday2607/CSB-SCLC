import os, pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
from scipy.stats import gaussian_kde
from influence import Influ
from misc_funcs import *

with open('ccle' + '/' + 'ccle_corre.data','rb') as f:
    ccle = pickle.load(f)

def Formula(top, nodes):

    up = np.triu_indices(len(top))
    low = np.tril_indices(len(top))

    y_up, y_low = [], []

    for i in range(1,1001):

        with open(Path('Random_network_intermat','intermat_{}.f'.format(i)), 'rb') as f:
            intermat = pickle.load(f)

        influ = Influ(top, nodes, 11, intermat)

        i_up = influ[up]
        r_up = ccle[up]

        y_up.append(pearsonr(i_up,r_up)[0])

        i_low = influ[low]
        r_low = ccle[low]

        y_low.append(pearsonr(i_low,r_low)[0])

    sns.set_context("paper", font_scale=1.5)
    with sns.axes_style("white"):
        plt.hist(y_up, bins = 20, alpha = 0.5, label = "R1")
        plt.hist(y_low, bins = 20, alpha = 0.5, label  = "R2")
        plt.xlabel("Metric R")
        plt.ylabel("Occurences")
        plt.grid(axis='y', alpha=0.75)
        plt.legend()
        plt.suptitle("R (Random Networks, CCLE)")
        plt.savefig("R_CCLE", dpi = 300)
        plt.close()

if __name__ == '__main__':

    nodes,intermat = Interaction('sclcnetwork', 'Ising')

    upper_square = ['ASCL1', 'ATF2', 'CBFA2T2', 'CEBPD','ELF3','ETS2','FOXA1','FOXA2','FLI1','INSM1','KDM5B','LEF1','MYB','OVOL2','PAX5','PBX1','POU3F2','SOX11', 'SOX2', 'TCF12','TCF3','TCF4','NEUROD1']
    lower_square = [i for i in nodes if i not in upper_square]

    upper_square.remove('NEUROD1')
    upper_square.append('NEUROD1')

    top = upper_square + lower_square

    Formula(top, nodes)
