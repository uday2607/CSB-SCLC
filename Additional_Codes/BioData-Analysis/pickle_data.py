import pickle
import pandas as pd
import os
from pathlib import Path

def Pickle_Data(Data, title, folder):

    if not os.path.exists("Pickle_files"):
        os.mkdir("Pickle_files")

    # 33 nodes #
    Nodes = []
    for node in open('sclcnetwork.ids').readlines():
        Nodes.append(str(node.split('\t')[0].strip()))
    Nodes = sorted(Nodes)

    Remove = []
    for node in Nodes:
        if not node in list(Data.index):
            Remove.append(node)

    for node in Remove:
        Nodes.remove(node)

    data = Data.loc[Nodes]
    data = data.astype(float)
    with open(Path(folder,'33_nodes.data'),'wb') as f:
        pickle.dump(data, f)
    with open(Path("Pickle_files",folder+'_33_nodes.data'),'wb') as f:
        pickle.dump(data, f)


    # 5 nodes #
    Nodes = ['ASCL1','NEUROD1','POU2F3','ATOH1','YAP1']

    Remove = []
    for node in Nodes:
        if not node in list(Data.index):
            Remove.append(node)

    for node in Remove:
        Nodes.remove(node)

    data = Data.loc[Nodes]
    data = data.astype(float)
    with open(Path(folder,'5_nodes.data'),'wb') as f:
        pickle.dump(data, f)
    with open(Path("Pickle_files",folder+'_5_nodes.data'),'wb') as f:
        pickle.dump(data, f)

    # All nodes #
    data = Data
    data = data.astype(float)
    with open(Path(folder,'All_nodes.data'),'wb') as f:
        pickle.dump(data, f)
    with open(Path("Pickle_files",folder+'_All_nodes.data'),'wb') as f:
        pickle.dump(data, f)
