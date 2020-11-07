import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
import scipy.stats as stats
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
import os
from pathlib import Path

def create_proxy(label):
    line = matplotlib.lines.Line2D([0], [0], linestyle='none', mfc='black',
                mec='none', marker=r'$\mathregular{{{}}}$'.format(label), markersize = 30)
    return line

def Hier_significance(Data, title, folder,**kwargs):

    out = 'Significance_test'
    if not os.path.exists(Path(folder,out)):
        os.mkdir(Path(folder, out))

    Nodes = ['ASCL1','NEUROD1','POU2F3','ATOH1','YAP1']
    Remove = []
    for node in Nodes:
        if not node in list(Data.index):
            Remove.append(node)

    for node in Remove:
        Nodes.remove(node)

    data_n = Data.loc[Nodes]
    data_n = data_n.astype(float)
    scaled_data_n = preprocessing.scale(data_n.T)

    hc_labels_n = []

    Ax = [0 for _ in range(len(Nodes))]
    Plots = []
    Plots.append([(0,0),(0,2),(1,0),(1,2)])
    Plots.append([(0,0),(0,2),(0,4),(1,1),(1,3)])

    for h in range(2,10):

        hc_n = AgglomerativeClustering(n_clusters = h,affinity='euclidean',linkage='ward')
        y_n = hc_n.fit_predict(scaled_data_n)
        hc_labels_n.append(np.array(hc_n.labels_))

    figure = plt.gcf()  # get current figure
    figure.set_size_inches(32, 18)

    for h in range(2,10):

        y = []
        y_std = []
        ticks = []
        tick_labels = []
        y_data = []

        for i in range(h):

            ticks.append(i)
            tick_labels.append(str(np.sum(hc_labels_n[h-2] == i)))
            y.append(np.array(np.mean(scaled_data_n[hc_labels_n[h-2] == i], axis = 0)))
            y_std.append(np.array(np.std(scaled_data_n[hc_labels_n[h-2] == i], axis = 0)))
            y_data.append(scaled_data_n[hc_labels_n[h-2] == i])

        y = np.array(y)
        y_std = np.array(y_std)
        y_data = np.array(y_data, dtype='object')

        if len(Nodes) == 4:
            for _ in range(len(Nodes)):
                Ax[_] = plt.subplot2grid(shape=(2,6), loc=Plots[0][_], colspan=2)

        elif len(Nodes) == 5:
            for _ in range(len(Nodes)):
                Ax[_] = plt.subplot2grid(shape=(2,6), loc=Plots[1][_], colspan=2)
        else:
            return

        for ii, node in enumerate(Nodes):

            mean = np.array([np.abs(y.T[ii])])
            std = y_std.T[ii]

            arr = np.repeat(mean,h,axis = 0)

            Diff = np.abs(arr - arr.T)
            Div = np.abs(arr/arr.T)
            Div[Div < 1] = 1/Div[Div < 1]

            im = Ax[ii].imshow(Diff, cmap='seismic', interpolation='nearest')
            figure.colorbar(im, ax = Ax[ii])
            Ax[ii].set_xticks(ticks)
            Ax[ii].set_yticks(ticks)
            Ax[ii].set_xticklabels(tick_labels,rotation = 90,fontsize=20)
            Ax[ii].set_yticklabels(tick_labels,fontsize=20)
            for i in range(h):
                for j in range(h):
                    data_corr,data_p = stats.ttest_ind(y_data[i].T[ii], y_data[j].T[ii], equal_var = False)
                    if data_p < 0.001:
                        text = Ax[ii].text(j, i, '\n\n***\n\n', ha="left", va="center", color="w", fontsize = 20)
                    elif data_p < 0.005:
                        text = Ax[ii].text(j, i, '\n\n**\n\n', ha="left", va="center", color="w", fontsize = 20)
                    elif data_p < 0.05:
                        text = Ax[ii].text(j, i, '\n\n*\n\n', ha="left", va="center", color="w", fontsize = 20)

                    if Div[i,j] > 1.5:
                        text = Ax[ii].text(j, i, '\n\n+\n\n', ha="right", va="center", color="w", fontsize = 20)
                    elif Div[i,j] > 2:
                        text = Ax[ii].text(j, i, '\n\n++\n\n', ha="right", va="center", color="w", fontsize = 20)
                    elif Div[i,j] > 2.5:
                        text = Ax[ii].text(j, i, '\n\n+++\n\n', ha="right", va="center", color="w", fontsize = 20)

            Ax[ii].set_title(str(node), fontsize = 26)

        LABELS = ['+','*']
        figure.legend([create_proxy(item) for item in LABELS], ['bio','stat'], fontsize = 45)
        plt.suptitle(title+": "+"Difference between mean expression levels of Choosen ({}) nodes, Hier : {}".format(len(Nodes),h), fontsize = 30)
        plt.savefig(Path(folder,out,title+"_"+"Difference between mean expression levels of Choosen ({}) nodes, Hier : {}".format(len(Nodes),h)))

        for ii, node in enumerate(Nodes):
            Ax[ii].clear()

    plt.close(figure)


def K_significance(Data, title, folder, **kwargs):

    out = 'Significance_test'
    if not os.path.exists(Path(folder,out)):
        os.mkdir(Path(folder, out))

    Nodes = ['ASCL1','NEUROD1','POU2F3','ATOH1','YAP1']
    Remove = []
    for node in Nodes:
        if not node in list(Data.index):
            Remove.append(node)

    for node in Remove:
        Nodes.remove(node)

    data_n = Data.loc[Nodes]
    data_n = data_n.astype(float)
    scaled_data_n = preprocessing.scale(data_n.T)

    k_labels_n = []

    Ax = [0 for _ in range(len(Nodes))]
    Plots = []
    Plots.append([(0,0),(0,2),(1,0),(1,2)])
    Plots.append([(0,0),(0,2),(0,4),(1,1),(1,3)])

    for k in range(2,10):

        kmeans_n = KMeans(init="random",n_clusters=k,n_init=20,max_iter=300)
        x_n = kmeans_n.fit(scaled_data_n)
        k_labels_n.append(kmeans_n.labels_)

    figure = plt.gcf()  # get current figure
    figure.set_size_inches(32, 18)

    for k in range(2,10):

        y = []
        y_std = []
        ticks = []
        tick_labels = []
        y_data = []

        for i in range(k):

            ticks.append(i)
            tick_labels.append(str(np.sum(k_labels_n[k-2] == i)))
            y.append(np.array(np.mean(scaled_data_n[k_labels_n[k-2] == i], axis = 0)))
            y_std.append(np.array(np.std(scaled_data_n[k_labels_n[k-2] == i], axis = 0)))
            y_data.append(scaled_data_n[k_labels_n[k-2] == i])

        y = np.array(y)
        y_std = np.array(y_std)
        y_data = np.array(y_data, dtype='object')

        if len(Nodes) == 4:
            for _ in range(len(Nodes)):
                Ax[_] = plt.subplot2grid(shape=(2,6), loc=Plots[0][_], colspan=2)

        elif len(Nodes) == 5:
            for _ in range(len(Nodes)):
                Ax[_] = plt.subplot2grid(shape=(2,6), loc=Plots[1][_], colspan=2)

        else:
            return

        for ii, node in enumerate(Nodes):

            mean = np.array([np.abs(y.T[ii])])
            std = y_std.T[ii]

            arr = np.repeat(mean,k,axis = 0)

            Diff = np.abs(arr - arr.T)
            Div = np.abs(arr/arr.T)
            Div[Div < 1] = 1/Div[Div < 1]

            im = Ax[ii].imshow(Diff, cmap='seismic', interpolation='nearest')
            figure.colorbar(im, ax = Ax[ii])
            Ax[ii].set_xticks(ticks)
            Ax[ii].set_yticks(ticks)
            Ax[ii].set_xticklabels(tick_labels, rotation = 90,fontsize=20)
            Ax[ii].set_yticklabels(tick_labels,fontsize=20)
            for i in range(k):
                for j in range(k):
                    data_corr,data_p = stats.ttest_ind(y_data[i].T[ii], y_data[j].T[ii], equal_var = False)
                    if data_p < 0.001:
                        text = Ax[ii].text(j, i, '\n\n***\n\n', ha="left", va="center", color="w", fontsize = 20)
                    elif data_p < 0.005:
                        text = Ax[ii].text(j, i, '\n\n**\n\n', ha="left", va="center", color="w", fontsize = 20)
                    elif data_p < 0.05:
                        text = Ax[ii].text(j, i, '\n\n*\n\n', ha="left", va="center", color="w", fontsize = 20)

                    if Div[i,j] > 1.5:
                        text = Ax[ii].text(j, i, '\n\n+\n\n', ha="right", va="center", color="w", fontsize = 20)
                    elif Div[i,j] > 2:
                        text = Ax[ii].text(j, i, '\n\n++\n\n', ha="right", va="center", color="w", fontsize = 20)
                    elif Div[i,j] > 2.5:
                        text = Ax[ii].text(j, i, '\n\n+++\n\n', ha="right", va="center", color="w", fontsize = 20)
            Ax[ii].set_title(str(node), fontsize = 26)

        LABELS = ['+','*']
        figure.legend([create_proxy(item) for item in LABELS], ['bio','stat'], fontsize = 45)
        plt.suptitle(title+": "+"Difference between mean expression levels of Choosen ({}) nodes, K : {}".format(len(Nodes),k),fontsize = 30)
        plt.savefig(Path(folder,out,title+"_"+"Difference between mean expression levels of Choosen ({}) nodes, K : {}".format(len(Nodes),k)))

        for ii, node in enumerate(Nodes):
            Ax[ii].clear()


    plt.close(figure)
