[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

# BioData Analysis  
   
A group of codes written (for SCLC project) to do several data analysis on SCLC datasets. These codes can do analysis on Bulk RNA data, Single Seq data,Tumor cell lines etc..,. These functions can be found in "Funcs" folder
  
## Instruction on running the analysis  
### IN file  
'.in' file in 'infiles' folder sends information to 'Parser' which parses through the dataset (supported file formats: txt, csv, xlsx, pickled file)
and returns a Pandas dataframe. It has an option to take only selected cell lines from dataset that are relevant to the analysis. An examle infile is given below: (Remove "#" comments & {} when running the file)  
  
|                     	|   	|                                                                                            	|
|---------------------	|---	|--------------------------------------------------------------------------------------------	|
| **InFolder**        	| = 	| {Folder which contains infiles}                                                            	|
| **Infile**          	| = 	| {Name of the data set (along with file extension) }                                        	|
| **log2**            	| = 	| {True/False} # Whether or not to apply log2 on dataset values                              	|
| **All_samples**     	| = 	| {True/False} # Boolean value on whetheror not to take all cell lines/ samples              	|
| **Select_samples**  	| = 	| {Name of columns which needs to taken} # You can only "select" samples or "reject" samples 	|
|                     	|   	| while running.You can't do both!!                                                          	|
| **Deselct_samples** 	| = 	| {Name of columsn which needs to rejected} # Opposite of select_columns                     	|
| **Title**           	| = 	| {Title of the plots to be generated}                                                       	|
| **OutFolder**       	| = 	| {Folder in which plots are to be saved}                                                    	|
    
    
**NOTE:** In "select_samples" and "deselect_samples", sample names are to be seperated by ','. Also most of the time sample names are serial i.e.. "Sample1, Sample2, Sample3 ... SampleN". Suppose if many samples are to be selected/rejected, you can use ":" to specify "from" and "to". Example:  
  
    
Select_samples = sample2, sample4 , sample10:sample34, sample39  
("from:to" -> "FROM" sample "TO" sample. Both are inclusive)  

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

