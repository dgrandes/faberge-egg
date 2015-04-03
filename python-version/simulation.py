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

def main(argv):
    
    i, o = parseParameters(argv)

    problems = parseProblemInstances(i)
    
    for p in problems:
        print "Problem Instance:"
        for c in p:
            print c
        print "\n"


if __name__ == "__main__":
	main(sys.argv[1:])