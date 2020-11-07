import os, sys
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import pearsonr
from scipy.stats import gaussian_kde
from misc_funcs import *
from Influ.influence import Influ_f3
from JSD import compute_JSD
from correlation import corre

n_top = 33
nodes,intermat = Interaction('sclcnetwork', 'Ising')

upper_square = ['ASCL1', 'ATF2', 'CBFA2T2', 'CEBPD','ELF3','ETS2','FOXA1','FOXA2','FLI1','INSM1','KDM5B','LEF1','MYB','OVOL2','PAX5','PBX1','POU3F2','SOX11', 'SOX2', 'TCF12','TCF3','TCF4','NEUROD1']
lower_square = [i for i in nodes if i not in upper_square]

upper_square.remove('NEUROD1')
upper_square.append('NEUROD1')

top = upper_square + lower_square

# The list which contains 10 states in the order wanted
Order = []
Order.append(tuple([-1,-1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,-1,1,-1,1,-1,1,-1,-1,-1,-1,1,1,-1,-1,-1,-1,-1,1,1,1]))
Order.append(tuple([1,1,-1,1,1,1,1,1,1,1,1,1,-1,1,-1,1,-1,1,-1,1,1,1,1,-1,-1,1,1,1,1,1,-1,-1,-1]))
Order.append(tuple([1,1,-1,1,1,1,1,1,1,1,1,1,-1,1,-1,1,-1,-1,-1,1,1,1,1,-1,-1,1,1,1,1,1,-1,-1,-1]))
Order.append(tuple([-1,-1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,-1,1,-1,1,1,1,-1,-1,-1,-1,1,1,-1,-1,-1,-1,-1,1,1,1]))

# RACIPE Correlation data
with open('RACIPE' + '/' + 'racipe_corre.data','rb') as f:
    racipe = pickle.load(f)

for run_no in range(1,2):
    indices = list(os.listdir(Path("run"+str(run_no),'OUTPUT')))
    indices.remove('jsd.txt')
    indices.remove('sclcnetwork')
    DATA = pd.DataFrame(index = indices ,columns=['state1','state2','state3','state4','JSD','J','R1','p1','R2','p2'])
    for direc in indices:
        if direc == 'jsd.txt':
            continue
        with open(Path("run"+str(run_no),'OUTPUT',direc,'states.f'), 'rb') as f:
            STATES = pickle.load(f)
            STATES = STATES.astype(int)

        Freq = np.zeros(len(Order))

        freq = STATES.T[-1]*100/sum(STATES.T[-1])
        STATES = list(STATES.T[:-1].T)

        for num, state in enumerate(STATES):
            if tuple(state) in Order:
                Freq[Order.index(tuple(state))] = freq[num]

        DATA.loc[direc,'state1'] = Freq[0]
        DATA.loc[direc,'state2'] = Freq[1]
        DATA.loc[direc,'state3'] = Freq[2]
        DATA.loc[direc,'state4'] = Freq[3]

        DATA.loc[direc,'JSD'] = compute_JSD(run_no,'Output_wild_type',direc)

        DATA.loc[direc,'J'] = corre(run_no,direc,top,nodes)

        up = np.triu_indices(len(top))
        low = np.tril_indices(len(top))

        with open(Path("run"+str(run_no),'OUTPUT',direc,'intermat.f'), 'rb') as f:
            intermat = pickle.load(f)

        influ = Influ_f3(top, nodes, 11, intermat)

        i_up = influ[up]
        r_up = racipe[up]

        R1, p1 = pearsonr(i_up,r_up)

        i_low = influ[low]
        r_low = racipe[low]

        R2, p2 = pearsonr(i_low,r_low)

        DATA.loc[direc,'R1'] = R1
        DATA.loc[direc,'p1'] = p1
        DATA.loc[direc,'R2'] = R2
        DATA.loc[direc,'p2'] = p2

        print(DATA.loc[direc])

    DATA.to_excel('run'+str(run_no)+"_edge_perturb.xlsx")
