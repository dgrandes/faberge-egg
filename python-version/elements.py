from math import atan2, pow, sqrt
import pprint

pp = pprint.PrettyPrinter(indent=4)

def strArray(array):
  #return str(reduce(lambda x,y: "\t"+str(x)+"\n"+str(y),array))
  return pp.pformat(array)

class Customer:
  def __init__(self, ID, xCoor, yCoor, dem):
    self.ID = ID
    self.xCoor = float(xCoor)
    self.yCoor = float(yCoor)
    self.dem = dem
    
    self.angle = atan2(self.yCoor, self.xCoor)

  def __repr__(self):
    return "Customer["+str(self.ID) +"]: ("+str(self.xCoor)+", "+str(self.yCoor)+") angle: "+str(self.angle)+", dem:"+str(self.dem)

class Demand:
  def __init__(self, dmax, dmin):
    self.dmax = float(dmax)
    self.dmin= float(dmin)
    self.num=dmax-dmin+1
    self.exp_dem = (self.dmax + self.dmin) / 2.0

  def __repr__(self):
    return "["+str(self.dmin) +","+str(self.dmax)+"]"

class Vehicle:
  def __init__(self, ID, customers, currQ, currPos):
    self.ID = ID
    self.customers = customers
    self.currQ = currQ
    self.currPos = currPos

  def __repr__(self):
    return "Vehicle["+str(self.ID)+"]: currQ:["+str(self.currQ)+"], currPos:["+str(self.currPos)+"], Vehicle Customers: \n"+strArray(self.customers)

#Group of Vehicles that are in pairs or trios thar are part of the larger fleet
class Flotilla:
  def __init__(self, ID, vehicles, boundaries):
    self.ID = ID
    self.vehicles = vehicles
    self.boundaries = boundaries

  def __repr__(self):
    return str("\nFlotilla["+str(self.ID)+"]: Vehicles:"+strArray(self.vehicles)+"\nBoundaires:"+strArray(self.boundaries))


class States:
  def __init__(self, currPos, demands, currCap):
    self.currPos = currPos
    self.demands = Demands
    self.currCap = currCap


def calculateDistance(customers):
  distMatrix = [[0 for x in range(len(customers))] for x in range(len(customers))] 
  for i in xrange(0,len(customers)): 
    for j in xrange(i,len(customers)):
        distMatrix[i][j] = sqrt((pow(customers[j].xCoor - customers[i].xCoor, 2) + (pow(customers[j].yCoor - customers[i].yCoor, 2))))
        distMatrix[j][i] = distMatrix[i][j]
        
  return distMatrix

class Problem:
  def __init__(self, customers, depot, Q):
    self.customers = customers
    self.depot = depot
    self.Q = Q
    self.distanceMatrix = calculateDistance(customers)

  def __repr__(self):
    return str("Problem Instance: Quantity: "+str(self.Q)+", Depot:"+str(self.depot)+", Customers:"+strArray(self.customers))










