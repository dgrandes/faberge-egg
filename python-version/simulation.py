import os, sys, getopt
from setup import *
from copy import copy as pycopy
import pprint
from random import randint
import timing
import pylab as pylab
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from math import sin, cos


def dbp(string):
    if False:
        print string

pp = pprint.PrettyPrinter(indent=2)

def parseParameters(argv):
    inputfile = ''
    outputfile = ''
    helpText = """
    	python simulation -i inputfile -o outputfile
        """
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print helpText
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print helpText
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    if inputfile == "" or outputfile == "":
        print helpText
        sys.exit(2)
    return inputfile, outputfile

#GO, NO GO Decision
def expLenWithChoice(accumCost, vehicleGiven, routeGiven, Q, d):
    route = routeGiven[:]
    vehicle = pycopy(vehicleGiven)

    if len(route) == 0:
        return accumCost

    nextNode = route[0]

    #The vehicle is at the Depot, it is already at the next node
    if vehicle.currPos.ID == nextNode.ID:
        #load it up
        vehicle.currQ = Q
        #advance the algorithm
        route.pop(0)
        return expLenWithChoice(accumCost, vehicle, route, Q, d)

    withDepotCost = goToDepot(vehicle, nextNode, accumCost, route, Q, d)
    withoutDepotCost = goStraight(vehicle, nextNode, accumCost, route, Q, d)

    #Choose between Go, Not GO
    minCost = min(withDepotCost, withoutDepotCost)

    return minCost
        
def goToDepot(vehicle, nextNode, accumCost, route, Q, d):
    withDepotCost = float("inf")
    goToDepot = False

    vehicleCopy = pycopy(vehicle)
    
    distanceToDepot = distCustomers(vehicle.currPos, route[-1])

    #Don't go to the depot if Im there or coming from there, or going there next
    if not (vehicle.currQ == Q or nextNode.ID == 0):
        goToDepot = True

    if goToDepot:
        #If we go to the depot, the cost needs to include the trip and the vehicle now has Q
        #Going to the depot and then to the next node.
        accumCost = accumCost + distanceToDepot + distCustomers(nextNode, route[-1])

        #Load up the truck again
        vehicleCopy.currQ = Q
        
        #Advancing the vehicle to the next node
        vehicleCopy.currPos = nextNode

        #Analyze demand with the vehicle in the next node
        withDepotCost = analyzeExpectedCostForAllDemand(accumCost, vehicleCopy, route, Q, d)

    return withDepotCost

def goStraight(vehicle, nextNode, accumCost, route, Q, d):
    withoutDepotCost = float("inf")

    vehicleCopy = pycopy(vehicle)   

    distanceToNextNode = distCustomers(vehicle.currPos, nextNode)
    
    #Updating Accum Cost to reaching the new node
    accumCost = accumCost + distanceToNextNode    
    #Advancing the vehicle to reach client
    vehicleCopy.currPos = nextNode        
    #Serve client
    withoutDepotCost = analyzeExpectedCostForAllDemand(accumCost, vehicleCopy, route, Q, d)
    return withoutDepotCost


#EXPECTED LENGTH
def analyzeExpectedCostForAllDemand(accumCost, vehicle, routeGiven, Q, d):
    
    route = routeGiven[:]

    #Reached the end, just return the cost
    if len(route) == 0:
        return accumCost

    #We are standing in the node to analyze
    currentNode = route[0]

    #If the current Node is the depot, then we just return the cost of getting here
    if currentNode.ID == 0:
        finalCost = accumCost + distCustomers(vehicle.currPos, route[-1])
        return finalCost

    #Retrieve from Cache based on node, Q and accumCost
    if (currentNode.ID,vehicle.currQ, accumCost) in d:
        result = d[currentNode.ID, vehicle.currQ, accumCost]
        return result

    costsForAllDemands = []

    #Generate the demands in an array demands
    demands = xrange(currentNode.dem.dmin, currentNode.dem.dmax+1)
    
    for demand in demands:
        subcost = satisfyDemand(demand, vehicle, accumCost, route, Q, d)
        costsForAllDemands.append(subcost)
        
    #The expected cost for all our demands is the average.
    expectedCost = sum(costsForAllDemands)/len(costsForAllDemands)
    
    #Store the end result in the dictionary for further use
    d[(currentNode.ID, vehicle.currQ, accumCost)] = expectedCost
    
    return expectedCost

#Satisfies the demand, updates vehicle and accumCost and goes back to expLen
def satisfyDemand(demand, vehicle, accumCost, route, Q, d):
    vehicleCopy = pycopy(vehicle)

    distanceToDepot = distCustomers(vehicleCopy.currPos, route[-1])
    
    if vehicleCopy.currQ < demand:
        #Failure, we go to the depot and back
        vehicleCopy.currQ = vehicleCopy.currQ - demand + Q
        accumCost = accumCost + 2 * distanceToDepot
    else:
        #update the Q of the vehicle
        vehicleCopy.currQ = vehicleCopy.currQ - demand
    
    return expLenWithChoice(accumCost, vehicleCopy, route, Q, d)    

def plotProblems(problems):
    
    i = 0
    
    for p in problems:
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8,4), dpi=200)
    
        titleString = "Problem-"+str(i)
        xCoords =  map(lambda c: c.xCoor, p.customers)
        yCoords =  map(lambda c: c.yCoor, p.customers)
        boundaryLabel = "boundary"
        for c in p.clusters:
            for b in c.boundaries:
                y = sin(b)
                x = cos(b)
                cluster = plt.Line2D([0.0,x],[0.0,y], linewidth=1, linestyle = "--", color="green", label=boundaryLabel)
                ax.add_line(cluster)
                boundaryLabel = None

        ax.scatter(xCoords, yCoords, color="blue", label="customers")
        ax.scatter([p.depot.xCoor],[p.depot.yCoor], color="red", label="depot")
        

        ax.legend(loc=0)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(titleString)
        
        fig.tight_layout()
        fig.savefig("results/"+titleString+".png")
        i = i + 1

def aprioriPath(vehicle, route, Q, d):
    #TODO Calculate the route that the vehicle would take if
    #the average demand of the next node leads to failure.
    nop


def createVehicleWithRouteOfClients(clients):
    customers = []
    
    depot = Customer(0,0,0,Demand(0,0))
    
    customers.append(depot)
    
    for r in clients:
        customers.append(Customer(
            r[0],r[1][0],r[1][1],Demand(r[2][1],r[2][0])))

    customers.append(depot)
    #print customers
    v = Vehicle(0, customers, 0, customers[0])
    return v

def main(argv):
    
    #Parse comamnd line parameters
    i, o = parseParameters(argv)

    #Generate the problems and set it up
    problems = setup(i)

    #Solve them!
    for p in problems[:]:

        for f in p.clusters[:]:
            for v in f.vehicles[:]:
                cust = v.customers[:]

                print "Route: "+str(map(lambda c: c.ID, cust))
                expLen = expLenWithChoice(0,v,list(cust), p.Q,{})
                print "Expected Length Result "+str(expLen)
                print "\n"

    
    plotProblems(problems)



if __name__ == "__main__":
	main(sys.argv[1:])