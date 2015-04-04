from math import atan2, pow, sqrt, hypot
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
    return "(Cust["+str(self.ID) +"]: ("+str(self.xCoor)+","+str(self.yCoor)+"), angle: "+str(self.angle)+", dem:"+str(self.dem)+")"

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
    return "V["+str(self.ID)+"]: Q:"+str(self.currQ)+", Cust:["+str(map(lambda c: c.ID, self.customers))+"]"

#Group of Vehicles that are in pairs or trios thar are part of the larger fleet
class Flotilla:
  def __init__(self, ID, vehicles, boundaries):
    self.ID = ID
    self.vehicles = vehicles
    self.boundaries = boundaries

  def __repr__(self):
    return str("Flotilla["+str(self.ID)+"]: Vehicles:{"+strArray(self.vehicles)+"}; Boundaires:"+strArray(self.boundaries))+""


class States:
  def __init__(self, currPos, demands, currCap):
    self.currPos = currPos
    self.demands = Demands
    self.currCap = currCap


def dist(x,y):
  return hypot(y.xCoor-x.xCoor,y.yCoor-x.yCoor)

def calculateDistance(customers):
  distMatrix = [[0 for x in range(len(customers))] for x in range(len(customers))] 

  for i in xrange(0,len(customers)): 
    for j in xrange(i,len(customers)):
        distMatrix[i][j] = dist(customers[i], customers[j])
        distMatrix[j][i] = distMatrix[i][j]

  return distMatrix

class Problem:
  def __init__(self, customers, depot, Q):
    self.customers = customers
    self.depot = depot
    self.Q = Q
    #self.distanceMatrix = calculateDistance(sorted(customers, key=lambda c: c.ID))
    self.flotillas = []

  def __repr__(self):
    return str("Problem Instance: Quantity: "+str(self.Q)+", Flotillas:\n"+strArray(self.flotillas))










