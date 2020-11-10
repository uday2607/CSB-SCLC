### Comparing Boolean states frequency to RACIPE frequency ###

import numpy as np
import pickle
import numba as nb
import matplotlib.pyplot as plt
import seaborn as sns


def num2vect(num,node_num):
    '''Converts a binary number into Vector.'''

    string = format(num, 'b').zfill(node_num)
    arr = np.fromiter(string, dtype=int)
    arr = np.where(arr <= 0, -1.0, arr)
    return arr.astype(np.float32)

@nb.jit(nopython=True, cache=True, nogil=True, fastmath=True)
def bin2num(arr):

    num = 0
    n = len(arr)
    for i in range(n):
        num = num + arr[i]*(2**(n-i-1))

    return num

@nb.jit(nopython=True, cache=True, nogil=True, fastmath=True)
def vect2num(input):
    '''Converts Vector to a binary number for easy Graph creation'''

    num = bin2num(arr)
    return num

@nb.jit(nopython=True, cache=True, nogil=True, fastmath=True)
def rows2num(arr):

    array = np.zeros(len(arr))
    for i in range(len(arr)):
        array[i] = bin2num(arr[i])

    return array

def Frequency(arr):

    arr = arr/np.sum(arr) * 100

    return arr

def plot(labels,list1,list2,err1,err2,label1,label2):

    x = np.arange(len(labels))  # the label locations
    width = 0.30  # the width of the bars

    sns.set_context("paper", font_scale=1.5)

    fig, ax = plt.subplots()
    ax2 = ax.twinx()

    # Add some text for labels, title and custom x-axis tick labels, etc.
    lns1 = ax.bar(x-width/2, np.array(list1), width, yerr = err1, error_kw = dict(lw = 5, capsize = 5, capthick = 3), label = "Boolean")
    ax.set_ylabel("Boolean Frequency")
    ax.set_xlabel('Steady States')
    ax.set_title('Frequency of '+label1+" and "+label2+ " states")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim([0,33])

    lns2 = ax2.bar(x+width/2, np.array(list2), width, yerr = err2, color = 'coral',error_kw = dict(lw = 5, capsize = 5, capthick = 3), label = "RACIPE")
    ax2.set_ylabel("RACIPE Frequency")
    ax2.set_ylim([0,13])

    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc=0)

    plt.savefig(label1+"_"+label2+"_"+".png", dpi=300, bbox_inches = "tight")
    plt.show()
    plt.close()

# Unpickling Bool states
with open('states1.f','rb') as f:
    Bools = pickle.load(f).T
Bools = Bools.astype(int)
Bools[Bools == -1] = 0
Bools[-1] = Frequency(Bools[-1])
bool_states = list(rows2num(Bools[:-1].T)) # states order in All three states.f is same

del Bools

Freqs = []
Bool_Freqs = []
for i in range(1,4):
    with open('racipe_up{}.data'.format(i), 'rb') as f:
        data = pickle.load(f)
    data = data.astype(float)
    scaled_data = (preprocessing.scale(data.T))
    scaled_data[scaled_data > 0] = 1
    scaled_data[scaled_data < 0] = 0
    scaled_data = rows2num(scaled_data.astype(int))

    states, counts = np.unique(scaled_data, return_counts = True)
    counts = Frequency(counts)
    del scaled_data
    del data

    with open('states{}.f'.format(i),'rb') as f:
        Bools = pickle.load(f).T
    Bools = Bools.astype(int)
    Bools[Bools == -1] = 0
    Bool_freq_ = Frequency(Bools[-1])
    bool_state_ = rows2num(Bools[:-1].T)

    freq = []
    bool_freq = []
    States = list(states)
    for state in bool_states:
        if state in States:
            if counts[States.index(state)] > 1: #states with frequency > 1% are only taken
                freq.append(counts[States.index(state)])
                bool_freq.append(Bool_freq_[bool_states.index(state)])

    Freqs.append(freq)
    Bool_Freqs.append(bool_freq)

bool_freq = np.mean(np.array(Bool_Freqs), axis = 0)
bool_err_freq = np.std(np.array(Bool_Freqs), axis = 0, ddof = 1)
racipe_freq = np.mean(np.array(Freqs), axis = 0)
r_err_freq = np.std(np.array(Freqs), axis = 0, ddof = 1)

labels = []
for i in range(len(bool_freq)):
    labels.append('S{}'.format(i+1))
plot(labels, bool_freq, racipe_freq, bool_err_freq, r_err_freq,'Boolean', 'RACIPE')
