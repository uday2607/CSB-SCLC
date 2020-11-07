import numpy as np
from numba import njit
import numba as nb
import random

################################################################################

@nb.jit(nopython=True, cache=True, nogil=True, fastmath=True)
def IterOneSync(inter_mat,vect,values):
  '''Iteration for one time step using Synchronous updating'''

  vect1 = vect[:]
  vect2 = inter_mat @ vect1 #Matrix of activations/inhibitions

  vect2[vect2 > 0] = int(values[0])
  vect2[vect2 < 0] = int(values[1])
  vect2[vect2 == 0] = vect1[vect2 == 0]
  #sigma Jij.Sj ><= 1 ,-1, previous vector

  return vect2

################################################################################

@nb.jit(nopython=True, cache=True, nogil=True, fastmath=True)
def IterOneAsync(inter_mat,vect,values):
    '''Iteration for one time step using Asynchronous updating'''

    vect1 = vect[:]
    index = int(inter_mat.shape[0] * random.random()) #index of the node which will get updated
    value = np.dot(inter_mat[index], vect1)   #value of activations/inhibitions

    if value > 0: #sigma Jij.Sj ><= 1 ,-1, previous vector
       vect1[index] = int(values[0])
    elif value < 0:
       vect1[index] = int(values[1])
    else:
        True

    return vect1

################################################################################
