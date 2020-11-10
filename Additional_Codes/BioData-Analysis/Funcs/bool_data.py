import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
import os
from pathlib import Path
import pickle

def num2vect(num,node_num):
    '''Converts a binary number into Vector.'''

    string = format(num, 'b').zfill(node_num)
    arr = np.fromiter(string, dtype=int)
    arr = np.where(arr <= 0, -1.0, arr)
    return arr.astype(np.float32)

def Hier_Bool(Data, title, folder, **kwargs):

    NODES = []
    for node in open('sclcnetwork.ids').readlines():
        NODES.append(str(node.split('\t')[0].strip()))
    NODES = sorted(NODES)

    Nodes = NODES
    Remove = []
    for node in Nodes:
        if not node in list(Data.index):
            Remove.append(node)

    Nodes = ['o' if node in Remove else node for node in Nodes]

    NODES = np.array(NODES)
    Nodes = np.array(Nodes)

    with open('states.f', 'rb') as f:
        states = pickle.load(f)

    STATES = []
    x_labels = []

    ii = 1
    for vect in list(states.keys()):
        STATES.append(num2vect(vect, len(NODES)))
        x_labels.append("Bool State "+str(ii))
        ii += 1

    STATES = np.array(STATES)
    STATES = (STATES.T[NODES == Nodes]).T
    Nodes = list(Nodes)
    Nodes = [node for node in Nodes if node != 'o']
    Nodes = np.array(Nodes)

    hc_labels_n = []
    y_labels = []

    data_n = Data.loc[Nodes]
    data_n = data_n.astype(float)
    scaled_data_n = preprocessing.scale(data_n.T)

    for h in range(2,10):

        hc_n = AgglomerativeClustering(n_clusters = h,affinity='euclidean',linkage='ward')
        y_n = hc_n.fit_predict(scaled_data_n)
        hc_labels_n.append(np.array(hc_n.labels_))

        labs = []
        for i in range(h):
            labs.append("Hier State "+str(i+1))
        y_labels.append(labs)

    for h in range(2,10):

        matrix = []
        for i in range(h):
            temp = []
            x = np.array(np.mean(scaled_data_n[hc_labels_n[h-2] == i], axis = 0))
            x[x > 0] = 1.0
            x[x < 0] = -1.0

            for state in STATES:
                temp.append(np.linalg.norm(x-state))

            matrix.append(temp)

        matrix = np.array(matrix)
        fig = plt.figure(figsize=(8,8))
        ax1 = fig.add_subplot(111)
        plt.imshow(matrix, cmap='seismic', interpolation='nearest')
        plt.colorbar()
        ax1.set_xticks(np.arange(len(STATES)))
        ax1.set_yticks(np.arange(h))
        ax1.set_xticklabels(x_labels,rotation=90, fontsize=10)
        ax1.set_yticklabels(y_labels[h-2],fontsize=10)
        for i in range(h):
            for j in range(len(STATES)):
                text = ax1.text(j, i, '%0.3f' % matrix[i, j], ha="center", va="center", color="black", fontsize = 7.5)
        plt.suptitle(title+": "+"Heatmap of distance of States from Hier({}) to Boolean ({}) states".format(h, len(STATES)))
        plt.savefig(Path(folder,title+"_"+"Heatmap_dis_Hier({})_to_Boolean({}).png".format(h, len(STATES))), format='png', bbox_inches = "tight")
        plt.cla()
        plt.clf()

    plt.close(fig)

def K_Bool(Data, title, folder, **kwargs):

    NODES = []
    for node in open('sclcnetwork.ids').readlines():
        NODES.append(str(node.split('\t')[0].strip()))
    NODES = sorted(NODES)

    Nodes = NODES
    Remove = []
    for node in Nodes:
        if not node in list(Data.index):
            Remove.append(node)

    Nodes = ['o' if node in Remove else node for node in Nodes]

    NODES = np.array(NODES)
    Nodes = np.array(Nodes)

    with open('states.f', 'rb') as f:
        states = pickle.load(f)

    STATES = []
    x_labels = []

    ii = 1
    for vect in list(states.keys()):
        STATES.append(num2vect(vect, len(NODES)))
        x_labels.append("Bool State "+str(ii))
        ii += 1

    STATES = np.array(STATES)
    STATES = (STATES.T[NODES == Nodes]).T
    Nodes = list(Nodes)
    Nodes = [node for node in Nodes if node != 'o']
    Nodes = np.array(Nodes)

    k_labels_n = []
    y_labels = []

    data_n = Data.loc[Nodes]
    data_n = data_n.astype(float)
    scaled_data_n = preprocessing.scale(data_n.T)

    for k in range(2,10):

        kmeans_n = KMeans(init="random",n_clusters=k,n_init=20,max_iter=300)
        x_n = kmeans_n.fit(scaled_data_n)
        k_labels_n.append(kmeans_n.labels_)

        labs = []
        for i in range(k):
            labs.append("K State "+str(i+1))
        y_labels.append(labs)

    for k in range(2,10):

        matrix = []
        for i in range(k):
            temp = []
            x = np.array(np.mean(scaled_data_n[k_labels_n[k-2] == i], axis = 0))
            x[x > 0] = 1.0
            x[x < 0] = -1.0

            for state in STATES:
                temp.append(np.linalg.norm(x-state))

            matrix.append(temp)

        matrix = np.array(matrix)
        fig = plt.figure(figsize=(8,8))
        ax1 = fig.add_subplot(111)
        plt.imshow(matrix, cmap='seismic', interpolation='nearest')
        plt.colorbar()
        ax1.set_xticks(np.arange(len(STATES)))
        ax1.set_yticks(np.arange(k))
        ax1.set_xticklabels(x_labels,rotation=90, fontsize=10)
        ax1.set_yticklabels(y_labels[k-2],fontsize=10)
        for i in range(k):
            for j in range(len(STATES)):
                text = ax1.text(j, i, '%0.3f' % matrix[i, j], ha="center", va="center", color="black", fontsize = 7.5)
        plt.suptitle(title+": "+"Heatmap of distance of States from K({}) to Boolean ({}) states".format(k, len(STATES)))
        plt.savefig(Path(folder,title+"_"+"Heatmap_dis_K({})_to_Boolean({}).png".format(k, len(STATES))), format='png', bbox_inches = "tight")
        plt.cla()
        plt.clf()

    plt.close(fig)
