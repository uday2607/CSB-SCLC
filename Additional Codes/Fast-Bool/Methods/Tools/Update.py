def UpdateFixedState(bool_vect,fixed_state):
    ''' Chages the values of nodes which have predefined values '''

    if fixed_state:
        for node,value in fixed_state.items():
            bool_vect[node] = value
        return bool_vect
    else:
        return bool_vect

################################################################################

def UpdateTurnState(boolvect,time_step,turn_state,fixed_state):
    ''' Fixes nodes at the given time '''

    if turn_state:
        nodes = []
        for node,values in turn_state.items():
            if values[0] == time_step:
                boolvect[node] = values[1]
                fixed_state[node] = values[1]
                nodes.append(node)
        for node in nodes:
            del turn_state[node] #This Node is no longer used for time update
        return boolvect,turn_state, fixed_state
    else:
        return boolvect, turn_state, fixed_state

################################################################################
