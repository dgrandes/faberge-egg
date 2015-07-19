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

#GO NO GO
def expLenWithChoice(accumCost, vehicle, routeGiven, Q, d):
    route = routeGiven[:]

    if len(route) == 0:
        return accumCost

    currentNode = route[0]

    #If the vehicle is in the depot, load it up
    if currentNode.ID == 0:
        vehicle.currQ = Q

    

    distanceToAdd = distCustomers(vehicle.currPos, currentNode)
    distanceToDepot = distCustomers(vehicle.currPos, route[-1])
    
    if distCustomers(vehicle.currPos, currentNode) == 0:
        #advance the algo
        route.pop(0)
        expLenWithChoice(accumCost, vehicle, route, Q, d)

    print "VEHICLE -> "+str(vehicle.currPos.ID)+",NEXT NODE -> "+str(route[0].ID)+", COST -> "+str(accumCost)
    #Updating Accum Cost to reaching the new node
    accumCost = accumCost + distanceToAdd

    #Moving the vehicle to the next node
    vehicle.currPos = currentNode

    #The Distance to Depot is the same as the distance to add if we are out of nodes

    
    #print "distance to depot "+str(distanceToDepot)
    #print "v "+str(vehicle.currPos) + " route"+str(route)
    
    

    withDepotCost = float("inf")
    withoutDepotCost = float("inf")
    #If the next node is the depot, or I'm at the depot, then it makes no sense
    #to think about going there

    skipTheDepot = False

    if (vehicle.currQ == Q or route[0].ID == 0 or (currentNode.ID == 0)):
        skipTheDepot = True

    if not skipTheDepot:

        #If we go to the depot, the cost needs to include the trip and the vehicle now has Q
        vehicleCopy = pycopy(vehicle)
        updatedCost = accumCost + 2 * distanceToDepot
        vehicleCopy.currQ = Q
        print "GO TO DEPOT BEFORE: "+str(route[0].ID)
        withDepotCost = analyzeExpectedCostForAllDemand(updatedCost, vehicleCopy, route, Q, d)
        print "!!!! END OF GOING TO DEPOT AT:" +str(currentNode.ID)
        print "\n"
    #I can always go straight
    if(len(route) > 1 ):
        print "NO GO TO DEPOT BEFORE: "+str(route[0].ID)
    withoutDepotCost = analyzeExpectedCostForAllDemand(accumCost, vehicle, route, Q, d)
    if(len(route) > 1 ):
        print "!!!! END OF NO GO TO DEPOT AT: "+str(currentNode.ID)
        print "\n"
     
    if(len(route) > 1 ):
        print "AT :"+str(currentNode.ID)+", CHOOSE BETWEEN :"+str(withDepotCost)+" vs "+str(withoutDepotCost)
        print "\n"
    #Choose between Go, Not GO
    minCost = min(withDepotCost, withoutDepotCost)

#    d[(currentNode.ID, vehicle.currQ, len(route))] = minCost

    return minCost
        
                     
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
        return accumCost + distCustomers(vehicle.currPos, route[-1])

    if currentNode.ID != 0 and (currentNode.ID,vehicle.currQ, len(route)) in d:

        result = d[currentNode.ID, vehicle.currQ, len(route)]
        #print "Cache [ID:"+str(currentNode.ID)+", Q:"+str(vehicle.currQ)+"] -> "+str(result)
        return result

    #Costs for different Demands
    costsForAllDemands = []



    #Generate the demands in an array demands
    if currentNode.ID != 0:
        demands = xrange(currentNode.dem.dmin, currentNode.dem.dmax+1)
    else:
        demands = [0]

    
    for demand in demands:
        print "----> EXPANDING:"+str(currentNode.ID) +", DEMAND: "+str(demand)+ ", COST: "+str(accumCost)
        #Generate a vehicle per demand just in case
        vehicleCopy = pycopy(vehicle)

        #Copy the route just in case
        routeCopy = route[:]

        #Copy the accumulated cost
        accumCostAuxi = accumCost

        distanceToDepot = distCustomers(vehicleCopy.currPos, routeCopy[-1])
        #print '"Distance to depot '+str(distanceToDepot)

        #Assess if we fail and need to return to the depot and back
        if vehicleCopy.currQ < demand:
            print "FAILURE :"+str(vehicle.currQ) + " < "+str(demand)
            #The vehicle goes to the depot, and comes back and unloads the remaining part
            vehicleCopy.currQ = vehicleCopy.currQ - demand + Q
            #Update the accumulated cost due to failure
            accumCostAuxi = accumCost + 2 * distanceToDepot

        else:
            #update the Q of the vehicle
            vehicleCopy.currQ = vehicleCopy.currQ - demand

        #Updated Q and Cost, we proceed to the next node, deciding of course to visit the depot beforehand or not
        subCost = expLenWithChoice(accumCostAuxi, 
                    vehicleCopy, routeGiven, Q, d)    

        #Eventually, we will have known all the costs for each of our demands! We add them app to costs
        costsForAllDemands.append(subCost)
        
    print "---->NODE:"+str(currentNode)+" EXPECTED COSTS:"+str(costsForAllDemands)
    #The expected cost for all our demands is the average.
    expectedCost = sum(costsForAllDemands)/len(costsForAllDemands)

    if currentNode.ID != 0:
        #Store the end result in the dictionary for further use
        d[(currentNode.ID, vehicle.currQ, len(route))] = expectedCost
    
    return expectedCost

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
                expLen = expLenWithChoice(0,v,list(cust), p.Q,{})
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

def main2(argv):
    vehicle = createVehicleWithRouteOfClients([(1,(1,0),[2,4]),(2,(2,0),[2,4])])
    Q = 5
    expLen = expLenWithChoice(0, vehicle, vehicle.customers, Q, {})
    print expLen
    #assert expLen == 2.0


if __name__ == "__main__":
	main(sys.argv[1:])