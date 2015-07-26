import os, sys, getopt
from setup import *
import pprint
from random import randint
import timing
from expLen import *
import subprocess
#from plotter import *

pp = pprint.PrettyPrinter(indent=2)

def parseParameters(argv):
    inputfile = ''
    outputfile = ''
    ntimes = 0
    helpText = """
    	python simulation -i inputfile -n times -q instances -o outputfile
        """
    try:
        opts, args = getopt.getopt(argv,"hi:n:o:",["ifile=","ntimes=","ofile="])
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
        elif opt in ("-n", "--ntimes"):
            ntimes = arg

    if inputfile == "" or outputfile == "":
        print helpText
        sys.exit(2)
    return inputfile, outputfile, ntimes

def callBichasProgram(input, problem, delta, ntimes):
    args = ['MVehiclesF.exe', input, problem, delta, ntimes]
    DEVNULL = open(os.devnull, 'wb')
    pid = subprocess.call(args, stdout=DEVNULL) 
    return pid
    

#Levanta el file de output del prog de la bicha y saca un promedio
#entre todas las corridas entre apriori y rollout y explen y rollout
def processBichasOutput(bichasOutput):
    aprioriResults = []
    aprioriDeltas = set()
    expLenDeltas = set()
    
    with open(bichasOutput, 'rU') as f:
        i = 0
        for line in f:
            l = line.split("/")
            #print l
            if i == 0:
                aprioriResults = float(l[0]) + float(l[1])
            else:
                exp1 = float(l[0])
                exp2 = float(l[1])
                bichita =  float(l[2])
                vsExpLen = exp1 + exp2 - bichita
                vsApriori = aprioriResults - bichita
                aprioriDeltas.add(vsApriori)
                expLenDeltas.add(vsExpLen)
            i = i + 1
    aprioAverage = sum(aprioriDeltas)/len(aprioriDeltas)
    expLenAve = sum(expLenDeltas)/len(expLenDeltas)
    result = (aprioAverage/(aprioriResults), expLenAve/(exp1+exp2))
    #print "Result: "+str(result)
    return result

#Corre el programa de la bicha por cada instancia del problema, devuelve el promedio
#de mejora del algoritmo contra apriori y expLen
def simulate(input, delta, ntimes):
    aprioriresults = []
    expLenresults = []
    problems = 10
    for i in xrange(0, problems):
        callBichasProgram(input, str(i), str(delta), ntimes)
        r = processBichasOutput("results.txt")
        aprioriresults.append(r[0])
        expLenresults.append(r[1])
    aprioriAverage = sum(aprioriresults)/len(aprioriresults)
    expLenAverage = sum(expLenresults)/len(expLenresults)
    return (aprioriAverage, expLenAverage)


def frange(x, y, jump):
  while x < y:
    yield x
    x += jump

def main(argv):
    

    os.chdir("C:\Users\dgrandes\Documents\GitHub\\faberge-egg\old-code-c\MVehicles Flex")
    #Parse comamnd line parameters
    i, o, ntimes = parseParameters(argv)
    instances = 10
    deltas = frange(0.5,1.5,0.1)
    print "delta,Rollout vs Apriori,Rollout vs Explen"
    results = []

    string = ''
    for delta in deltas:
        results = simulate(i,delta,ntimes)
        print str(delta)+","+str(results[0])+","+str(results[1])
        




if __name__ == "__main__":
	main(sys.argv[1:])