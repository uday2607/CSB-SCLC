import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
import umap
import pickle, os
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering,MeanShift
import seaborn as sns

def UMAP_analysis(Data, title, folder, **kwargs):

    n_neighbors = 4
    trial = 5

    # dimensions which are to be plotted
    TADA = kwargs['Dims']
    if TADA == ['']:
        NODES = []
        for node in open('sclcnetwork.ids').readlines():
            NODES.append(str(node.split('\t')[0].strip()))
        NODES = sorted(NODES)

        TADA = NODES

    # Color labels
    Nodes = kwargs['Colors']

    Remove = []
    for node in TADA:
        if not node in list(Data.index):
            Remove.append(node)

    for node in Remove:
        TADA.remove(node)

    DATA = Data.loc[TADA]
    DATA = DATA.astype(float)
    Scaled_data = preprocessing.scale(DATA.T)

    Scaled_data = np.array(pd.DataFrame(Scaled_data,columns = TADA))
    if not os.path.exists(Path(folder,"UMAP")):
        os.mkdir(Path(folder,"UMAP"))
    
    DATA = Data.loc[Nodes]
    DATA = DATA.astype(float)

    label_data = preprocessing.scale(DATA.T)
    label_data = pd.DataFrame(label_data,columns = Nodes)

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    for j in range(0,trial):
        print("starting trial:",j+1)
        reducer = umap.UMAP(n_neighbors = n_neighbors, n_epochs = 1000)
        embedding = reducer.fit_transform(Scaled_data)

        for node in Nodes:
            sns.set_context("paper", font_scale=1.5)
            plt.scatter(embedding[:, 0],embedding[:, 1],c = label_data[node],cmap = 'RdYlGn',s=10)
            # plt.title(title+': UMAP_{}_Nodes={}_Exp:{}_n={}'.format(str(j),TADA,node,str(n_neighbors)))
            plt.title('{}'.format(node))
            plt.colorbar()
            plt.savefig(Path(folder,"UMAP",title+'_UMAP_{}_Nodes={}_Exp{}_n={}.png'.format(str(j),str(len(TADA)),node,str(n_neighbors))), format='png')
            plt.close()
