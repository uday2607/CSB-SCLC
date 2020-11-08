import os, pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit
from scipy.stats import gaussian_kde
from Influ.influence import Influ
from misc_funcs import *

with open('RACIPE' + '/' + 'racipe_corre.data','rb') as f:
    racipe = pickle.load(f)

def Formula(top, nodes, n):

    def f(x, a, b):
        return a*x + b

    influ = Influ(top, nodes, n)

    up = np.triu_indices(len(influ))
    low = np.tril_indices(len(influ))

    ## X -> Y scatter plot #
    i_up = influ[up]
    r_up = racipe[up]

    x = r_up
    y = i_up

    xy = np.vstack([x,y])
    z = gaussian_kde(xy)(xy)
    idx = z.argsort()
    x, y, z = x[idx], y[idx], z[idx]

    popt, pcov = curve_fit(f, x, y)
    residuals = y - f(x, *popt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y-np.mean(y))**2)
    r_squared = 1 - (ss_res / ss_tot)

    sns.set_context("paper", font_scale=1.5)
    fig = plt.figure(figsize=(7,5))
    plt.scatter(x,y,c=z)
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('Kernel Density Estimate', rotation=90)
    plt.xlabel("RACIPE Correlation coeffecients")
    plt.ylabel("Influence coeffecients")
    plt.suptitle("R-square of Linear Fit: {}".format(r_squared))
    plt.savefig("xtoy_density_{}".format(n), dpi = 300)
    plt.close()

    ## Y -> X Scatter Plot#

    r_low = racipe[low]
    i_low = influ[low]

    x = r_low
    y = i_low

    xy = np.vstack([x,y])
    z = gaussian_kde(xy)(xy)
    idx = z.argsort()
    x, y, z = x[idx], y[idx], z[idx]

    popt, pcov = curve_fit(f, x, y)
    residuals = y - f(x, *popt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y-np.mean(y))**2)
    r_squared = 1 - (ss_res / ss_tot)

    sns.set_context("paper", font_scale=1.5)
    fig = plt.figure(figsize=(7,5))
    plt.scatter(x,y,c = z)
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('Kernel Density Estimate', rotation=90)
    plt.xlabel("RACIPE Correlation coeffecients")
    plt.ylabel("Influence coeffecients")
    plt.suptitle("R-square of Linear Fit: {}".format(r_squared))
    plt.savefig("ytox_density_{}".format(n), dpi = 300)
    plt.close()


if __name__ == '__main__':
    
    nodes,intermat = Interaction('sclcnetwork', 'Ising')

    upper_square = ['ASCL1', 'ATF2', 'CBFA2T2', 'CEBPD','ELF3','ETS2','FOXA1','FOXA2','FLI1','INSM1','KDM5B','LEF1','MYB','OVOL2','PAX5','PBX1','POU3F2','SOX11', 'SOX2', 'TCF12','TCF3','TCF4','NEUROD1']
    lower_square = [i for i in nodes if i not in upper_square]

    upper_square.remove('NEUROD1')
    upper_square.append('NEUROD1')

    top = upper_square + lower_square

    Formula(top, nodes, 10)
