from setup import *
from copy import copy as pycopy

def dbp(string):
    if False:
        print string
        
#GO NO GO
def expLenWithChoice(accumCost, vehicleGiven, routeGiven, Q, d):
    route = routeGiven[:]
    vehicle = pycopy(vehicleGiven)
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
        return expLenWithChoice(accumCost, vehicle, route, Q, d)


    dbp("VEHICLE -> "+str(vehicle.currPos.ID)+",CURRENT NODE -> "+str(currentNode.ID)+", NEXT NODE -> "+str(route[0].ID)+", COST -> "+str(accumCost))
    
    #Moving the vehicle to the next node
    vehicle.currPos = currentNode

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
        updatedCost = accumCost + distanceToDepot + distCustomers(currentNode, route[-1])
        
        vehicleCopy.currQ = Q
        dbp("********")
        dbp("---8--> GO TO DEPOT BEFORE: "+str(route[0].ID) + ", CURRENT:"+str(currentNode.ID)+", WITH Q:"+str(vehicle.currQ)+", COST:"+str(accumCost))
        withDepotCost = analyzeExpectedCostForAllDemand(updatedCost, vehicleCopy, route, Q, d)
        dbp("<--8--- END OF GOING TO DEPOT BEFORE:"+str(route[0].ID) +", CURRENT: "+str(currentNode.ID)+", WITH Q:"+str(vehicle.currQ)+", COST:"+str(accumCost))
        dbp("********")
        dbp("\n")
    
    #Updating Accum Cost to reaching the new node
    accumCost = accumCost + distanceToAdd

    #I can always go straight
    if(len(route) > 1 ):
        dbp("******")
        dbp("----> STRAIGHT TO: "+str(route[0].ID)+" with Q:"+str(vehicle.currQ)+", COST:"+str(accumCost))
    
    withoutDepotCost = analyzeExpectedCostForAllDemand(accumCost, vehicle, route, Q, d)
    
    if(len(route) > 1 ):
        dbp("*******")
        dbp("<---- END OF STRAIGHT TO: "+str(currentNode.ID)+" with Q:"+str(vehicle.currQ)+", COST:"+str(accumCost))
        dbp("\n")
     
    if(len(route) >= 0 ):
        dbp("AT :"+str(currentNode.ID)+", CHOOSE BETWEEN :"+str(withDepotCost)+" vs "+str(withoutDepotCost)+", WITH Q:"+str(vehicle.currQ)+", COST:"+str(accumCost))
        dbp("\n")
    #Choose between Go, Not GO
    minCost = min(withDepotCost, withoutDepotCost)

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
        finalCost = accumCost + distCustomers(vehicle.currPos, route[-1])
        #print "FINAL COST:"+str(finalCost)
        return finalCost

    if (currentNode.ID,vehicle.currQ, accumCost) in d:

        result = d[currentNode.ID, vehicle.currQ, accumCost]
        dbp("Cache [ID:"+str(currentNode.ID)+", Q:"+str(vehicle.currQ)+", cost:"+str(accumCost)+"] -> "+str(result))
        return result

    #Costs for different Demands
    costsForAllDemands = []

    #Generate the demands in an array demands
    if currentNode.ID != 0:
        demands = xrange(currentNode.dem.dmin, currentNode.dem.dmax+1)
    else:
        demands = [0]

    
    for demand in demands:
        #print "----> EXPANDING:"+str(currentNode.ID) +", DEMAND: "+str(demand)+ ", COST: "+str(accumCost)
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
            dbp("FAILURE :"+str(vehicle.currQ) + " < "+str(demand))
            #The vehicle goes to the depot, and comes back and unloads the remaining part
            vehicleCopy.currQ = vehicleCopy.currQ - demand + Q
            #Update the accumulated cost due to failure
            accumCostAuxi = accumCost + 2 * distanceToDepot

        else:
            #update the Q of the vehicle
            vehicleCopy.currQ = vehicleCopy.currQ - demand

        #print "*******GOING TO EXPLEN with COST:" +str(accumCostAuxi)+" and Route:"+str(routeGiven) 
        #Updated Q and Cost, we proceed to the next node, deciding of course to visit the depot beforehand or not
        subCost = expLenWithChoice(accumCostAuxi, 
                    vehicleCopy, routeGiven, Q, d)    

        #Eventually, we will have known all the costs for each of our demands! We add them app to costs
        costsForAllDemands.append(subCost)
        
    dbp("---->NODE:"+str(currentNode)+" EXPECTED COSTS:"+str(costsForAllDemands))
    #The expected cost for all our demands is the average.
    expectedCost = sum(costsForAllDemands)/len(costsForAllDemands)

    
    #Store the end result in the dictionary for further use
    d[(currentNode.ID, vehicle.currQ, accumCost)] = expectedCost
    
    return expectedCost