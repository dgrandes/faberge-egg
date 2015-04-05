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
    coords = "("+str(self.xCoor)+","+str(self.yCoor)+"), angle: "+str(self.angle)
    return "Cust["+str(self.ID) +"]: dem:"+str(self.dem)

class Demand:
  def __init__(self, dmax, dmin):
    self.dmax = int(dmax)
    self.dmin= int(dmin)
    self.num=dmax-dmin+1
    self.exp_dem = (self.dmax + self.dmin) / 2.0
    self.currDemand = self.exp_dem

  def __repr__(self):
    return "["+str(self.dmin) +","+str(self.dmax)+"]"

class Vehicle:
  def __init__(self, ID, customers, currQ, currPos):
    self.ID = ID
    self.customers = customers
    self.currQ = currQ
    self.currPos = currPos

  def __repr__(self):
    return "V["+str(self.ID)+"]: Q:"+str(self.currQ)+", Cust:["+str(map(lambda c: "ID:"+str(c.ID)+",dem:"+str(c.dem), self.customers))+"]"

#Group of Vehicles that are in pairs or trios thar are part of the larger fleet
class Cluster:
  def __init__(self, ID, vehicles, boundaries):
    self.ID = ID
    self.vehicles = vehicles
    self.boundaries = boundaries

  def __repr__(self):
    return str("Cluster["+str(self.ID)+"]: Vehicles:{"+strArray(self.vehicles)+"}; Boundaires:"+strArray(self.boundaries))+""


class States:
  def __init__(self, currPos, demands, currCap):
    self.currPos = currPos
    self.demands = Demands
    self.currCap = currCap


def distCustomers(x,y):
  return hypot(y.xCoor-x.xCoor,y.yCoor-x.yCoor)

def calculateDistance(customers):
  distMatrix = [[0 for x in range(len(customers))] for x in range(len(customers))] 

  for i in xrange(0,len(customers)): 
    for j in xrange(i,len(customers)):
        distMatrix[i][j] = distCustomers(customers[i], customers[j])
        distMatrix[j][i] = distMatrix[i][j]

  return distMatrix

class Problem:
  def __init__(self, ID, customers, depot, Q):
    self.ID = ID
    self.customers = customers
    self.depot = depot
    self.Q = Q
    #self.distanceMatrix = calculateDistance(sorted(customers, key=lambda c: c.ID))
    self.clusters = []

  def __repr__(self):
    return str("Problem Instance: Quantity: "+str(self.Q)+", Clusters:\n"+strArray(self.clusters))










