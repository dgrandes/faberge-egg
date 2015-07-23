from setup import *
from copy import copy as pycopy


def aprioriRoute(vehicle, route, Q):	
	
	result = []
	depot = route[-1]

	for node in route:
		if node.ID == depot.ID:
			vehicle.currQ = Q
			result.append(depot)
		else:
			if vehicle.currQ >= node.dem.exp_dem:
				vehicle.currQ = vehicle.currQ - node.dem.exp_dem
				result.append(node)
			else:
				vehicle.currQ = Q
				result.append(depot)
				result.append(node)
	return result


def expLen(accumCost, vehicleGiven, routeGiven, Q, d):

    route = routeGiven[:]
    vehicle = pycopy(vehicleGiven)
    if len(route) == 0:
        return accumCost

    nextNode = route[0]

    #If the vehicle is already at the next node, just advance the route
    if vehicle.currPos.ID == nextNode.ID:
        #advance the algo
        route.pop(0)
        return expLen(accumCost, vehicle, route, Q, d)

    #If the vehicle is in the depot, load it up
    if vehicle.currPos.ID == 0:
        vehicle.currQ = Q

    withDepotCost = goToDepot(vehicle, nextNode, accumCost, route, Q, d)        
    withoutDepotCost = goStraight(vehicle, nextNode, accumCost, route, Q, d)
    return (withDepotCost, withoutDepotCost)

def expLenChoice(accumCost, vehicleGiven, routeGiven, Q, d):
	t = expLen(accumCost, vehicleGiven, routeGiven, Q, d)
	withDepotCost = t[0]
	withoutDepotCost = t[1]

	if withDepotCost < withoutDepotCost:
		return routeGiven[-1]
	else:
		return routeGiven[0]

#GO NO GO
def expLenCost(accumCost, vehicleGiven, routeGiven, Q, d):

    t = expLen(accumCost, vehicleGiven, routeGiven, Q, d)
    withDepotCost = t[0]
    withoutDepotCost = t[1]
    #Choose between Go, Not GO
    minCost = min(withDepotCost, withoutDepotCost)

    return minCost

def goToDepot(vehicle, nextNode, accumCost, route, Q, d):
    withDepotCost = float("inf")

    vehicleCopy = pycopy(vehicle)
    
    distanceToDepot = distCustomers(vehicle.currPos, route[-1])
    distanceFromDepotToNext = distCustomers(nextNode, route[-1])
    #Don't go to the depot if Im there or coming from there, or going there next
    if not (vehicle.currQ == Q or nextNode.ID == 0):
        #If we go to the depot, the cost needs to include the trip
        accumCost = accumCost + distanceToDepot + distanceFromDepotToNext

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
    distanceToNextNode = distCustomers(vehicleCopy.currPos, nextNode)

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

    if (currentNode.ID,vehicle.currQ, accumCost) in d:
        result = d[currentNode.ID, vehicle.currQ, accumCost]
        return result

    #Generate the demands in an array demands
    demands = xrange(currentNode.dem.dmin, currentNode.dem.dmax+1)
    costsForAllDemands = []

    for demand in demands:
    	subCost = satisfyDemand(demand, vehicle, accumCost, route, Q, d)
        #Eventually, we will have known all the costs for each of our demands! We add them app to costs
        costsForAllDemands.append(subCost)
        
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
    
    return expLenCost(accumCost, vehicleCopy, route, Q, d)    
