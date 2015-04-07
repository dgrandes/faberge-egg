import setup as simSetup
import simulation as simSim
import elements as simElements

def createVehicleWithRouteOfClients(clients):
	customers = []
	
	depot = simElements.Customer(0,0,0,simElements.Demand(0,0))
	
	customers.append(depot)
	
	for r in clients:
		customers.append(simElements.Customer(
			r[0],r[1][0],r[1][1],simElements.Demand(r[2][1],r[2][0])))

	customers.append(depot)
	#print customers
	v = simElements.Vehicle(0, customers, 0, customers[0])
	return v
    

def test_1_client_route_with_demand_below_Q():
	vehicle = createVehicleWithRouteOfClients([(1,(1,0),[2,5])])
	Q = 8
	expLen = simSim.expectedRouteLength(0, vehicle, vehicle.customers, Q, {})
	assert expLen == 2.0

def test_1_client_route_with_demand_above_Q():
	vehicle = createVehicleWithRouteOfClients([(1,(1,0),[3,6])])
	Q = 5
	expLen = simSim.expectedRouteLength(0, vehicle, vehicle.customers, Q, {})
	assert expLen == 2.5

def test_1_client_route_with_demand_above_Q():
	vehicle = createVehicleWithRouteOfClients([(1,(1,0),[6,8])])
	Q = 5
	expLen = simSim.expectedRouteLength(0, vehicle, vehicle.customers, Q, {})
	assert expLen == 4.0

def test_2_client_route_with_demand_below_Q():
	vehicle = createVehicleWithRouteOfClients([(1,(1,0),[2,5]),(2,(2,0),[2,5])])
	Q = 8
	expLen = simSim.expectedRouteLength(0, vehicle, vehicle.customers, Q, {})
	assert expLen == 2.0