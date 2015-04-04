from data import *


#Groups the customers in polar regions and distributes them between the vehicles.
#It assigns a vehicle only as much customers as the expected demand dictates per vehicle.
def distributeCustomersBetweenVehicles(expectedDemandPerVehicle, problem, vehicleQty):
    currDemand = 0
    vehicles = []
    tempCustomers = []
    ID = 0

    sortedCustomers = sorted(problem.customers, key=lambda c:c.angle)

    for customer in sortedCustomers:
        #Calculates the next step of demand as a scout
        postDemand = currDemand + customer.dem.exp_dem/2.0
        
        #If demand spills over, then this vehicle is done and we move to the next one
        if postDemand > expectedDemandPerVehicle:
            
            vehicles.append(Vehicle(ID,tempCustomers,currDemand,problem.depot))
            ID = ID + 1
            tempCustomers = [customer]
            currDemand = customer.dem.exp_dem
        else:
            tempCustomers.append(customer)
            currDemand = currDemand + customer.dem.exp_dem
    
    #If there is spill over and we are one vehicle short we spawn it
    if currDemand > 0 and len(vehicles) < vehicleQty:
        vehicles.append(Vehicle(ID,tempCustomers,currDemand,problem.depot))
    elif len(vehicles) == vehicleQty:
        #We already are maxed out of vehicles, so we just assign the remaining nodes
        lastVehicle = vehicles.pop()
        lastVehicle.customers.extend(tempCustomers)
        vehicles.append(lastVehicle)

    return vehicles

#Returns a list partitioned in n-size chunks
def chunk(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def assignFlotillas(vehicles):
    #Create pairs of vehicles
    vehicleGroups = list(chunk(vehicles, 2))
    
    #If its uneven, add it to the last pair and create a trio
    if len(vehicleGroups[-1]) == 1:

        lastVehicle = vehicleGroups.pop()
        vehicleGroups[-1].extend(lastVehicle)

    #Calculate the boundaries in radians between the vehicles
    boundaries = []
    for vG in vehicleGroups:
        subSetBoundaries = []
        for i in xrange(1, len(vG)):
            #Calculates the angle that is between the first and last vehicle.
            #If its a trio, it calculates two boundaries
            a = vG[i - 1].customers[-1].angle
            b = vG[i].customers[0].angle
            c = (a + b)/2.0
            subSetBoundaries.append(c)
        boundaries.append(subSetBoundaries)

    #Generate an ID array
    ids = xrange(0, len(boundaries))

    #All three arrays, IDs, Vehicle Groups and Boundaries are zipped together and a Flotilla is born!
    flotillas = map(lambda x: Flotilla(x[0],x[1],x[2]), zip(ids, vehicleGroups, boundaries))
    
    return flotillas
    

# **************************************************************************************
# OPTIMIZATION HEURISTICS
# **************************************************************************************

def sortCustomersByNearesNeighbor(vehicle):
    nearestCustomers = []
    remaining = list(vehicle.customers)
    #Depot
    origin = vehicle.currPos

    while remaining:
        sortedCustomers = sorted(remaining, key=lambda c: dist(origin,c))
        next = sortedCustomers.pop(0)
        nearestCustomers.append(next)
        i = remaining.index(next)
        del remaining[i]
        origin = nearestCustomers[-1]

    return nearestCustomers

def calcRouteCost(route):
    c = 0
    for i in xrange(0,len(route)-1):
        c = c + dist(route[i], route[i+1])
    return c

def twoOptFunction(route):
    improvement = True
    existing_route = route[:]
    while improvement:
        best_distance = calcRouteCost(existing_route)
        improvement = False
        for i in xrange(1,len(route) - 2):
            for k in xrange(i+1,len(route) -1):
                new_route = twoOptSwap(existing_route, i, k)
                new_distance = calcRouteCost(new_route)
                if (new_distance < best_distance):
                    existing_route = new_route[:]
                    improvement = True

    return existing_route

def twoOptSwap(route, i, k):
    new_route = route[:]
    new_route[i:k] = route[k-1:i-1:-1]
    return new_route

def twoOpt(vehicle):
    route = [vehicle.currPos]
    route.extend(vehicle.customers)
    route.append(vehicle.currPos)
    new_route = twoOptFunction(route)
    return new_route


#Optimizes the initial route with nearest neighbor and 2-opt. Modifies
#the route in place
def optimizeInitialRoute(vehicle):
    vehicle.customers = sortCustomersByNearesNeighbor(vehicle)
    vehicle.customers = twoOpt(vehicle)

#Groups the customers in polar regions ditributed evenly by the amount of vehicles
#Then it groups them together in flotillas
def clustering(problem, vehicleQty, expectedDemand):
    #Distribute demand per vehicle
    expectedDemandPerVehicle = (expectedDemand*(len(problem.customers)))/(vehicleQty*1.0)

    #Group customers in polar coordinates and ditribute them between the vehicles
    vehicles = distributeCustomersBetweenVehicles(expectedDemandPerVehicle, problem, vehicleQty)

    #Generate the groups of Vehicles that will work together in pairs or trios
    flotillas = assignFlotillas(vehicles)

    #Optimize the initial route of all vehicles. Add the depot to beginning and end
    #and optimize by nearest neighbor and 2-opt
    for f in flotillas:
        for v in f.vehicles:
            optimizeInitialRoute(v)

    #Returns the groups of vehicles that will be working close to each other
    return flotillas

def generateProblems(customerSets, vehicleQty, expectedDemand, routeFailure):
    
    problems = []

    for customers in customerSets:
        #Treat the depot differently and remove it from the customer list
        depot = customers[0]
        customers.pop(0)

        #Q is calculated for the entire problem
        Q = round(expectedDemand*(len(customers))/(vehicleQty*(routeFailure+1)))
         
        #Basic data is setup for the problem
        problem = Problem(customers, depot, Q)

        #Vehicles are distributed according to Demand in a polar groupings
        problem.flotillas = clustering(problem, vehicleQty, expectedDemand)

        #There are many problems parsed at the same time
        problems.append(problem)

    return problems

def setup(inputFile):

    vehicleQty = 11
    routeFailures = [0.75,1.25,1.75]
    expectedDemand = 3

    #Specify a number if you only want to tackle a single problem. Otherwise use None
    problemNumber = None

    #Read inputfile and generate customers
    customerSets = parseCustomerSets(inputFile)

    if problemNumber is not None:
        #Reduce the amount of problems to deal with if specified
        customerSets = customerSets[problemNumber:problemNumber+1]    
    
    #Problems are generated with basic paramenters
    problems = generateProblems(customerSets, vehicleQty, expectedDemand, routeFailures[0])
    

    return problems
