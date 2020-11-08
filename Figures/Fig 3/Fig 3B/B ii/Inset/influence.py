import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt
import scipy.stats as stats
import os
from pathlib import Path
import pickle
from misc_funcs import *

def Influ(top, nodes, n):

    intermat = pickle.load(open('intermat.f', 'rb'))
    N = float(np.count_nonzero(intermat))
    inf = intermat.copy()
    M_max = intermat.copy()
    M_max[M_max != 0] = 1.0
    for i in range(2,n):
        a = np.linalg.matrix_power(intermat, i).astype(float)
        b = np.linalg.matrix_power(M_max, i).astype(float)
        inf = inf + np.divide(a, b, out=np.zeros_like(a), where=b!=0)

    inf = inf/n

    data = pd.DataFrame(data=inf,index=nodes,columns=nodes)
    data = data.loc[top,top]
    inf = np.array(data)

    return inf
