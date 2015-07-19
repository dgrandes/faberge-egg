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
        result = d[currentNode.ID, vehicle.currQ, len(route)]
        return result


    vehicleCopy = pycopy(vehicle)
    vehicleCopy.currPos = currentNode
        

    if (len(route) > 1):
        routeWithDepot = [route[-1]]+route[:]
        withDepotCost = expectedRouteLengthCalc(accumCost+distance, 
            vehicleCopy, routeWithDepot, Q, d)

    withoutDepotCost = expectedRouteLengthCalc(accumCost + distance,
        vehicleCopy, route, Q, d)

    minCost = min(withDepotCost, withoutDepotCost)

    return minCost
        
                     
#Calculates the route expected cost by averaging all possibilities of demand in each node
def expectedRouteLengthCalc(accumCost, vehicle, routeGiven, Q, d):
    
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
        print ">>>--- NODE "+str(currentNode.ID)+", DEMAND:"+str(demand)+", Q:"+str(vehicle.currQ)+", Accum COST:"+str(accumCost+distance)+" Route to go:"+str(route)
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
                
                
                #We substact the full amount, go negative and then assume we want back to the depot
                vehicleCopy.currQ = vehicleCopy.currQ - demand + Q
                #We add the cost of going to the depot and coming back
                #print "ACCUM COST RIGHT NOW: " + str(accumCost + distance)
                #print "DIST TO ADD "+str(distCustomers(vehicleCopy.currPos,routeCopy[-1]))
                accumCostAuxi = accumCost + 2 * distCustomers(vehicleCopy.currPos,routeCopy[-1])
                #print "ACCUM COST AFTER RUPUTRA: " + str(accumCost + distance)
                #We set the current demand of the node in 0 as it is done.
                currentNodeCopy = pycopy(currentNode)
                currentNodeCopy.dem = Demand(0,0)
                
                
                withoutDepotCost = expectedRouteLength(accumCostAuxi + distance, 
                    vehicleCopy, routeCopy, Q, d)    
            #We can evaluate both cases now, going to the depot or not
            else:        
                #We offload the truck!
                vehicleCopy.currQ = vehicleCopy.currQ - demand
                
                if len(routeCopy) > 1:
                    routeWithDepot = [routeCopy[-1]]+routeCopy[:]
                else:
                    routeWithDepot = routeCopy[:]
                
                withoutDepotCost = expectedRouteLength(accumCost + distance,
                 vehicleCopy, routeCopy, Q, d)
                
                #if (len(routeCopy) > 1):
                 #   print "***********YENDO AL DEPOSITO con RUTA "+str(routeWithDepot)+"*************"
                withDepotCost = expectedRouteLength(accumCost + distance,
                    vehicleCopy, routeWithDepot, Q, d)    
            
        #Depot, we just go to the next node after loading the truck
        elif currentNode.ID == 0:
            
            vehicleCopy.currQ = min(Q, vehicleCopy.currQ+Q)

            withoutDepotCost = expectedRouteLength(accumCost + distance,
             vehicleCopy, routeCopy, Q, d)
            
        minCost = min(withDepotCost, withoutDepotCost)

        costs.append(minCost)
        
    print "??????NODE "+str(currentNode.ID)+", DEMAND:"+str(demand)+", With Depot Cost: "+str(withDepotCost)+", withoutDepotCost:"+str(withoutDepotCost)+", Q:"+str(vehicleCopy.currQ)

    print "<<<----- NODE "+str(currentNode.ID)+", COSTS"+str(costs)
    print "\n"

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
        pp.pprint(p)
        for f in p.clusters[:]:
            for v in f.vehicles[:]:
                cust = v.customers[0:1]+v.customers[-4:]
                print cust
                print "Route"
                print str(map(lambda c: c.ID, cust))
                print p.Q
                d = {}
                expLen = expectedRouteLength(0,v,list(cust), p.Q,{})
                print d
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