import numpy as np
import scipy.stats
from numpy.linalg import norm
import os
import pickle


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

def compute_JSD(wild_type, in_file, run_no):

    file  = open(os.path.join('OUTPUT',wild_type,'states.f'), 'rb')
    W_states = pickle.load(file)
    file.close()
    file = open(os.path.join('OUTPUT',in_file,'states.f'), 'rb')
    M_states = pickle.load(file)
    file.close()

    states = list(set().union(W_states.keys(),M_states.keys()))  #Union of all the stable states
    Frequency_W = [] #Contains frequency of wild type States
    Frequency_M = [] #Contains frequency of mutated type states

    for state in states:
        if state in W_states:
            Frequency_W.append(W_states[state]) #Appending the frequency
        else:
            Frequency_W.append(0)  #If state is not found then it is technically zero

        if state in M_states:
            Frequency_M.append(M_states[state]) #Appending the frequency
        else:
            Frequency_M.append(0)  #If state is not found then it is technically zero

    if set(Frequency_W) == set(Frequency_M):
        Boolean = "True"
    else:
        Boolean = "False"

    jsd = JSD(Frequency_W, Frequency_M)

    f = open(os.path.join("OUTPUT",'jsd.txt'),'a')
    f.write(str(run_no) + "\t" + str(len(W_states)) + "\t" + str(len(M_states)) + "\t" + str(jsd) + "\t" + Boolean + "\n")
    f.close()
