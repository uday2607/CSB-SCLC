import numpy as np

def GetIni(index,nodes,values,ini_state,fixed_state):
    ''' Gives an initial condition '''

    values = np.array(values)
    # Genearting a boolean vector of size node num
    ini_vect = np.random.choice(values,len(nodes))
    if ini_state or fixed_state:
        for node,value in dict(list(ini_state.items()) + list(fixed_state.items())):
            ini_vect[nodes.index(node)] = value
    return ini_vect
