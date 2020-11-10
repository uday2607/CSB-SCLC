# FastBool
Python package for simulating Asynchronous and Synchronous Updating methods of Boolean networks

**Command to run**: <pre><code>python bool.py bool.in </code></pre>
bool.in file has all the instructions for the simulation. These are:

**network**: name of the network (.topo and .ids file with this name should be present in the same folder) <br>
**node_values**: Binary values assigned for the <br>
**ini_on**: Name of nodes seprated by ',' which have initial value of 'high' (value depends on node_values) <br>
**ini_off**: Name of nodes seprated by ',' which have initial value of 'low' (value depends on node_values) <br>
**fixed_on**: Name of nodes seprated by ',' which have fixed value of 'high' (value depends on node_values) <br>
**fixed_off**: Name of nodes seprated by ',' which have fixed value of 'low' (value depends on node_values) <br>
**turn_off**: Name of nodes and time step at which node will be permanently fixed 'low', format: (Node 1, t1); (Node2, t2) <br>
**turn_on**: Name of nodes and time step at which node will be permanently fixed 'low', format: (Node 1, t1); (Node2, t2) <br>
**plot_nodes**: Name of the nodes seperated by ',' for which you want a plot of their expression levels vs time <br>
**rounds**: Number of initial conditions you want the simulation to run for <br>
**steps**: Number of time steps <br>
**mode**: Update Mode (Async or Sync) <br>
**model**: Model specifing the inteartion edge values(Ising -> [1,0,-1], ActivatoryDominant -> [1000,0,-1], InhibitoryDominant -> [1,0,-1000] <br>
**NetworkX**: Boolean value whether or not to use "networkX", python package to do State transition analysis (which gives types of states either oscillatory or steady-state) <br>
**Parallel_Process**: Boolean value on whether or not to use parallel processes <br>
**Number_processes**: Number of cores (so parallel processes) to use <br>

For the 'network' you are required to have two files: 'name_of_network.ids' and 'name_of_network.topo' file. '.ids' file should have all the name of the nodes along with their indices (starting from 0) [format: node_name node_index]. And then for '.topo' file it should have names of 'Source' 'Target' and 'interaction'. Check out the files in the repo (of 'sclcnetwork') provided for better understanding. <br>
