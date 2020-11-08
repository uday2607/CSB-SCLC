import numpy as np
import scipy.stats
from numpy.linalg import norm
from scipy.spatial import distance
import os
import pickle
import pandas as pd
import numba as nb

from Methods.Tools.Funcs import *

def add_freq(States, freq):

    states = States.copy()
    states = np.array(states)
    freq = np.array(freq)

    temp = np.vstack((states, freq)).T
    df = pd.DataFrame(temp, columns = ['states', 'freq'])
    df = df.groupby(['states'], as_index = False)['freq'].sum()
    df.columns = ['states', 'freq']
    df.sort_values('freq')

    return list(df['states']),  list(df['freq'])

def JSD(p, q):
    """
    method to compute the Jenson-Shannon Distance
    between two probability distributions
    """

    # calculate m
    m = (p + q) / 2

    # compute Jensen Shannon Divergence
    divergence = distance.jensenshannon(p,q, base = 2) ** 2

    # compute the Jensen Shannon Distance
    #distance = np.sqrt(divergence)

    return divergence

def compute_JSD(Wfile, Mfile, run_no):

    FreqW = [] #Contains frequency of wild type States
    FreqM = [] #Contains frequency of mutated type states

    with open(os.path.join('OUTPUT',Wfile,'states.f'),'rb') as f:
        Wstates = pickle.load(f)
        W_states = rows2num(Wstates[:,:-1])
        W_freq = Wstates[:,-1]

    with open(os.path.join('OUTPUT',Mfile,'states.f'),'rb') as f:
        Mstates = pickle.load(f)
        M_states = rows2num(Mstates[:,:-1])
        M_freq = Mstates[:,-1]

    del Wstates, Mstates

    W_states, W_freq = add_freq(W_states, W_freq)
    M_states, M_freq = add_freq(M_states, M_freq)

    FreqW = []
    FreqM = []

    states = list(set(W_states) & set(M_states))
    if len(states) == 0:
        FreqW = np.array(W_freq + [0]*len(M_freq))
        FreqM = np.array([0]*len(W_freq) + M_freq)
    else:
        for state in states:
            FreqW.append(W_freq[W_states.index(state)])
            FreqM.append(M_freq[M_states.index(state)])

        FreqW_nu = list(set(W_freq)-set(FreqW))
        FreqM_nu = list(set(M_freq)-set(FreqM))
        MM = len(FreqM_nu)
        WW = len(FreqW_nu)
        FreqW = np.array(FreqW + FreqW_nu + [0]*(MM))
        FreqM = np.array(FreqM + [0]*(WW) + FreqM_nu)

    if set(W_states).issubset(set(M_states)) or set(W_states).issuperset(set(M_states)):
        Boolean = "True"
    else:
        Boolean = "False"

    jsd = JSD(FreqW, FreqM)
    print(jsd)

    f = open(os.path.join("OUTPUT",'jsd.txt'),'a')
    f.write(str(run_no) + "\t" + str(len(W_states)) + "\t" + str(len(M_states)) + "\t" + str(jsd) + "\t" + Boolean + "\n")
    f.close()

