
class Customer:
  def __init__(self, ID, xCoor, yCoor, dem):
    self.ID = ID
    self.xCoor = xCoor
    self.yCoor = yCoor
    self.dem = dem

class Demand:
  def __init__(self, dmax, dmin, num):
    self.dmax = dmax
    self.dmin= dmin
    self.num=dmax-dmin+1

class Vehicles:
  def __init__(self, ID, customers, currQ, currPos):
    self.ID = ID
    self.customers = customers
    self.currQ = currQ
    self.currPos = currPos

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









