### Fig 2B

##### Fig 2B i

Place **RACIPE.input** in the **input** folder of [**BioData-Analysis**](https://github.com/uday2607/CSB-SCLC/tree/master/Additional_Codes/BioData-Analysis). Then run the **data_analysis.py** as mentioned [here](https://github.com/uday2607/CSB-SCLC/tree/master/Additional_Codes/BioData-Analysis). A folder with the name **RACIPE** will be generated and correlation plot will be saved in that folder.

##### Fig 2B ii

**read_J_vals.py** generates the **Fig 2B ii** using **CCLE_discrete_J_vals.xlsx** and **73160_discrete_J_vals** which can be generated from [**BioData-Analysis**](https://github.com/uday2607/CSB-SCLC/tree/master/Additional_Codes/BioData-Analysis) by placing **Random_corre.input** in the **input** folder and running **data_analysis.py** and **corre.txt** which can be generated from [**Boolean_Random_Networks**](https://github.com/uday2607/CSB-SCLC/tree/master/Additional_Codes/Boolean_Random_Networks)

**73160_discrete_J_vals** and **CCLE_discrete_J_vals** contains J values of discrete form of Correlation matrices (Continuous to Discrete by discretizing the values to -1/1. For more information go through the SI material) of datasets 73160 and CCLE respectively.

**corre.txt** contains number of states resulting from Asynchronous update of a Random network Network and J value of the correlation matrix resulting from the steady state distribution. Index 0 is data of WT SCLC network.
