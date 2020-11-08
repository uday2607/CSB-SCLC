# This script is for copying intermat files on cluster to a folder

import shutil, os
from pathlib import Path

if not os.path.exists("Random_network_intermat"):
    os.mkdir("Random_network_intermat")

for i in range(1,1001):

    shutil.copy2(Path(os.getcwd(),'OUTPUT/Output_sclcnetwork_{}/intermat.f'.format(i)),'Random_network_intermat/intermat_{}.f'.format(i))    
