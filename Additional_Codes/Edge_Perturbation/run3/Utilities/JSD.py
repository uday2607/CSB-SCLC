import numpy as np
import scipy.stats
from numpy.linalg import norm
import os
import pickle
import pandas as pd

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


def JSD(P, Q):
    """
    method to compute the Jenson-Shannon Distance
    between two probability distributions
    """

    # convert the vectors into numpy arrays in case that they aren't
    p = np.array(P)
    q = np.array(Q)

    # calculate m
    m = (p + q) / 2

    # compute Jensen Shannon Divergence
    divergence = (scipy.stats.entropy(p, m) + scipy.stats.entropy(q, m)) / 2

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

    states = list(set().union(W_states,M_states))
    for state in states:
        if state in W_states:
            FreqW.append(W_freq[W_states.index(state)]) #Appending the frequency
        else:
            FreqW.append(0)  #If state is not found then it is technically zero

        if state in M_states:
            FreqM.append(M_freq[M_states.index(state)]) #Appending the frequency
        else:
            FreqM.append(0)  #If state is not found then it is technically zero

    if set(W_states).issubset(set(M_states)) or set(W_states).issuperset(set(M_states)):
        Boolean = "True"
    else:
        Boolean = "False"

    jsd = JSD(FreqW, FreqM)

    f = open(os.path.join("OUTPUT",'jsd.txt'),'a')
    f.write(str(run_no) + "\t" + str(len(W_states)) + "\t" + str(len(M_states)) + "\t" + str(jsd) + "\t" + Boolean + "\n")
    f.close()
