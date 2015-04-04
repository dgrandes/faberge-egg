import os, sys, getopt
from setup import *
from copy import *
import pprint
from random import randint


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



#Route is expected to always end at the depot
def expectedLength(accumCost, vehicle, route, Q, routeSoFar, d):

    if len(route) == 0:
        return accumCost, routeSoFar


    currentNode = route.pop(0)
    
    withDepotCost = float("inf")
    withoutDepotCost = float("inf")

    distance = dist(vehicle.currPos, currentNode)

    #Necessary in order to prevent the curpos to modify the original vehicle
    vehicleCopy = copy(vehicle)
    vehicleCopy.currPos = currentNode
    
    if (currentNode.ID,vehicleCopy.currQ) in d:
        results = d[currentNode.ID, vehicleCopy.currQ]
        return results[0], list(results[1])

    #Normal Client
    if currentNode.ID != 0:
        #If we can't meet demand, we go back to the depot by force
        if vehicleCopy.currQ < currentNode.dem.exp_dem:
            
            vehicleCopy.currQ = vehicleCopy.currQ - currentNode.dem.exp_dem
            routeWithDepot = [route[-1],currentNode]+route[:]
            withDepotCost, soFarWithDepot = expectedLength(accumCost + distance, 
                vehicleCopy, routeWithDepot, Q, routeSoFar+[currentNode], d)    
        #We can evaluate both cases now, going to the depot or not
        else:        
            #We offload the truck!
            vehicleCopy.currQ = vehicleCopy.currQ - currentNode.dem.exp_dem
            routeWithDepot = [route[-1]]+route[:]
            withoutDepotCost, soFarWithoutDepot = expectedLength(accumCost + distance,
             vehicleCopy, route, Q, routeSoFar+[currentNode], d)
            withDepotCost, soFarWithDepot = expectedLength(accumCost + distance,
             vehicleCopy, routeWithDepot, Q, routeSoFar+[currentNode], d)    
        
    #Depot, we just go to the next node after loading the truck
    elif currentNode.ID == 0:

        vehicleCopy.currQ = min(Q, vehicleCopy.currQ+Q)
        withoutDepotCost, soFarWithoutDepot = expectedLength(accumCost + distance,
         vehicleCopy, route, Q, routeSoFar+[currentNode], d)
        #print "IN DEPOT -> WITHOUT DEPOT COST:"+str(withoutDepotCost)
    minCost = min(withDepotCost, withoutDepotCost)
    if minCost == withoutDepotCost:
        routeSoFar = soFarWithoutDepot
    else:
        routeSoFar = soFarWithDepot
    
    #Store the end result int eh dictionary for further use
    d[(currentNode.ID, vehicleCopy.currQ)] = (minCost, routeSoFar)
    return minCost, routeSoFar

def main(argv):
    
    #Parse comamnd line parameters
    i, o = parseParameters(argv)

    #Generate the problems and set it up
    problems = setup(i)

    #Solve them!
    for p in problems[:]:
        pp.pprint(p)
        for f in p.flotillas[:]:
            for v in f.vehicles[:]:
                cust = v.customers[:]
                print "Route"
                print str(map(lambda c: c.ID, cust))
                print cust
                d = {}
                le, rt = expectedLength(0,v,list(cust), p.Q, [], {})
                print "Route Result"
                print str(map(lambda c: c.ID, rt))
                


if __name__ == "__main__":
	main(sys.argv[1:])