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
	expLen = simSim.expLenCost(0, vehicle, vehicle.customers, Q, {})
	assert abs(expLen == 2.0)

def test_1_client_route_with_1_demand_above_Q():
	vehicle = createVehicleWithRouteOfClients([(1,(1,0),[3,6])])
	Q = 5
	expLen = simSim.expLenCost(0, vehicle, vehicle.customers, Q, {})
	assert abs(expLen == 2.5)

def test_2_client_route_with_route_failure():
	vehicle = createVehicleWithRouteOfClients([(1,(1,0),[2,4]),(2,(2,0),[2,4])])
	Q = 5
	expLen = simSim.expLenCost(0, vehicle, vehicle.customers, Q, {})
	assert abs(expLen - 5.77777) < 0.001

def test_3_client_route_with_route_failure_just_like_2():
	vehicle = createVehicleWithRouteOfClients([(1,(1,0),[3,5]),(2,(2,0),[3,5]),(3,(3,0),[1,3])])
	Q = 5
	expLen = simSim.expLenCost(0, vehicle, vehicle.customers, Q, {})
	assert abs(expLen - 11.11111111111) < 0.001

def test_1_node_excercise_6():
	vehicle = createVehicleWithRouteOfClients([(1,(0.28,0.97),[1,3])])
	Q = 5 
	expLen = simSim.expLenCost(0, vehicle, vehicle.customers, Q, {})
	assert abs(expLen - 2.01920776544) < 0.00000001

def test_2_nodes_excercise_6():
	vehicle = createVehicleWithRouteOfClients([(3,(0.52,0.55),[3,5]),(1,(0.28,0.97),[1,3])])
	Q = 5 
	expLen = simSim.expLenCost(0, vehicle, vehicle.customers, Q, {})
	assert abs(expLen - 3.32977734256) < 0.00000001

def test_3_nodes_excercise_6():
	vehicle = createVehicleWithRouteOfClients([(2,(0.7,0.4),[3,5]),(3,(0.52,0.55),[3,5]),(1,(0.28,0.97),[1,3])])
	Q = 5 
	expLen = simSim.expLenCost(0, vehicle, vehicle.customers, Q, {})
	assert abs(expLen - 4.63796108951) < 0.00000001

def test_4_nodes_excercise_6():
	vehicle = createVehicleWithRouteOfClients([(5, (0.71, 0.27),[3,5]),(2,(0.7,0.4),[3,5]),(3,(0.52,0.55),[3,5]),(1,(0.28,0.97),[1,3])])
	Q = 5 
	expLen = simSim.expLenCost(0, vehicle, vehicle.customers, Q, {})
	assert abs(expLen - 5.96971931052) < 0.00000001

def test_1_node_apriori():
	v = createVehicleWithRouteOfClients([(1, (1,0),[3,5])])
	Q = 5
	result = simSim.aprioriRoute(v, v.customers, Q)
	assert len(result) == 3

def test_2_node_apriori():
	v = createVehicleWithRouteOfClients([(1, (1,0),[3,5]), (2, (2,0),[3,5])])
	Q = 10
	result = simSim.aprioriRoute(v, v.customers, Q)
	assert len(result) == 4

def test_2_node_apriori_with_failure():
	v = createVehicleWithRouteOfClients([(1, (1,0),[3,5]), (2, (2,0),[3,5])])
	Q = 5
	result = simSim.aprioriRoute(v, v.customers, Q)
	assert len(result) == 5