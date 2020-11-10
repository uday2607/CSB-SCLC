# BioData Analysis  
   
A collection of codes generated (for SCLC project) to run data analysis on SCLC datasets using several algorithms. These codes can be used to run analysis on Bulk RNA data, Single Seq data,Tumor cell lines and several other experimental data sets. The functions/ algorithms used to run the analysis can be found in [``Funcs``](https://github.com/uday2607/CSB-SCLC/tree/master/Additional_Codes/BioData-Analysis/Funcs) folder. For this project, CCLE (can be found [here](https://data.broadinstitute.org/ccle_legacy_data/mRNA_expression/CCLE_Expression_2012-09-29.res)) and GSM73160 (can be found [here](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE73160)) are used. Text files of the datasets can be found in ``Datasets`` folder.
  
### How to use the codes?  
#### IN file  
A **.in** file in ``infiles`` folder sends information to [``Parser file``](https://github.com/uday2607/CSB-SCLC/blob/master/Additional_Codes/BioData-Analysis/Parse.py) which parses through the dataset (supported file formats: txt, csv, xlsx, python pickled (binary) file) and returns a Pandas dataframe \(columns are cell line indices and rows are names of genes) after parsing. It has an option to take only selected cell lines from dataset that are relevant to the analysis. The structure of an **.in** file is as follows: 

|                     	|   	|                                                                                            	|
|---------------------	|---	|--------------------------------------------------------------------------------------------	|
| **InFolder**        	| = 	| {Name of the Folder which contains infiles}                                                            	|
| **Infile**          	| = 	| {Name of the data set (along with file extension) }                                        	|
| **log2**            	| = 	| {True/False} # Whether or not to apply log2 on dataset values                              	|
| **All_samples**     	| = 	| {True/False} # Boolean value on whether or not to take all cell lines/ samples              	|
| **Select_samples**  	| = 	| {Cell lines which are **ONLY** to be considered, seperated by a **comma(,)**} # You can only "select" samples or "reject" samples.<br> **You can't do both at the same time!!**(wicked weird things happens) 	|
| **Deselct_samples** 	| = 	| {Cell lines which are **NOT** to be included, seperated by a **comma(,)**} # Opposite of select_columns                     	|
| **Title**           	| = 	| {Title to be used for the plots generated}                                                       	|
| **OutFolder**       	| = 	| {Folder to which plots are to be saved}                                                    	|

For example, you can look at **.in** files present [here](https://github.com/uday2607/CSB-SCLC/tree/master/Additional_Codes/BioData-Analysis/infiles) to get a better understanding.
    
**NOTE:** In **Select_samples** and **Deselect_samples**, cell line names are to be seperated using a **comma(,)**. If most of the cell line indices are serial i.e.. "Sample1, Sample2, Sample3 ... SampleN" and many samples are to be selected/rejected, one can use "**colon(:)**" to specify "from" and "to" to select/reject the cell lines. Example:  
  
<p align="center",display: inline-block>Select_samples = sample2, sample4 , sample10:sample34, sample39 <br>  
("from:to" -> "FROM" sample "TO" sample. Both are inclusive)  </p>

### Input file
A **.input** (or can use any extension) file in ``input`` folder sends information to **[Parser file](https://github.com/uday2607/CSB-SCLC/blob/master/Additional_Codes/BioData-Analysis/Parse.py)** which parses through the **.in** file (from ``infiles`` folder) mentioned in **.input** file. And it also has names of functions/algorithms which are to be used in the data analysis of a dataset. An example is given below:  
|                     	|   	|                                                                                            	|
|---------------------	|---	|--------------------------------------------------------------------------------------------	|
| **IN**        	      | = 	| {names of **.in** files for which data analysis needs to be run <br> (seperated by **comma(,)**}                |
| **funcs**           	| = 	| {Names of functions/algorithms which needs to be applied on dataset <br> (seperated by **comma(,)** }                	|
| **Nodes**             | =   | {Names of Genes whose expression levels are to be taken as orthogonal dimensions in a given analysis <br> (seperated by **comma(,)** }           	  |
| **Color**             | =   | {Names of Genes whose expression levels are used for color labelling of scatter points <br> (seperated by **comma(,)** }        	|

For example, you can look at **.input** files present [here](https://github.com/uday2607/CSB-SCLC/tree/master/Additional_Codes/BioData-Analysis/input) to get a better understanding.
  
### data_analysis.py  
This is the python script which does all analysis by importing functions from other python scripts and run them for a given dataset. Import all the functions that are to be used (i.e.. the ones given under **funcs** option in **.in** file from [``input folder``](https://github.com/uday2607/CSB-SCLC/tree/master/Additional_Codes/BioData-Analysis/input)). Then run the scipt as shown:
  
<pre><code>python data_analysis.py {name_of_infile}.input </code></pre>
  
Now a folder with name as specified in **.in** file from ``infiles`` folder will be generated along with plots and data from functions used which are specified in **.input** file from [``input folder``](https://github.com/uday2607/CSB-SCLC/tree/master/Additional_Codes/BioData-Analysis/input)) folder
