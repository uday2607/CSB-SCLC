import sys, os, time, gc
from Utilities.RandNetworkFiles import GenRandNetworks
from Utilities.JSD import compute_JSD
import bool
from correlation import corre
from random_correlation import random_corre
from influence import Influ
from misc_funcs import Interaction
import pandas as pd
import numpy as np

start_time = time.time()

with open("bool.in") as f:
    network = f.readline().split('=')[1].strip()

nodes,intermat = Interaction(network, 'Ising')
tada = ['ASCL1', 'ATF2', 'CBFA2T2', 'CEBPD','ELF3','ETS2','FOXA1','FOXA2','FLI1','INSM1','KDM5B','LEF1','MYB','OVOL2','PAX5','PBX1','POU3F2','SOX11', 'SOX2', 'TCF12','TCF3','TCF4','NEUROD1']
redundant = ['ATF2','CBFA2T2','CEBPD','ELF3','FLI1','KDM5B','OVOL2','PAX5','PBX1','ZEB1','BHLHE40','ETS2','FOXA2','MITF','MYB','MYC','TCF12','TCF7L2']
ting = [i for i in nodes if i not in tada]
top = tada+ting

#GenRandNetworks(1000,network)
print("All the Random networks are generated")

if not os.path.exists("OUTPUT"):
    os.mkdir("OUTPUT")

f = open(os.path.join("OUTPUT",'jsd.txt'),'w')
f.write("Run" + "\t" + "Num W" + "\t" + "Num R" + "\t" + "JSD" + "\t" + "Same states" + "\n")
f.close()

f = open(os.path.join("OUTPUT",'corre.txt'),'w')
f.write("Run" + "\t" + "Corre W" + "\t" + "Corre R" + "\t" + "Same matrix" + "\n")
f.close()

f = open(os.path.join("OUTPUT",'influ.txt'),'w')
f.write("Run" + "\t" + "Influ W" + "\t" + "Influ R" + "\t" + "Same matrix" + "\n")
f.close()

J_vals = pd.DataFrame(index = np.arange(1001), columns = np.arange(1000))

wild_type = "Output" + "_" + network
bool.main(network,wild_type)
numb = corre(wild_type,wild_type,top,nodes,0,0)
num_i = Influ(wild_type,top,nodes,0,0)
J_vals.iloc[0] = random_corre(wild_type,top,nodes)

time_taken = time.time() - start_time
print("Time elapsed %s" %time_taken)

for i in range(1,1001):
    in_file = network + "_" + str(i)
    out_file = "Output" + "_" + network + "_" + str(i)
    print("Running %s file" %i)
    bool.main(in_file,out_file)
    compute_JSD(wild_type,out_file,i)
    corre(wild_type,out_file,top,nodes,i,numb)
    Influ(out_file,top,nodes,i,num_i)
    J_vals.iloc[i] = random_corre(out_file,top,nodes)
    time_taken = time.time()  -start_time
    print("Time elapsed %s" %time_taken)
    gc.collect()

J_vals.to_excel("Boolean_J_vals.xlsx")
print("All the analysis is done")
