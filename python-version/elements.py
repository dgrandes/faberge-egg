from math import atan2

def strArray(array):
  return str(reduce(lambda x,y: str(x)+"\n"+str(y),array))

class Customer:
  def __init__(self, ID, xCoor, yCoor, dem):
    self.ID = ID
    self.xCoor = float(xCoor)
    self.yCoor = float(yCoor)
    self.dem = dem
    
    self.angle = atan2(self.yCoor, self.xCoor)

  def __str__(self):
    return "Cust "+str(self.ID) +": ("+str(self.xCoor)+", "+str(self.yCoor)+") angle: "+str(self.angle)+", dem:"+str(self.dem)+""

class Demand:
  def __init__(self, dmax, dmin):
    self.dmax = float(dmax)
    self.dmin= float(dmin)
    self.num=dmax-dmin+1
    self.exp_dem = (self.dmax + self.dmin) / 2.0

  def __str__(self):
    return "["+str(self.dmin) +","+str(self.dmax)+"]"

class Vehicle:
  def __init__(self, ID, customers, currQ, currPos):
    self.ID = ID
    self.customers = customers
    self.currQ = currQ
    self.currPos = currPos

  def __str__(self):
    return "Vehicle "+str(self.ID)+"\ncurrQ:["+str(self.currQ)+"], currPos:["+str(self.currPos)+"], Vehicle Customers: \n"+strArray(self.customers)

class Pairs:
  def __init__(self, ID, vehicles, line):
    self.ID = ID
    self.vehicles = vehicles
    self.line=line

class Trios:
  def __init__(self, vehicles, line):
    self.vehicles = vehicles
    self.line = line

class States:
  def __init__(self, currPos, demands, currCap):
    self.currPos = currPos
    self.demands = Demands
    self.currCap = currCap


class Problem:
  def __init__(self, customers, depot, Q):
    self.customers = customers
    self.depot = depot
    self.Q = Q

  def __str__(self):
    return str("Quantity: "+str(self.Q)+"\nDepot:"+str(self.depot)+"\nCustomers:\n"+strArray(self.customers))










