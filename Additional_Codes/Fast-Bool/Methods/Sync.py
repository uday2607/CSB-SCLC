import numpy as np
import os ,pickle ,math ,time

from Methods.Iterations.iters import IterOneSync

from Methods.Tools.Funcs import *
from Methods.Tools.initial import *
from Methods.Tools.Update import *
from Methods.Tools.Core import *

start_time = time.time()

''' This code is in Alpha phase. Don't trust this at all..... '''

def Dynamics(IniVector,inter_mat,steps,values,fixed_state,turn_state,networkx,plot_nodes,PlotNodes):
    ''' Updates the initial vector for given time steps and gives the steady state vectors '''

    state_traj = []
    state_vect = []

    ''' For numba functionality '''
    inter_mat = inter_mat.astype('float64') #For better calculations
    values = np.array(values) #For numba

    prevVector = IniVector #Initial vector

    state_vect = [prevVector] #Appending initial vector to state vectors
    index = 0
    for i in range(steps): #Time dynamics for given steps
        if index == 10:
            break
        if turn_state:
            prevVector,turn_state,fixed_state = UpdateTurnState(prevVector, i,turn_state, fixed_state)
        nextVector = IterOneSync(inter_mat, prevVector,values)
        if fixed_state:
            nextVector = UpdateFixedState(nextVector, fixed_state)
        if networkx:
            state_vect.append([nextVector])
            prevV = vect2num(prevVector)
            nextV = vect2num(nextVector)
            traj = (prevV,nextV)
            state_traj.append(traj)
        if np.all(prevVector == nextVector):
            index += 1
        else:
            index = 0
        if i < steps-1:
            prevVector = nextVector
        #adding this trajecctory to the State traj vector

    if plot_nodes:
        state_vect1 = np.transpose(state_vect)
        state_vect1[state_vect1<0] = 0 #Replacing all -1s with 0
        for i,node in enumerate(plot_nodes):
            PlotNodes[i] = [x+y for x,y in zip(PlotNodes[i],state_vect1[node])]

    if networkx:
        with open('traj.f', 'ab') as f:
            pickle.dump(state_traj,f, protocol=pickle.HIGHEST_PROTOCOL)

    if np.all(prevVector == nextVector): #Fixed Point Attractors
        return (True, vect2num(IniVector), vect2num(nextVector), PlotNodes) #Fixed Point steady state. IniVector is the basin of the Steady state
    else:
        return (False, False, False, PlotNodes) #If it is not a steady state don't return anything

def Simulation(nodes,inter_mat,input,IniState,FixedState,TurnState,folder):
    ''' Runs dynamics for given number of initial conditions '''

    print("Preparing Simulation rules...\n")
    import multiprocessing as mp

    steps = input['steps'] #Number of time Steps
    if input['rounds']:
        rounds = input['rounds']
    else:
        rounds = 2**len(nodes)
    # Number of simulations
    run_power = math.ceil((highestPowerof2(rounds)/2)) # So that we can create a nested for loop for multiple processes
    values = input['node_values'] #Values of node

    basin_dic = {}  # store attractor for each state, key as basin state, value as attractor state.
    SteadyState = {}  # store steadystate and its frequency
    frustration = {} # store frustration of each stable stable, stable state as key, frustration as value


    if input['Parallel_Process']:
        print("\nParallel Process support is enabled. Number of Individual processes is %s" % input['Number_processes'])
        process = input['Number_processes']
        pool = mp.Pool(processes = process) #Creating No of processors
    else:
        print("\nParallel Process support is not enabled. Runs take a lot of time....")
        pool = mp.Pool(processes = 1) #Creating 1 process

    #Generating an array for Plot nodes
    plot_nodes = []
    if input['plot_nodes']:
        for node in input['plot_nodes']:
            plot_nodes.append(nodes.index(node))
        PlotNodes = np_as_tmp_map(np.array([[0 for col in range(steps)] for row in range(len(plot_nodes))])) #Creating empty list for plot nodes
    else:
        PlotNodes = [] #returns an empty list when we don't need to plot

    print("Preparing %s runs...." %2**(run_power))
    print("Fireing the runs for each initial condition. May take some time")
    index = 0 #index of run
    for i in range(2**(run_power)):
        value = i*100/2**(run_power)
        print(" %0.4f percent complete" %value, end = '\r', flush = True)
        jobs = []
        for j in range(int(rounds/2**(run_power))):
            IniVector = GetIni(index,nodes,values,IniState,FixedState)
            index += 1
            jobs.append(pool.apply_async(Dynamics,args=(IniVector,inter_mat,steps,
                                            values,FixedState,TurnState,input['NetworkX'],
                                            plot_nodes,PlotNodes)))
            #Pool processes
        [result.wait() for result in jobs]
        for results in jobs:
            result = results.get()
            if result[0]:
                if result[2] in SteadyState: #If steady state is already found and basin is different, then we store the basin
                    basin_dic[result[1]] = result[2]
                    SteadyState[result[2]] += 1 #Frequency increased
                else:
                    basin_dic[result[1]] = result[2] #Adding basin and attractors
                    SteadyState[result[2]] = 1
                    frustration[result[2]] = Frustration(result[2],inter_mat)
            PlotNodes = result[3]

    pool.close() #Very important to close the pool. Or multiple instances will be running

    if input['NetworkX']: #If we use networkx to analyze attractors
        import networkx as nx
        State_traj = nx.DiGraph() #Digraph for State trajectories
        AttractorAnalysis(nodes,State_traj,inter_mat,folder)
        State_traj.clear()
        os.remove('traj.f')

    if input['plot_nodes']:
        print("Ploting Node activity dynamics for the following nodes: ")
        for node in input['plot_nodes']:
            print("* " + node)
        PlotNodes = [[float(j)/rounds for j in i] for i in PlotNodes] #fastest way to divide all elements of list of lists
        plot_result(PlotNodes,input['plot_nodes'],folder,marker=False) #If we want plot of dynamics, it does it

    return basin_dic,SteadyState,frustration

def SummarySync(nodes,inter_mat,input,IniState,FixedState,TurnState,folder):
    ''' Summarises all the info of this Synchronous update dynamics '''

    print("Summarizing the results.....\n")
    Basins,SteadyState,frustration = Simulation(nodes,inter_mat,input,IniState,FixedState,TurnState,folder)

    current_dir = os.getcwd() #current working directory
    path = current_dir + "/OUTPUT/" + folder
    try:
        os.makedirs(path) #If folder doesn't exist then create it
    except:
        pass

    import xlsxwriter as xlsxwt

    workbook = xlsxwt.Workbook(os.path.join('OUTPUT',folder,'Summary_Sync.xlsx'))
    worksheet = workbook.add_worksheet("stable_states")
    cell_format = workbook.add_format()
    cell_format.set_bg_color('black')

    for i, node in enumerate(nodes):
        worksheet.write(i+1, 0, node) #Writing names of the nodes

    worksheet.write(len(nodes)+2,0,'Frequency')
    worksheet.write(len(nodes)+3,0,'Frustration')

    for i, (state,values) in enumerate(SteadyState.items()):
        worksheet.write(0,i+1,'Fixed point')
        vect = num2vect(state, len(nodes))
        for j,node in enumerate(vect):
            if node == input['node_values'][0]:
                worksheet.write(j+1,i+1,str(node),cell_format)
            else:
                worksheet.write(j+1,i+1,str(node))
        worksheet.write(len(nodes)+2,i+1,str(values))
        worksheet.write(len(nodes)+3,i+1,str(frustration[state]))

    workbook.close()

    state_file = open(os.path.join('OUTPUT',folder,'states.f'), 'wb')
    pickle.dump(SteadyState,state_file)
    state_file.close()
    #Dumping all the steady states to a file as we need it later

    time_taken = (time.time() - start_time)
    print("Total Time elapsed: %0.4f " %time_taken)

    return
