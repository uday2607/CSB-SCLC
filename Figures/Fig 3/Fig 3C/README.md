### Fig 3C

##### Fig 3C i

**effective_edges.py** calculates the effective activation/inhibition from one group of genes to other. For **Reduced model 1**, use **Influence matrix of path length 10** to calculate the effective edges. **effective_edges.py** takes in **bool_influ.data** (contains influence matrix of path length 10), which can be generated using th codes given [here](https://github.com/uday2607/CSB-SCLC/tree/master/Figures/Fig%203/Fig%203A/A%20i/Influence)

**Note:** From **Edge_perturbation analysis**, one can clearly see that  edge from **NEUROD1** to **Group A** and edge from **ELF3** to **NEUROD1** doesn't affect the steady state distribution of WT SCLC network. So even though, **effective_edges.py** shows that there is an effective edge from **NEUROD1** to **Group A** and from **ELF3** to **NEUROD1**, we have omitted it to capture most of the features of WT SCLC network into the Reduced model.

##### Fig 3C ii

Steady state distribution of **Reduced Model 1** can generated using [Fast-Bool](https://github.com/uday2607/CSB-SCLC/tree/master/Additional_Codes/Fast-Bool), by using the **model1** .ids and .topo file. Mean and standard deviation of the resulting frequencies for several runs are given in **model1.csv**. **states_hist.py** takes in **model1.csv** and plots the bargraph.
