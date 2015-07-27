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
    inputNodes = ''
    ntimes = 0
    helpText = """
    	python simulation -i inputNodes -n times
        """
    try:
        opts, args = getopt.getopt(argv,"hi:n:",["iNodes=","ntimes="])
    except getopt.GetoptError:
        print helpText
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print helpText
            sys.exit()
        elif opt in ("-i", "--iNodes"):
            inputNodes = arg
        elif opt in ("-n", "--ntimes"):
            ntimes = arg

    if inputNodes == "":
        print helpText
        sys.exit(2)
    return inputNodes, ntimes

def callBichasProgram(input, problem, failure, delta, ntimes):
    #ARGS are name, number of nodes, problem instance, failure rate, delta, ntimes
    args = ['MVehiclesF.exe', input, problem, failure, delta, ntimes]
    DEVNULL = open(os.devnull, 'wb')
    pid = subprocess.call(args, stdout=DEVNULL) 
    return pid
    

#Levanta el file de output del prog de la bicha y saca un promedio
#entre todas las corridas entre apriori y rollout y explen y rollout
def processBichasOutput(inp, problem, failure, delta):
    bichasOutput = "Results/"+str(inp)+"Nodes/"+str(problem)+"/failure_"+failure+"_delta_"+str(delta)+"_results.txt"
    #print bichasOutput
    aprioriResults = []
    aprioriDeltas = []
    expLenDeltas = []
    
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
                vsExpLen = (exp1 + exp2 - bichita)/(exp1+exp2)
                vsApriori = (aprioriResults - bichita)/(aprioriResults)
                aprioriDeltas.append(vsApriori)
                expLenDeltas.append(vsExpLen)
            i = i + 1
    aprioAverage = sum(aprioriDeltas)/len(aprioriDeltas)
    expLenAve = sum(expLenDeltas)/len(expLenDeltas)
    result = (aprioAverage,expLenAve)
    #print "Result: "+str(result)
    return result

#Corre el programa de la bicha por cada instancia del problema, devuelve el promedio
#de mejora del algoritmo contra apriori y expLen
def simulate(inp, failure, delta, ntimes):
    aprioriresults = []
    expLenresults = []
    problems = 10
    for i in xrange(0, problems):
        callBichasProgram(inp,  str(i), str(failure), str(delta), ntimes)
        r = processBichasOutput(inp, i, str(failure), delta)
        aprioriresults.append(r[0])
        expLenresults.append(r[1])
    aprioriAverage = sum(aprioriresults)/len(aprioriresults)
    expLenAverage = sum(expLenresults)/len(expLenresults)
    return (aprioriAverage, expLenAverage)

def cleanup(nodes):
    import os, shutil
    folder_path = r"C:\Users\dgrandes\Documents\GitHub\faberge-egg\old-code-c\MVehicles Flex\Results\\"+str(nodes)+"Nodes"
    for file_object in os.listdir(folder_path):
        file_object_path = os.path.join(folder_path, file_object)
        if os.path.isfile(file_object_path):
            os.unlink(file_object_path)
        else:
            shutil.rmtree(file_object_path)
    for i in xrange(0,10):
        os.mkdir(folder_path+"/"+str(i))

def frange(x, y, jump):
  while x < y:
    yield x
    x += jump

def main(argv):
    os.chdir("C:\Users\dgrandes\Documents\GitHub\\faberge-egg\old-code-c\MVehicles Flex")
    #Parse comamnd line parameters
    i, ntimes = parseParameters(argv)
    #Clean up the previous folder
    cleanup(i)
    failures = [0.75,1.25,1.75]
    
    for x in failures:
        deltas = frange(0.0,100.0,10)
        results = []
        output = "Results/"+str(i)+"Nodes/"+"total_results_"+"failure_"+str(x)+"_"+ntimes+".txt"
        f = open(output,'w')
        f.write("delta,RolloutvsApriori,RolloutvsExplen\n")
        for delta in deltas:
            results = simulate(i,x,delta,ntimes)
            f.write(str(delta)+","+str(results[0])+","+str(results[1])+"\n")
        f.close()
if __name__ == "__main__":
	main(sys.argv[1:])