#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
# from json import jsonlines
import numpy as np
#######################
# 打造世界上最完美的机器人
#######################


from xlwings import xrange

#
# ls = [1,3,2,9,9,3]
# ls.remove(9)
# print(sorted(ls))
# ls = sorted(ls)
# print(ls)
#

x = {(1,2):2, (3,4):4}
print(x)


##########
#or tools相关
##########
# node = [1, 2, 3, 4]
# for val in xrange(len(node)):
#     print(val)


order_path = "./algorithm/data_interaction/unallocated_order_items.json"

# f = open(order_path, 'r', encoding='utf-8')
# lines = f.read()
# f.close()

# lines_json = lines.replace('},', '}')
# n = open(order_path, 'w', encoding='utf-8')
# n.write(lines_json)
# n.close()

with open(order_path, 'r+', encoding='utf-8') as jsonfile:
    lines = jsonfile.read()
    orders = json.loads(lines)

for order in orders:
    print(order)


# data = np.array(rows)



data = {}
### 1.车辆每个路径点上的装载量
data['demands'] = [0, 1, 1, 2]

# 车辆装载起点；
data['vehicle_capacities'] = [15, 15, 15, 15]

# 辆车的装载量；
manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                       data['num_vehicles'], data['depot'])
routing = pywrapcp.RoutingModel(manager)


def demand_callback(from_index):
    from_node = manager.IndexToNode(from_index)
    return data['demands'][from_node]


demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
routing.AddDimensionWithVehicleCapacity(demand_callback_index,
                                        0, data['vehicle_capacities'], True, 'Capacity')

###   2.里程计约束
data['pickups_deliveries'] = [[1, 6], [2, 10], [4, 3], [5, 9], [7, 8], [15, 11], [13, 12], [16, 14], ]


# ["pick_location", "delivery_location"]


def distance_callback(from_index, to_index):
    """Returns the distance between the two nodes."""
    # Convert from routing variable Index to distance matrix NodeIndex.
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data['distance_matrix'][from_node][to_node]


transit_callback_index = routing.RegisterTransitCallback(distance_callback)

routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
dimension_name = 'Distance'
routing.AddDimension(
    transit_callback_index,
    0,  # no slack
    3000,  # vehicle maximum travel distance
    True,  # start cumul to zero
    dimension_name)
distance_dimension = routing.GetDimensionOrDie(dimension_name)
distance_dimension.SetGlobalSpanCostCoefficient(100)

for request in data['pickups_deliveries']:
    pickup_index = manager.NodeToIndex(request[0])
    delivery_index = manager.NodeToIndex(request[1])
    routing.AddPickupAndDelivery(pickup_index, delivery_index)
    routing.solver().Add(
        routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index))
    routing.solver().Add(
        distance_dimension.CumulVar(pickup_index) <= distance_dimension.CumulVar(delivery_index))


# 3.承诺完成时间约束


def create_data_model():
    data = {}
    data['time_matrix'] = ["时间距离矩阵"]
    data['time_windows'] = [
        (0, 5)]  # depot(7, 12),  # 1(10, 15),        # 2(16, 18),  # 3(10, 13),  # 4]   [创建时间，承诺完成时间]
    data['num_vehicles'] = 4
    data['depot'] = 0
    return data


def time_callback(from_index, to_index):
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data['time_matrix'][from_node][to_node]


transit_callback_index = routing.RegisterTransitCallback(time_callback)
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
# 回调时间距离代价

time = 'Time'
routing.AddDimension(transit_callback_index,
                     30,  # allow waiting time
                     30,  # maximum time per vehicle
                     False,  # Don't force start cumul to zero.
                     time)



time_dimension = routing.GetDimensionOrDie(time)
# Add time window constraints for each location except depot.
for location_idx, time_window in enumerate(data['time_windows']):
    if location_idx == data['depot']:
        continue
    index = manager.NodeToIndex(location_idx)
    time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
# Add time window constraints for each vehicle start node.
depot_idx = data['depot']
for vehicle_id in range(data['num_vehicles']):
    index = routing.Start(vehicle_id)
    time_dimension.CumulVar(index).SetRange(
        data['time_windows'][depot_idx][0],
        data['time_windows'][depot_idx][1])
for i in range(data['num_vehicles']):
    routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.Start(i)))
    routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.End(i)))


