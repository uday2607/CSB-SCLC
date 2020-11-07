import os, sys, pickle
from pathlib import Path
import pandas as pd
import numpy as np

def dequote(s):
    """
    If a string has single or double quotes around it, remove them.
    Make sure the pair of quotes match.
    If a matching pair of quotes is not found, return the string unchanged.
    """
    if s == '' or s == " ":
        return s.strip()
    if (s[0] == s[-1]) and s.startswith(("'", '"')):
        return s[1:-1]
    return s.strip()

def dequote_list(ls):
    """
    dequote for a list
    """
    ns = []
    for s in ls:
        if s == '' or s == " ":
            ns.append(s.strip())
        elif (s[0] == s[-1]) and s.startswith(("'", '"')):
            ns.append(s[1:-1].strip())
        else:
            ns.append(s.strip())

    return ns

def Float_list(ls):

    ns = []
    for e in ls:
        if e != '':
            ns.append(float(e))
        else:
            ns.append(0)

    return ns

def parse_infile(file):

    with open(Path("infiles",file), 'r') as f:
        lines = f.readlines()

    IN = lines[0].split('=')[1].strip().strip("\n")
    Infile = lines[1].split('=')[1].strip().strip("\n")
    log2 = lines[2].split('=')[1].strip().strip("\n")
    title = lines[6].split('=')[1].strip().strip("\n")
    out = lines[7].split('=')[1].strip().strip("\n")

    if not os.path.exists(out):
        os.mkdir(out)

    if Infile[-3:] == 'txt':

        A = open(Path(IN, Infile)).readlines()

        Cell_Lines = []
        for col in A[0].split('\t'):
            Cell_Lines.append(dequote(col.strip().strip('\n')))

        Nodes = []
        for i in range(1,len(A)):
            Nodes.append(dequote(A[i].split('\t')[0].strip()))

        data = pd.DataFrame(columns = Cell_Lines, index = Nodes)

        for i in range(1,len(A)):
            data.loc[dequote(A[i].split('\t')[0].strip()),dequote_list(A[0].strip('\n').split('\t'))] = A[i].strip('\n').split('\t')[1:]

    elif Infile[-3:] == 'csv':

        data = pd.read_csv(Path(IN,Infile), index_col = 0)

    elif Infile[-4:] == 'xlsx':

        data = pd.read_csv(Path(IN,Infile), index_col = 0)

    elif Infile[-4:] == 'data':

        with open(Path(IN,Infile),'rb') as f:
            data = pickle.load(f)

    data = data.replace('NA', 0)

    if lines[3].split('=')[1].strip().strip("\n") == 'True':
        if log2 == 'True':
            return data.astype(float).apply(np.log2), title, out
        else:
            return data.astype(float), title, out
    else:
        Data = pd.DataFrame(index = Nodes)

        if lines[4].split('=')[1].strip().strip("\n") != '':

            string = lines[4].split('=')[1].strip().strip("\n")
            select = []
            for col in string.split(','):
                if ':' in col:
                    Data = pd.concat([Data, data[list(data.loc[:, dequote(col.split(':')[0].strip()):dequote(col.split(':')[1].strip())].columns)]], axis = 1)
                else:
                    select.append(dequote(col.strip()))

            Data = pd.concat([Data, data[select]], axis = 1)

            if log2 == 'True':
                return Data.astype(float).apply(np.log2), title, out
            else:
                return Data.astype(float), title, out

        else:
            string = lines[5].split('=')[1].strip().strip("\n")
            deselect = []
            for col in string.split(','):
                if ':' in col:
                    data = data.drop(list(data.loc[:, dequote(col.split(':')[0].strip()):dequote(col.split(':')[1].strip())].columns), axis = 1)
                else:
                    deselect.append(dequote(col.strip()))
            data = data.drop(deselect, axis=1)

            if log2 == 'True':
                return data.astype(float).apply(np.log2), title, out
            else:
                return data.astype(float), title, out

def parse_input(file):

    with open(Path("input",file),'r') as f:
        lines = f.readlines()

    Inputs = lines[0].split("=")[1].strip("\n").strip().split(",")
    IN = []
    for data in Inputs:
        IN.append(data.strip())

    funcs = lines[1].split("=")[1].strip("\n").strip().split(",")
    runs = []
    for func in funcs:
         runs.append(func.strip())

    dims = lines[2].split("=")[1].strip("\n").strip().split(",")
    Dims = []
    for dim in dims:
        Dims.append(dim.strip())

    color = lines[3].split("=")[1].strip("\n").strip().split(",")
    Colors = []
    for c in color:
        Colors.append(c.strip())

    return IN, runs, Dims, Colors
