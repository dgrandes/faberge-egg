import os, sys
from elements import *


def parseDemand(demandType):
    
    demand = None
    if demandType is None:
        demand = Demand(0,0)
    elif demandType == "0":
        demand = Demand(3,1)
    elif demandType == "1":
        demand = Demand(4,2)
    elif demandType == "2":
        demand = Demand(5,3)

    return demand


def parseProblemInstances(input):
    
    x_coords = []
    y_coords = []
    demand_type = []

    with open(input, 'rU') as f:
        i = 0
        for line in f:
            line = line.rstrip()

            if i == 0:
                x_coords.append(line.split(' '))                
            elif i == 1:
                y_coords.append(line.split(' '))
            elif i == 2:
                demand_type.append(line.split(' '))
                i = -1

            i = i + 1

    for d in demand_type:
        d[0] = None

    problems = []
    for p in xrange(len(x_coords)):
        problem_instance = []
        for j in xrange(len(x_coords[p])):
            c = Customer(j, x_coords[p][j],y_coords[p][j],parseDemand(demand_type[p][j]))
            problem_instance.append(c)
        problems.append(problem_instance)

    return problems