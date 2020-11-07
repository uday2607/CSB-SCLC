import os, sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
import seaborn as sns

with open('jsd.txt','r') as f:
    lines  = f.readlines()[2:]

jsd = []
for line in lines:
    jsd.append(float(line.split('\t')[3].strip()))

num_st = []
for line in lines:
    num_st.append(float(line.split('\t')[2].strip()))

jsd = np.round(np.array(jsd)/np.log(2), 3)
lg_st = np.round(np.log10(np.array(num_st)),4)

sns.set_context("paper", font_scale=1.5)
with sns.axes_style("white"):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.hist(lg_st, bins = 50,range = [1,6.5])
    plt.xlabel('log10(Number of States)')
    plt.ylabel('Occurences')
    plt.xticks([0.5*x for x in range(2,14)])
    plt.axvline(x=1, color='r', linestyle='--')
    plt.grid(axis='y', alpha=0.75)

    plt.show()
    plt.savefig("Distr.png",format="png")
