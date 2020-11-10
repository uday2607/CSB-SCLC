import os, pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit
from scipy.stats import gaussian_kde
from Influ.influence import Influ
from misc_funcs import *

with open('ccle' + '/' + 'ccle_corre.data','rb') as f:
    ccle = pickle.load(f)

def Formula(top, nodes):

    up = np.triu_indices(len(top))
    low = np.tril_indices(len(top))

    x_up, x_low = [], []
    y_up, y_low = [], []

    for n in range(3,21):

        influ = Influ(top, nodes, n)

        i_up = influ[up]
        r_up = ccle[up]

        y_up.append(pearsonr(i_up,r_up)[0])
        x_up.append(n-1)

        i_low = influ[low]
        r_low = ccle[low]

        y_low.append(pearsonr(i_low,r_low)[0])
        x_low.append(n-1)

        if n == 10:
            print(pearsonr(i_up,r_up)[0])
            print(pearsonr(i_low,r_low)[0])

    x = list(x_up) + list(x_low)
    y = list(y_up) + list(y_low)
    classes = ['R1']*len(x_up) + ['R2']*len(x_low)

    sns.set_context("paper", font_scale=1.5)
    plt.figure(figsize=(8,5))
    sns.scatterplot(x=x, y=y, hue=classes, s = 35)
    plt.xticks(np.arange(2,20))
    plt.xlabel("Path length")
    plt.ylabel("R of Wild-type")
    plt.suptitle("R vs path length")
    plt.savefig("R_CCLE", dpi = 300, bbox_inches = 'tight')
    plt.close()


if __name__ == '__main__':

    nodes,intermat = Interaction('sclcnetwork', 'Ising')

    upper_square = ['ASCL1', 'ATF2', 'CBFA2T2', 'CEBPD','ELF3','ETS2','FOXA1','FOXA2','FLI1','INSM1','KDM5B','LEF1','MYB','OVOL2','PAX5','PBX1','POU3F2','SOX11', 'SOX2', 'TCF12','TCF3','TCF4','NEUROD1']
    lower_square = [i for i in nodes if i not in upper_square]

    upper_square.remove('NEUROD1')
    upper_square.append('NEUROD1')

    top = upper_square + lower_square

    Formula(top, nodes)
