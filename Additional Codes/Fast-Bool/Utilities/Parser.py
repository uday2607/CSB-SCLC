import os
import numpy as np
from pathlib import Path

################################################################################
def InputParser(Input_File):
    '''parser parameters for simulation and transition matrix building'''
    INPUT = {'network': 'rules',
             'node_values': '1,-1',
             'ini_on': '',
             'ini_off': '',
             'fixed_on': '',
             'fixed_off': '',
             'turn_off': '',
             'turn_on': '',
             'plot_nodes': '',
             'rounds': 0,
             'steps': 1,
             'mode': 'Sync',
             'model': 'Ising',
             'NetworkX': False,
             'Parallel_Process': False,
             'Number_processes': 1,

             }  # define parameters

    for each_line in open(Input_File).readlines():
        para_name = each_line.split('=')[0].strip()
        para_value = each_line.split('=')[1].strip()
        if para_name in list(INPUT.keys()):
            # Creating key-pair values for Inputs
            INPUT[para_name] = para_value
        else:
            print("Error: Unknown Parameters: %s" % para_name)
            sys.exit()  # Exits out of code so that OP can rectify the errors

    try:
        INPUT['network'] = str(INPUT['network'])
        INPUT['node_values'] = str(INPUT['node_values'])
        INPUT['ini_on'] = [node.strip() for node in INPUT['ini_on'].split(',')]
        INPUT['ini_off'] = [node.strip()
                            for node in INPUT['ini_off'].split(',')]
        INPUT['fixed_on'] = [node.strip()
                             for node in INPUT['fixed_on'].split(',')]
        INPUT['fixed_off'] = [node.strip()
                              for node in INPUT['fixed_off'].split(',')]
        INPUT['turn_on'] = [node.strip().strip('(').strip(')').split(';')
                            for node in INPUT['turn_on'].split(',')]
        INPUT['turn_off'] = [node.strip('(').strip(')').strip().split(
            ';') for node in INPUT['turn_off'].split(',')]
        INPUT['plot_nodes'] = [node.strip()
                               for node in INPUT['plot_nodes'].split(',')]
        INPUT['rounds'] = int(INPUT['rounds'])
        INPUT['steps'] = int(INPUT['steps'])
        INPUT['mode'] = str(INPUT['mode'])
        INPUT['model'] = str(INPUT['model'])
        INPUT['NetworkX'] = True if INPUT['NetworkX'] == 'True' else False
        INPUT['Parallel_Process'] = True if INPUT['Parallel_Process'] == 'True' else False
        INPUT['Number_processes'] = int(INPUT['Number_processes'])
        for empty_keys in list(INPUT.keys()):
            if INPUT[empty_keys] == [''] or INPUT[empty_keys] == [['']]:
                # Formatting all the inputs into desired form
                INPUT[empty_keys] = []
            # [''] or [['']] for empty cases
    except BaseException:
        print("Error: Invalid input data types!")
        sys.exit()  # Exits out of code so that OP can rectify the errors

    values = ['1,-1', '1,0']
    if INPUT['node_values'] in values:
        INPUT['node_values'] = [
            float(i) for i in (
                INPUT['node_values']).split(',')]
    else:
        print("Wrong Node Values! Use 1,-1 or 1,0")
        sys.exit()  # Exits out of code so that OP can rectify the errors

    if INPUT['mode'] not in ['Async', 'Sync']:
        print("Wrong simulation method! Use 'Sync' or 'ASync'")
        sys.exit()  # Exits out of code so that OP can rectify the errors

    Models = ['Ising', 'InhibitoryDominant', 'ActivatoryDominant']
    if INPUT['model'] not in Models:
        print("Wrong model! Use 'Ising','InhibitoryDominant' or 'ActivatoryDominant'")
        sys.exit()  # Exits out of code so that OP can rectify the errors

    return INPUT

################################################################################
def ReadRules(file, model):
    ''' Reads .ids and .topo file to get nodes and interactions '''

    current_dir = os.getcwd()  # current working directory
    path = current_dir + "/"
    NODES = [
        x.split('\t')[0] for x in open(
            Path(
                path +
                file +
                '.ids')).readlines()]  # Contains all the nodes (from .ids)

    NODES = sorted(NODES) #sorting the nodes alphabetically

    INTERMAT = np.ascontiguousarray([[0] * len(NODES)] * len(NODES))  # Interaction matrix

    Models = ['Ising', 'InhibitoryDominant',
              'ActivatoryDominant']  # All Models
    # Differnt edge weights for different models
    Edge_weights = [[1.0, -1.0], [1.0, -1000.0], [1000.0, -1.0]]
    for line in open(
        Path(
            path +
            file +
            '.topo')).readlines()[
            1:]:  # reads interactions from .topo file
        res = line.split()
        if res[2] == '1':
            INTERMAT[NODES.index(res[1])][NODES.index(
                res[0])] = Edge_weights[Models.index(model)][0]
        if res[2] == '2':
            INTERMAT[NODES.index(res[1])][NODES.index(
                res[0])] = Edge_weights[Models.index(model)][1]
           
    return NODES, INTERMAT

################################################################################

def PreDefine(INPUT, nodes):
    ''' Give values to all the nodes which are predefined  '''

    ini_state = {}  # define inital states of each nodes
    for nodes in INPUT['ini_on']:
        ini_state[nodes.index(nodes)] = INPUT['node_values'][0]
    for nodes in INPUT['ini_off']:
        ini_state[nodes.index(nodes)] = INPUT['node_values'][1]

    fixed_state = {}  # define fixed states of the nodes
    for nodes in INPUT['fixed_on']:
        fixed_state[nodes.index(nodes)] = INPUT['node_values'][0]
    for nodes in INPUT['fixed_off']:
        fixed_state[nodes.index(nodes)] = INPUT['node_values'][1]

    turn_state = {}  # define turn on/off of the States
    for nodes in INPUT['turn_on']:
        turn_state[nodes.index(nodes[0])] = [
            int(nodes[1]), INPUT['node_values'][0]]
    for nodes in INPUT['turn_off']:
        turn_state[nodes.index(nodes[0])] = [
            int(nodes[1]), INPUT['node_values'][1]]

    return ini_state, fixed_state, turn_state

################################################################################
