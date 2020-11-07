import numpy as np
import math
import tempfile
import numba as nb
import pickle
import os

''' Important functions which can be used throughout the package '''

def num2vect(num,node_num):
    '''Converts a binary number into Vector.'''

    string = format(num, 'b').zfill(node_num)
    arr = np.fromiter(string, dtype=int)
    arr = np.where(arr <= 0, -1.0, arr)
    return arr.astype(np.float32)

def col2vect(arr,node_num):

    vect_arr = []
    for num in arr:
        num = int(num)
        vect_arr.append(num2vect(num,node_num))

    return np.array(vect_arr)

################################################################################################################

@nb.jit(nopython=True, cache=True, nogil=True, fastmath=True)
def bin2num(arr):

    num = 0
    n = len(arr)
    for i in range(n):
        num = num + arr[i]*(2**(n-i-1))

    return num

def vect2num(input):
    '''Converts Vector to a binary number for easy Graph creation'''

    arr = np.copy(input).astype(np.int8)
    arr = np.where(arr < 0, 0 ,arr)
    num = bin2num(arr)
    return num

def rows2num(arr):

    array = []
    for i in arr:
        array.append(vect2num(i))

    return np.array(array)

################################################################################################################

def load_data(file_name): #You may dump multiple objects to pickle file using 'ab' (append binary) attribute in the above function
    #This function can retrive multiple objects dumped to a single file
    with open(file_name, "rb") as f:
        while True:
            try:
                yield pickle.load(f) #if there's a single object dumped you can retrive it using pickle.load(file)
            except EOFError: #Once all the appended data is retrived, we get no data encounter error. So using try except we can break once we get all the data
                break

def pickle_file(arr, file_name):

    with open(file_name, 'wb') as file: #Always open file with 'wb' attributes when pickling. (wb -> write binary)
        pickle.dump(arr, file, protocol=pickle.HIGHEST_PROTOCOL) #HIGHEST_PROTOCOL -> fast and less memory

################################################################################################################
@nb.jit(parallel=True, nopython = True, nogil = True, fastmath = True)
def parallel_nonzero_count(arr):
    flattened = arr.ravel()
    sum_ = 0
    for i in range(flattened.size):
        sum_ += flattened[i] != 0
    return sum_

@nb.jit(nopython=True, cache=True, nogil=True, fastmath=True)
def frust(boolvect1,inter_mat):
    ''' Calculates frustration of a vector '''

    # By calculating number of non-zero elements we can know number of edges in a network
    edges = parallel_nonzero_count(inter_mat)
    # transpose in Numpy produces the same mtrix for 1xn mtrix. So we use reshaping
    boolvect2 = boolvect1.reshape((-1, 1))
    # reshape((-1,1)) means columns to rows and single column
    frust_mat = (np.multiply((np.multiply(inter_mat,boolvect2)),boolvect1))
    # Frustration for a node = sigma JijSiSj
    result = (frust_mat < 0).sum() # Checking now many nodes are Frustrated

    return result/edges # returns relative frustration

def Frustration(vect,inter_mat):
    ''' Returns frustration using the njit function '''

    vect = num2vect(vect,inter_mat.shape[0])
    num = frust(vect,inter_mat)
    return num

################################################################################

def highestPowerof2(n):
    ''' Find the highest Power of 2 '''

    p = int(math.log(n, 2))
    return p

################################################################################

class tempmap(np.memmap):
    """
    Extension of numpy memmap to automatically map to a file stored in temporary directory.
    Usefull as a fast storage option when numpy arrays become large and
    we just want to do some quick experimental stuff.
    """
    def __new__(subtype, dtype=np.uint64, mode='w+', offset=0,
                shape=None, order='C'):
        ntf = tempfile.NamedTemporaryFile()
        self = np.memmap.__new__(subtype, ntf, dtype, mode, offset, shape, order)
        self.temp_file_obj = ntf
        return self

    def __del__(self):
        if hasattr(self,'temp_file_obj') and self.temp_file_obj is not None:
            self.temp_file_obj.close()
            del self.temp_file_obj

def np_as_tmp_map(nparray): #A useful function for creating arrays fast

    tmpmap = tempmap(dtype=nparray.dtype, mode='w+', shape=nparray.shape)
    tmpmap[...] = nparray
    return tmpmap

################################################################################
