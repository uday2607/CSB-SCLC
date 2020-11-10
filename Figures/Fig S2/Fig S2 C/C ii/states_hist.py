import pandas as pd
import numpy as np
import pickle
from scipy.spatial import distance
from sklearn import preprocessing
import numba as nb
import matplotlib.pyplot as plt
import scipy
import seaborn as sns

def plot(labels,list1,list2,err1,err2,label1,label2):

    x = np.arange(len(labels))  # the label locations
    width = 0.30  # the width of the bars

    sns.set_context("paper", font_scale=1.5)

    fig, ax = plt.subplots()

    # Add some text for labels, title and custom x-axis tick labels, etc.
    lns1 = ax.bar(x-width/2, np.array(list1), width, yerr = err1, error_kw = dict(lw = 5, capsize = 5, capthick = 3), label = label1)
    lns2 = ax.bar(x+width/2, np.array(list2), width, yerr = err2, color = 'coral',error_kw = dict(lw = 5, capsize = 5, capthick = 3), label = label2)
    ax.set_ylabel("Frequency")
    ax.set_xlabel('Steady States')
    #ax.set_title('Frequency of '+label1+" and "+label2+ " states")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim([0,0.35])

    lines, labels = ax.get_legend_handles_labels()
    ax.legend(lines, labels, loc=0)

    plt.savefig(label1+"_"+label2+"_"+".png", dpi=300, bbox_inches = "tight")
    plt.show()
    plt.close()

if __name__ == '__main__':

    toy2 = pd.read_csv("model2.csv")
    labels = ["S{}".format(i+1) for i in range(len(toy2['State']))]
    plot(labels,toy2['Toy_Mean'],toy2['WT_Mean'],toy2["Toy_SD"],toy2["WT_SD"],'Reduced Model 2','WT')
