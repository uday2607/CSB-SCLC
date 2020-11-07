import os, sys
import numpy as np
import matplotlib.pyplot as plt

with open('jsd.txt','r') as f:
    lines  = f.readlines()[2:]

jsd = []
for line in lines:
    jsd.append(float(line.split('\t')[3].strip()))

plt.hist(jsd, bins = [0.1,0.2,0.3,0.4,0.5,0.6,0.7])
plt.xlabel('JSD Vals', fontsize = 10)
plt.ylabel('No of occurences', fontsize = 10)
plt.xticks([0.1,0.2,0.3,0.4,0.5,0.6,0.7])
plt.grid(axis='y', alpha=0.75)
plt.suptitle("Occurences of JSD values", fontsize = 14)
plt.show()
