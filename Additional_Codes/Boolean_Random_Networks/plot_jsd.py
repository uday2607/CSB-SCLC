import os, sys
import numpy as np
import matplotlib.pyplot as plt

with open('jsd.txt','r') as f:
    lines  = f.readlines()[2:]

jsd = []
for line in lines:
    jsd.append(float(line.split('\t')[3].strip()))

jsd = np.round(np.array(jsd)/np.log(2), 3)
plt.hist(jsd, bins = [0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1])
plt.xlabel('JSD Vals', fontsize = 10)
plt.ylabel('No of occurences', fontsize = 10)
plt.xticks([0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1])
plt.grid(axis='y', alpha=0.75)
plt.suptitle("Occurences of JSD values (Wild type states = 10)", fontsize = 14)
plt.show()
plt.close()

with open('corre.txt','r') as f:
    lines  = f.readlines()[1:]

corre = []
for line in lines:
    corre.append(float(line.split('\t')[2].strip()))

hist, bin_edges = np.histogram(corre, density=True)
plt.hist(corre, bins = bin_edges)
plt.xlabel('Metric', fontsize = 10)
plt.ylabel('No of occurences', fontsize = 10)
plt.grid(axis='y', alpha=0.75)
plt.suptitle("Occurences of Metric values (Wild type metric value = 1024)", fontsize = 14)
plt.show()
