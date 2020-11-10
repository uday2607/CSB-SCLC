## Edge Perturbation

All the codes used for the Edge Perturbation Analysis are added to this folder. Folders with names ``run1``, ``run2`` and ``run3`` have the python scripts to generate network files with a single edge perturbed (deleted/changed) per each file. Similar to the [``Boolean_Random_Networks``](https://github.com/uday2607/CSB-SCLC/tree/master/Additional_Codes/Boolean_Random_Networks), ``runner.py`` of each **run** folder, runs the Boolean update of every single network and writes to the outfiles.

``runs.sh`` is a bash script which can be used to automatically run the ``runner.py`` in all the **run** folders. It runs the analysis in a folder sequentially.

Once done, one can use ``edge_perturb_data.py`` to read all the output files and calculate J, R1 & R2 (with RACIPE) and JSD for all the edge perturbed network files. It creates an excel sheet which contains all these metrics along with the Frequencies of top 4 occuring states.
