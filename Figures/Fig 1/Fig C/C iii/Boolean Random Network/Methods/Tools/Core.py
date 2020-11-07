import os
from Methods.Tools.Funcs import *

################################################################################

def AttractorAnalysis(nodes,StateTraj,inter_mat,folder):
    '''Identifying attractors using NetworkX and writes them to a file'''

    import networkx as nx

    for traj in load_data('traj.f'):
        StateTraj.add_edges_from(traj)
    attractors = list(nx.attracting_components(StateTraj))

    current_dir = os.getcwd() #current working directory
    path = current_dir + "/OUTPUT/" + folder
    try:
        os.makedirs(path) #If folder doesn't exist then create it
    except:
        pass

    import xlsxwriter as xlsxwt
    workbook = xlsxwt.Workbook(os.path.join('OUTPUT',folder,'NetworkX_Sync.xls'))
    worksheet = workbook.add_worksheet("stable_states")
    cell_format = workbook.add_format()
    cell_format.set_bg_color('black')

    for i, node in enumerate(nodes):
        worksheet.write(i+1, 0, node) #Writing names of the nodes
    worksheet.write(len(nodes)+2,0, 'Frustration')
    worksheet.write(len(nodes)+3,0, 'Frequency')

    attract_list = []
    j = 0
    for states in attractors:
        for state in states:
            attract_list.append(state)
            if len(states) == 1:
                worksheet.write(0,j+1,"Fixed Point")
            else:
                worksheet.write(0,j+1,"{} state oscillator".format(len(states)))
            j += 1

    for i in range(1,len(attract_list)+1):
        state = num2vect(attract_list[i-1],len(nodes)).tolist()
        for j,node_value in enumerate(state):
            if node_value == 1:
                worksheet.write(j+1,i,node_value,cell_format)
            else:
                worksheet.write(j+1,i,node_value)
        worksheet.write(len(nodes)+2,i,Frustration(attract_list[i-1],inter_mat))
        worksheet.write(len(nodes)+3,i,StateTraj.degree[attract_list[i-1]])

    worksheet.set_column(0,len(attractors)+2,15)

    workbook.close()
    print("All the attractoors by Networks are found. Number of attractors found is %s" %len(attractors))
    print("Saving these states in %s/NetworkX_Sync.xls\n" % folder)
################################################################################
