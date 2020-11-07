import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
import os
from pathlib import Path

def plot_result(results,plotnodes,folder,marker=True):
    current_dir = os.getcwd() #current working directory
    path = current_dir + "/OUTPUT/" + folder
    try:
        os.makedirs(path) #If folder doesn't exist then create it
    except:
        pass

    '''Plot the simulated results'''
    print("Ploting results...")

    plotsymbyl=['o','v','*','s','+','p','x','1','2','h','D','.',','] # plot line with symbyl
    ploti=0

    for i,items in enumerate(plotnodes):  # plot nodes states using matplotlib
        if marker:
            plt.plot(results[i],label=items,linewidth=1,linestyle='-',marker=plotsymbyl[ploti]) #with marker
        else: plt.plot(results[i],label=items,linewidth=1,linestyle='-') #no marker

        ploti += 1
        if ploti >= 12: ploti=0

    plt.xlabel('Steps',size=10)
    plt.ylabel('Percentage',size=10)
    plt.yticks([-0.1,0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1],size=10)
    plt.xticks(size=10)
    plt.legend(prop={'size':10}) # make legend
    plt.savefig('OUTPUT/%s/dynamics.png' % folder ,dpi=400)
    print("All the plotting is done. Save the file in %s as 'dynamics.png'\n" % folder)
    #plt.show()  # show plot
    return

def Plot_network(file):
    current_dir = os.getcwd() #current working directory
    path = current_dir +"/" #+ "/inputfiles/"

    G = nx.DiGraph()

    for line in open(Path(path+file+'.topo')).readlines()[1:] : #reads interactions from .topo file
        res = line.split()
        G.add_edge(res[0], res[1], weight = int(res[2]))

    activators = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == 1]
    inhibitors = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == 2]

    pos = graphviz_layout(G)  # positions for all nodes

    # nodes
    plt.figure(1,figsize=(20,20))
    nx.draw_networkx_nodes(G, pos, node_size=50)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=activators, width=0.5)
    nx.draw_networkx_edges(G, pos, edgelist=inhibitors, width=0.5, alpha=0.5, edge_color='b', style='dashed')

    # labels
    nx.draw_networkx_labels(G, pos, font_size=25, font_family='sans-serif')

    plt.axis('off')
    plt.show()
