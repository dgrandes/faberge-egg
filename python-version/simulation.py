import os, sys, getopt
from setup import *
import pprint
from random import randint
import timing
from expLen import *
from plotter import *

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

def simulate(problem):
    for f in problem.clusters[:]:
        print str(f)
        aprioriRoutes = []
        for v in f.vehicles[:]:
            apriori = aprioriRoute(v, v.customers, problem.Q)
            
            print str(map(lambda c: c.ID, apriori))
            aprioriRoutes.append(apriori)
            cust = v.customers[:]
            #print cust
            print "Route"
            print str(map(lambda c: c.ID, cust))

            # expLenRoute = []
            # for i in len(cust):
            #     decision = expLenChoice(0, v, cust[i:], problem.Q, {})
            #     expLenRoute.append(e)
            # decision = expLenChoice(
            # print "decision :"+str(decision)

            #print p.Q
            d = {}
            expLen = expLenCost(0,v,list(cust), problem.Q,{})
            #print d
            print "Expected Length Result "+str(expLen)
            print "\n"
            d = {}


def main(argv):
    
    #Parse comamnd line parameters
    i, o = parseParameters(argv)

    #Generate the problems and set it up
    problems = setup(i)

    #Solve them!
    for p in problems[:]:
        #pp.pprint(p)
        simulate(p)
    
    plotProblems(problems)



if __name__ == "__main__":
	main(sys.argv[1:])