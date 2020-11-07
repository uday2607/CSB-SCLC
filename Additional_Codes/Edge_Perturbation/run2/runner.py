import sys, os, time, gc
from Utilities.RandNetworkFiles import GenEdgePertNetworkFiles
from Utilities.JSD import compute_JSD
import bool
from correlation import corre
from influence import Influ
from misc_funcs import Interaction

start_time = time.time()

with open("bool.in") as f:
    network = f.readline().split('=')[1].strip()

nodes,intermat = Interaction(network, 'Ising')
tada = ['ASCL1', 'ATF2', 'CBFA2T2', 'CEBPD','ELF3','ETS2','FOXA1','FOXA2','FLI1','INSM1','KDM5B','LEF1','MYB','OVOL2','PAX5','PBX1','POU3F2','SOX11', 'SOX2', 'TCF12','TCF3','TCF4','NEUROD1']
redundant = ['ATF2','CBFA2T2','CEBPD','ELF3','FLI1','KDM5B','OVOL2','PAX5','PBX1','ZEB1','BHLHE40','ETS2','FOXA2','MITF','MYB','MYC','TCF12','TCF7L2']
ting = [i for i in nodes if i not in tada]
top = tada+ting

GenEdgePertNetworkFiles(network)
print("All the Random networks are generated")

if not os.path.exists("OUTPUT"):
    os.mkdir("OUTPUT")

f = open(os.path.join("OUTPUT",'jsd.txt'),'w')
f.write("Run" + "\t" + "Num W" + "\t" + "Num R" + "\t" + "JSD" + "\t" + "Same states" + "\n")
f.close()

wild_type = "Output" + "_" + 'wild_type'
bool.main(network,wild_type)

time_taken = time.time() - start_time
print("Time elapsed %s" %time_taken)

i = 0
for infile in os.listdir('inputfiles'):
    if infile.endswith('.topo'):
        in_file = infile[:-5]
        out_file = infile[:-5]
        print("Running %s file" %i)
        bool.main(in_file,out_file)
        compute_JSD(wild_type,out_file,in_file)
        time_taken = time.time()  -start_time
        print("Time elapsed %s" %time_taken)
        gc.collect()
        i += 1

print("All the analysis is done")
