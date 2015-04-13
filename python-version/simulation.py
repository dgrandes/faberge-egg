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

#Calculates the route expected cost by averaging all possibilities of demand in each node
def expectedRouteLength(accumCost, vehicle, routeGiven, Q, d):
    
    route = routeGiven[:]

    if len(route) == 0:
        return accumCost

    currentNode = route.pop(0)
    withDepotCost = float("inf")
    withoutDepotCost = float("inf")

    distance = distCustomers(vehicle.currPos, currentNode)
    
    #If the result is in d, we use it instead of generating it again
    if currentNode.ID != 0 and (currentNode.ID,vehicle.currQ, len(route)) in d:
        #sys.stdout.write("Node result from cache: %d   \r" % (globalCounter) )
        #sys.stdout.flush()

        result = d[currentNode.ID, vehicle.currQ, len(route)]
        return result

    costs = []


    if currentNode.ID != 0:
        demGenerator = xrange(currentNode.dem.dmin, currentNode.dem.dmax+1)
    else:
        demGenerator = [0]


    for demand in demGenerator:
        #print ">>>--- NODE "+str(currentNode.ID)+", DEMAND:"+str(demand)+", Q:"+str(vehicle.currQ)+", Accum COST:"+str(accumCost)+" Route to go:"+str(route)
        #Necessary in order to prevent the curpos to modify the original vehicle
        
        vehicleCopy = pycopy(vehicle)
        vehicleCopy.currPos = currentNode
        #print "Q:"+str(vehicleCopy.currQ)+" Demand "+str(demand)+" in "+str(currentNode)
        routeCopy = route[:]
        withDepotCost = float("inf")
        withoutDepotCost = float("inf")
        
        #Normal Client
        if currentNode.ID != 0:
            #If we can't meet demand, we go back to the depot by force
            if vehicleCopy.currQ < demand:
                
                
                vehicleCopy.currQ = vehicleCopy.currQ - demand
                currentNodeCopy = pycopy(currentNode)
                currentNodeCopy.dem = Demand(0,0)
                #We set this node's demand in 0 as we have given him everything and went negative
                routeWithDepot = [routeCopy[-1],currentNodeCopy]+routeCopy[:]
                withDepotCost = expectedRouteLength(accumCost + distance, 
                    vehicleCopy, routeWithDepot, Q, d)    
            #We can evaluate both cases now, going to the depot or not
            else:        
                #We offload the truck!
                vehicleCopy.currQ = vehicleCopy.currQ - demand
                
                routeWithDepot = [routeCopy[-1]]+routeCopy[:]
                
                withoutDepotCost = expectedRouteLength(accumCost + distance,
                 vehicleCopy, routeCopy, Q, d)
                
                withDepotCost = expectedRouteLength(accumCost + distance,
                 vehicleCopy, routeWithDepot, Q, d)    
            
        #Depot, we just go to the next node after loading the truck
        elif currentNode.ID == 0:
            
            vehicleCopy.currQ = min(Q, vehicleCopy.currQ+Q)

            withoutDepotCost = expectedRouteLength(accumCost + distance,
             vehicleCopy, routeCopy, Q, d)
            
        minCost = min(withDepotCost, withoutDepotCost)

        costs.append(minCost)
        
        #print "              NODE "+str(currentNode.ID)+", DEMAND:"+str(demand)+", With Depot Cost: "+str(withDepotCost)+", withoutDepotCost:"+str(withoutDepotCost)+", Q:"+str(vehicleCopy.currQ)

    #print "<<<----- NODE "+str(currentNode.ID)+", COSTS"+str(costs)
    #print "\n"

    expectedCost = sum(costs)/len(costs)
    if currentNode.ID != 0:
        #Store the end result in the dictionary for further use
        d[(currentNode.ID, vehicle.currQ, len(route))] = expectedCost
    
    return expectedCost

#Route is expected to always end at the depot
def plotRouteWithExpectedDemand(accumCost, vehicle, routeGiven, Q, routeSoFar, d):
    route = routeGiven[:]
    if len(route) == 0:
        return accumCost, routeSoFar

    
    currentNode = route.pop(0)
    
    withDepotCost = float("inf")
    withoutDepotCost = float("inf")

    distance = distCustomers(vehicle.currPos, currentNode)

    #Necessary in order to prevent the others from modifying the original vehicle
    vehicleCopy = pycopy(vehicle)
    vehicleCopy.currPos = currentNode
    
    #If the result is in d, we use it instead of generating it again
    if currentNode.ID != 0 and (currentNode.ID,vehicleCopy.currQ) in d:
        results = d[currentNode.ID, vehicleCopy.currQ]
        return results[0], list(results[1])

    #Normal Client
    if currentNode.ID != 0:
        #If we can't meet demand, we go back to the depot by force
        if vehicleCopy.currQ < currentNode.dem.exp_dem:
            
            vehicleCopy.currQ = vehicleCopy.currQ - currentNode.dem.exp_dem

            #We have to set this exp_dem in 0, but we don't want the shared node
            currentNodeCopy = pycopy(currentNode)
            currentNodeCopy.dem.exp_dem = 0

            #We insert the copy in this route
            routeWithDepot = [route[-1],currentNodeCopy]+route[:]

            withDepotCost, soFarWithDepot = plotRouteWithExpectedDemand(accumCost + distance, 
                vehicleCopy, routeWithDepot, Q, routeSoFar+[currentNodeCopy], d)  

        #We can evaluate both cases now, going to the depot or not
        else:        
            #We offload the truck!
            vehicleCopy.currQ = vehicleCopy.currQ - currentNode.dem.exp_dem
            routeWithoutDepot = route[:]
            routeWithDepot = [route[-1]]+routeWithoutDepot[:]

            withoutDepotCost, soFarWithoutDepot = plotRouteWithExpectedDemand(accumCost + distance,
             vehicleCopy, routeWithoutDepot, Q, routeSoFar+[currentNode], d)

            withDepotCost, soFarWithDepot = plotRouteWithExpectedDemand(accumCost + distance,
             vehicleCopy, routeWithDepot, Q, routeSoFar+[currentNode], d) 
        
    #Depot, we just go to the next node after loading the truck
    elif currentNode.ID == 0:

        vehicleCopy.currQ = min(Q, vehicleCopy.currQ+Q)

        withoutDepotCost, soFarWithoutDepot = plotRouteWithExpectedDemand(accumCost + distance,
         vehicleCopy, route, Q, routeSoFar+[currentNode], d)
        
    minCost = min(withDepotCost, withoutDepotCost)

    if minCost == withoutDepotCost:
        routeSoFar = soFarWithoutDepot
    else:
        routeSoFar = soFarWithDepot
    
    #Store the end result in the dictionary for further use
    if currentNode.ID != 0:
        d[(currentNode.ID, vehicleCopy.currQ)] = (minCost, routeSoFar)

    return minCost, routeSoFar

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

def main(argv):
    
    #Parse comamnd line parameters
    i, o = parseParameters(argv)

    #Generate the problems and set it up
    problems = setup(i)

    #Solve them!
    for p in problems[:]:
        #pp.pprint(p)
        for f in p.clusters[:]:
            for v in f.vehicles[:]:
                cust = v.customers[:]
                #print cust
                #print "Route"
                #print str(map(lambda c: c.ID, cust))
                d = {}
                expLen = expectedRouteLength(0,v,list(cust), p.Q,{})
                #print d
                print "Expected Length Result "+str(expLen)
                print "\n"
                d = {}
                #routeCost, routePlot = plotRouteWithExpectedDemand(0,v,list(cust), p.Q, [], d)
                #pp.pprint(d)
                #print "Plot Route with Expected demand "+str(routeCost)
                #print str(map(lambda c: c.ID, routePlot))
                
                #print "\n"
    
    plotProblems(problems)


if __name__ == "__main__":
	main(sys.argv[1:])