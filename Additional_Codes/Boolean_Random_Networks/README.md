## Boolean Random Networks

Using [``Fast-Bool``](https://github.com/uday2607/CSB-SCLC/tree/master/Additional_Codes/Fast-Bool) as the base of the code, **Boolean_Random_Networks** creates 1000 Random Networks from WT-SCLC network and runs Asynchronous Update on every single network.

``runner.py`` is the main code which imports functions from several python scripts and runs the analysis. It uses ``RandNetworkFiles.py`` from the folder [``Utilities``](https://github.com/uday2607/CSB-SCLC/tree/master/Additional_Codes/Boolean_Random_Networks/Utilities), which generates 1000 Random networks from a given network, to generate the RNs for WT-SCLC network.

``bool.py`` just like in [``Fast-Bool``](https://github.com/uday2607/CSB-SCLC/tree/master/Additional_Codes/Fast-Bool) runs the Boolean Update on a given Network

``correlation.py`` calculates the Pearson Correlation matrix from the steady state distribution of a given Random network. ``random_correlation.py`` generates 1000 Pearson Correlation matrices of continuous values from a Discrete valued Pearson Correlation matrix (as mentioned in SI) and calculates J values of these matrices.

``influence.py`` calculates the Influence matrix of path length 10 from the Interaction matrix of a given Random network.

