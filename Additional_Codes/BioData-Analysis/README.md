# BioData Analysis  
   
A collection of codes generated (for SCLC project) to run data analysis on SCLC datasets using several algorithms. These codes can be used to run analysis on Bulk RNA data, Single Seq data,Tumor cell lines and several other experimental data sets. The functions/ algorithms used to run the analysis can be found in [Funcs](https://github.com/uday2607/CSB-SCLC/tree/master/Additional_Codes/BioData-Analysis/Funcs) folder.
  
### How to use the codes?  
#### IN file  
An **.in** file in **infiles** folder sends information to **[Parser file](https://github.com/uday2607/CSB-SCLC/blob/master/Additional_Codes/BioData-Analysis/Parse.py)** which parses through the dataset (supported file formats: txt, csv, xlsx, python pickled (binary) file) and returns a Pandas dataframe \(columns are cell line indices and rows are names of genes) after parsing. It has an option to take only selected cell lines from dataset that are relevant to the analysis. The structure of an **.in** file is as follows: 

|                     	|   	|                                                                                            	|
|---------------------	|---	|--------------------------------------------------------------------------------------------	|
| **InFolder**        	| = 	| {Name of the Folder which contains infiles}                                                            	|
| **Infile**          	| = 	| {Name of the data set (along with file extension) }                                        	|
| **log2**            	| = 	| {True/False} # Whether or not to apply log2 on dataset values                              	|
| **All_samples**     	| = 	| {True/False} # Boolean value on whether or not to take all cell lines/ samples              	|
| **Select_samples**  	| = 	| {Cell lines which are **ONLY** to be considered} # You can only "select" samples or "reject" samples. **You can't do both at the same time!!**(wicked weird things happens) 	|
| **Deselct_samples** 	| = 	| {Cell lines which are **NOT** to be included} # Opposite of select_columns                     	|
| **Title**           	| = 	| {Title to be used for the plots generated}                                                       	|
| **OutFolder**       	| = 	| {Folder to which plots are to be saved}                                                    	|

For example, you can loop at **.in** files present [here](https://github.com/uday2607/CSB-SCLC/tree/master/Additional_Codes/BioData-Analysis/infiles) to get a better understanding.
    
**NOTE:** In **Select_samples** and **Deselect_samples**, cell line names are to be seperated using a **comma(,)**. If most of the cell line indices are serial i.e.. "Sample1, Sample2, Sample3 ... SampleN" and many samples are to be selected/rejected, one can use ":" to specify "from" and "to" to select/reject the cell lines. Example:  
  
<p align="center">Select_samples = sample2, sample4 , sample10:sample34, sample39  <br>
("from:to" -> "FROM" sample "TO" sample. Both are inclusive)  </p>

### Input file
'.input' (or can use any extension) file in 'input' folder send information to 'Parser' which parses through the .in file which has name of the '.in' file from infiles folder which gives information about whch file to run. And it also has names of functions which needs to be applied on dataset (which is a pandas dataframe now). An example is given below:  
|                     	|   	|                                                                                            	|
|---------------------	|---	|--------------------------------------------------------------------------------------------	|
| **IN**        	      | = 	| {names of .in files on which data analysis needs to be done (seperated by ','}                |
| **funcs**           	| = 	| {Names of function which needs to be applied on datset (seperated by ',') }                	|
| **Nodes**             | =   | {Names of nodes which are the dimensions in a given analysis (seperated by ',') }             |
| **Color**             | =   | {Names of nodes whose expression levels are used for color labels (seperated by ',') }        |
  
### data_analysis.py  
This the python script which does analysis by importing functions from other python scripts and apply them. Import all the functions that needs to be used (i.e.. the ones given in "funcs" in '.in' file from "input folder"). Then just use the scipt as shown:
  
<pre><code>python data_analysis.py {name_of_infile}.input </code></pre>
  
Now a folder with name as specified in .'in' file from 'infiles' folder will be generated along with plots and data from functions used which are specified in '.input' file from 'input' folder
