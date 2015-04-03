import os, sys, getopt
from data import *
import pprint

pp = pprint.PrettyPrinter(indent=4)

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



def generateProblems(customerSets, vehicleQty, expectedDemand, routeFailure):
    
    problems = []

    for customers in customerSets:
        depot = customers[0]
        customers.pop(0)

        Q = round(expectedDemand*(len(customers))/(vehicleQty*(routeFailure+1)))
        sortedCustomers = sorted(customers, key=lambda c:c.angle)
        problems.append(Problem(sortedCustomers, depot, Q))

    return problems

def distributeCustomersBetweenVehicles(expectedDemandPerVehicle, problem, vehicleQty):
    currDemand = 0
    vehicles = []
    tempCustomers = []
    ID = 0

    for customer in problem.customers:
        postDemand = currDemand + customer.dem.exp_dem/2.0
        
        if postDemand > expectedDemandPerVehicle:
            
            vehicles.append(Vehicle(ID,tempCustomers,currDemand,problem.depot))
            ID = ID + 1
            tempCustomers = [customer]
            currDemand = customer.dem.exp_dem
        else:
            tempCustomers.append(customer)
            currDemand = currDemand + customer.dem.exp_dem
        
    if currDemand > 0 and len(vehicles) < vehicleQty:
        vehicles.append(Vehicle(ID,tempCustomers,currDemand,problem.depot))
    else:
        lastVehicle = vehicles.pop()
        lastVehicle.customers.extend(tempCustomers)
        vehicles.append(lastVehicle)

    return vehicles

def chunk(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def assignFlotillas(vehicles):
 
    vehicleGroups = list(chunk(vehicles, 2))
    
    if len(vehicleGroups[-1]) == 1:

        lastVehicle = vehicleGroups.pop()
        vehicleGroups[-1].extend(lastVehicle)

    boundaries = []
    for vG in vehicleGroups:
        subSetBoundaries = []
        for i in xrange(1, len(vG)):
            a = vG[i - 1].customers[-1].angle
            b = vG[i].customers[0].angle
            c = (a + b)/2.0
            subSetBoundaries.append(c)
        boundaries.append(subSetBoundaries)

    ids = xrange(0, len(boundaries))

    flotillas = map(lambda x: Flotilla(x[0],x[1],x[2]), zip(ids, vehicleGroups, boundaries))
    
    return flotillas
    

def clustering(problem, vehicleQty, expectedDemand):
    expectedDemandPerVehicle = (expectedDemand*(len(problem.customers)))/(vehicleQty*1.0)
    vehicles = distributeCustomersBetweenVehicles(expectedDemandPerVehicle, problem, vehicleQty)


    flotillas = assignFlotillas(vehicles)
    return flotillas


def main(argv):
    
    i, o = parseParameters(argv)

    vehicleQty = 11
    routeFailures = [0.75,1.25,1.75]
    expectedDemand = 3

    customerSets = parseCustomerSets(i)
    problems = generateProblems(customerSets, vehicleQty, expectedDemand, routeFailures[0])
    

    for problem in problems[0:1]:
        
        pp.pprint(problem)
        flotillas = clustering(problem, vehicleQty, expectedDemand)
        print "\nFlotillas\n"
        for f in flotillas:
            pp.pprint(f)
        


if __name__ == "__main__":
	main(sys.argv[1:])