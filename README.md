## Topological signatures in regulatory network enable phenotypic heterogeneity in small cell lung cancer

This resource provides the Python code to reproduce all the figures and key results described in [**Topological signatures in regulatory network enable phenotypic heterogeneity in small cell lung cancer**](https://www.biorxiv.org/content/10.1101/2020.10.30.362228v1)

The analysis done can be briefly described as:

* **Discrete Modelling**: Asynchonous Update on Ising model of Wild-Type Small Cell Lung Cancer(WT-SCLC) network. This is done by the set of codes given [here](https://github.com/uday2607/CSB-SCLC/tree/master/Additional_Codes/Fast-Bool).
* **Continuous Modelling**: **RACIPE** is used to generate an ensemble of continuous models of WT-SCLC. For this we have used **RACIPE-1.0** package which can be found [here](https://github.com/simonhb1990/RACIPE-1.0).
* **Experimental Data Analysis:** Using SCLC cell line data like [**CCLE**](https://data.broadinstitute.org/ccle_legacy_data/mRNA_expression/CCLE_Expression_2012-09-29.res) and [**GSM73160**](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE73160), verification of Theoretical results predicted by Ising Model and RACIPE is done and patterns seen in datasets are explained using the models used. This is done by the set of codes given [here](https://github.com/uday2607/CSB-SCLC/tree/master/Additional_Codes/BioData-Analysis).

### Figures
All the figures presented in the paper including Supplementary Figures (apart from the Schematics and Network Representation) are provided in the [``Figures``](https://github.com/uday2607/CSB-SCLC/tree/master/Figures) folder. Details of reproducing the figures are briefly given in the in the ``README`` file in each folder containing the subfigures.

### Simulation Data
**Boolean Simulation data** generated using [``Fast-Bool``](https://github.com/uday2607/CSB-SCLC/tree/master/Additional_Codes/Fast-Bool) and **Edge Perturbation data** generated using [``Edge_Perturbation``](https://github.com/uday2607/CSB-SCLC/tree/master/Additional_Codes/Edge_Perturbation) are provided in the **Simulation_Data** folder. Since **RACIPE** simulation data files are quite huge, they are uploaded to this [drive link](https://drive.google.com/drive/folders/1PKs5vHkXCoJm9Wcg7P4nBPdPrFJCxJ5B?usp=sharing).

### Additonal Codes
This folder contains all the codes required for data analysis and simulation of WT-SCLC network. These are the basic framework of codes which some scripts used for figure production relies on.

### How to reproduce the plots?
**1.** Clone the GitHub Repository
```
git clone https://github.com/uday2607/CSB-SCLC
```
**2.** Set the working directory to ``CSB-SCLC``
**3.** Install all the Required Python Packages (**Conda** is preferable)
```
while read requirement; do conda install --yes $requirement || pip install $requirement; done < requirements.txt
```
**4.** Go to the folder corresponding to the figure that needs to be reproduced and follow the instructions given there
**5.** Voila! you are done

### Notes
* Some of the codes have an option of running processes in Parallel. Just make sure that you don't give spawn more processes than your CPUs can handle.
* Installing Python packages using **Conda** would be preferable. Using **Intel Python Distribution** gives significant speed boosts in some of the codes.
* Codes like **UMAP_analysis** and **Bool.py** may take longer times. Just be patient and don't **Ctrl+C** it even if you have to wait for some time (_Just Don't do it. Time is precious_)

### Requirements
Python(Tested on Version 3.8.5)



