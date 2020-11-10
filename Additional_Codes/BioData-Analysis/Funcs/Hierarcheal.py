import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
import scipy.cluster.hierarchy as hierarchy
from scipy.cluster.hierarchy import dendrogram,linkage,fcluster,cophenet
import scipy.spatial.distance as ssd
from sklearn.cluster import AgglomerativeClustering,MeanShift
from sklearn.cluster import MeanShift
import sklearn.metrics as sm
import os
from pathlib import Path
import seaborn as sns

def Hier_analysis(Data, title, folder, **kwargs):

    ## Dendogram for n nodes ##
    Nodes = kwargs['Dims']
    if Nodes == ['']:
        NODES = []
        for node in open('sclcnetwork.ids').readlines():
            NODES.append(str(node.split('\t')[0].strip()))

        Nodes = NODES

    Remove = []
    for node in Nodes:
        if not node in list(Data.index):
            Remove.append(node)

    for node in Remove:
        Nodes.remove(node)

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    data = Data.loc[Nodes]
    data = data.astype(float)
    scaled_data = preprocessing.scale(data.T)
    sns.set_context("paper", font_scale=1.5)
    hierarchy.set_link_color_palette(colors)
    dend1 = dendrogram(linkage(scaled_data,method='ward'),
                       leaf_rotation=90,color_threshold=(5))
    plt.suptitle(title+": "+"Dendogram for Choosen ({}) Nodes".format(Nodes))
    plt.savefig(Path(folder,title+"_"+"Dendogram_({})_Nodes.png".format(len(Nodes))), format='png', bbox_inches = "tight")
    plt.close()
