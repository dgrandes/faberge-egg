import os, sys, getopt
from data import *

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

def clustering(problem, vehicleQty, expectedDemand):
    expectedDemandPerVehicle = (expectedDemand*(len(problem.customers)))/(vehicleQty*1.0)
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



def main(argv):
    
    i, o = parseParameters(argv)

    vehicleQty = 2
    routeFailures = [0.75,1.25,1.75]
    expectedDemand = 3

    customerSets = parseCustomerSets(i)
    problems = generateProblems(customerSets, vehicleQty, expectedDemand, routeFailures[0])
    

    for problem in problems[0:1]:
        print "Problem Instance:"
        print problem
        vehicles = clustering(problem, vehicleQty, expectedDemand)
        print "\nVehicles"
        for v in vehicles:
            print v
        print "\n"


if __name__ == "__main__":
	main(sys.argv[1:])