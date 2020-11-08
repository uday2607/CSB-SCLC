import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

with open("corre.txt",'r') as f:
    lines = f.readlines()

corre = []
for line in lines:
    corre.append(float(line.split('\t')[2].strip()))

corre = np.array(corre)
corre = (corre - 33)/2

CCLE = pd.read_excel("CCLE_discrete_J.xlsx",index_col = 0)
GSM73160 = pd.read_excel("73160_discrete_J.xlsx",index_col = 0)

sns.set_context("paper", font_scale=1.5)
with sns.axes_style("white"):
    plt.hist(corre, bins = 50, density = False)
    plt.axvline(496,c='r',ls='-')
    plt.axvline(float(CCLE[1]),c='green',ls='--')
    plt.axvline(float(GSM73160[1]),c='black',ls='--')
    plt.axvline(float(CCLE[2]),c='green',ls='-.')
    plt.axvline(float(GSM73160[2]),c='black',ls='-.')
    plt.xlabel('J Metric')
    plt.ylabel('Occurences')
    plt.grid(axis='y', alpha=0.75)
    plt.suptitle("Occurences of Metric values (Continuous to Discrete)")
    plt.savefig("conti_to_dis.png",dpi = 300, bbox_inches = 'tight')
