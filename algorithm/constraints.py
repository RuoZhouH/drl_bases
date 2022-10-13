# -*- coding: utf-8 -*-

from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import numpy as np
import csv
from xlwings import xrange
from floyd import *
import json
import time
INF_val = 9999


class Prepare_Data():
    def __init__(self, json_path1, json_path2, json_path3):
        self.map_path = json_path1
        self.order_path = json_path2
        self.vehicles_path = json_path3
        self.node = []
        self.orders = []
        # self.starts = []    # 带有任务小车的起点
        # self.ends = []      # 带有任务小车的终点
        self.data = {}

    def generate_distance_matrix(self):
        """
        根据map数据生成距离、时间矩阵
        :return:
        """
        with open(self.map_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            rows = [row for row in reader]
        data = np.array(rows)
        factory_id_set = set()
        for l in data[1:]:
            factory_id_set.add(l[1])
            factory_id_set.add(l[2])
        factory_id_unique = sorted(list(factory_id_set))

        n = len(factory_id_unique)  # 154个节点

        factory_id_map = {}
        factory_id_map_opposite = {}
        for i in range(n):
            factory_id_map[i] = factory_id_unique[i]
            factory_id_map_opposite[factory_id_unique[i]] = i

        # 排序factory_id，并建立(u, v, cost)
        factory_distance = []
        factory_time = []
        factory_id = []
        for l in data[1:]:
            # u, v, time
            factory_id.append([factory_id_map_opposite[l[1]], factory_id_map_opposite[l[2]], l[4]])
            factory_distance.append((l[1], l[2], float(l[3])))
            factory_time.append((l[1], l[2], int(l[4])))
        # factory_id = sorted(factory_id, key=lambda x: (x[0], x[1]))

        node = factory_id_unique

        node_list = factory_distance

        node_list_time = factory_time

        # node_map[i][j] 存储i到j的最短距离
        node_map = [[INF_val for val in xrange(len(node))] for val in xrange(len(node))]

        node_map_time = [[INF_val for val in xrange(len(node))] for val in xrange(len(node))]

        # path_map[i][j]=j 表示i到j的最短路径是经过顶点j
        path_map = [[0 for val in xrange(len(node))] for val in xrange(len(node))]

        set_node_map(node_map, node, node_list, path_map)

        set_node_map(node_map_time, node, node_list_time, path_map)

        floydpath = Floyd_Path(node, node_map, path_map)

        floydpath_time = Floyd_Path(node, node_map_time, path_map)
        # path = Floydpath(from_node, to_node)

        self.node = node
        self.data["distance_matrix"], self.data["time_distance_matrix"] = [], []
        self.data["distance_matrix"] = floydpath.node_map
        self.data["time_distance_matrix"] = floydpath_time.node_map

        # return floydpath.node_map, floydpath_time.node_map

    def generate_order_demands(self):
        self.data["demands"] = [0 for _ in range(len(self.node))]
        with open(self.order_path, 'r+', encoding='utf-8') as jsonfile:
            lines = jsonfile.read()
            orders = json.loads(lines)
        self.orders = orders
        for order in orders:
            from_index = self.node.index(order["pickup_factory_id"])
            # to_index = self.node.index(order["delivery_factory_id"])
            self.data["demands"][from_index] += order["demand"]

    def generate_vehicle_info(self):
        self.data["vehicle_capacities"], self.data["num_vehicles"] = [], []
        self.data["starts"], self.data["ends"] = [], []

        with open(self.vehicles_path, 'r+', encoding='utf-8') as jsonfile:
            lines = jsonfile.read()
            vehicles = json.loads(lines)
        for vehicle in vehicles:
            self.data["vehicle_capacities"].append(vehicle["capacity"])
            if vehicle["destination"] is not None and len(self.node) > 0:
                self.data["starts"].append(self.node.index(vehicle["cur_factory_id"]))
                self.data["ends"].append(self.node.index(vehicle["destination"]["factory_id"]))
        self.data["num_vehicles"] = len(vehicles)

    def generate_pickups_deliveries(self):
        self.data["pickups_deliveries"] = []
        if len(self.orders) > 0:
            for order in self.orders:
                pickup = order["pickup_factory_id"]
                pickup_index = self.node.index(pickup)
                delivery = order["delivery_factory_id"]
                delivery_index = self.node.index(delivery)
                self.data["pickups_deliveries"].append([pickup_index, delivery_index])

    def generate_time_windows(self):


        pass

    def create_data_model(self):
        self.generate_distance_matrix()
        self.generate_order_demands()
        self.generate_vehicle_info()
        self.generate_pickups_deliveries()
        return self.data


class Solver():
    def __init__(self, input):
        self.input = input

    @property
    def add_constraints(self):
        start_time = time.time()
        prepares = Prepare_Data(self.input[0], self.input[1], self.input[2])
        data = prepares.create_data_model()
        manager = pywrapcp.RoutingIndexManager(len(data["time_distance_matrix"]), data["num_vehicles"], data["starts"],
                                               data["ends"])
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['time_distance_matrix'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        dimension_name = 'Distance'
        routing.AddDimension(
            transit_callback_index,
            0,
            3000000,
            True,
            dimension_name)
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(100)

        # def time_callback(from_index, to_index):
        #     from_node = manager.IndexToNode(from_index)
        #     to_node = manager.IndexToNode(to_index)
        #     return data['time_distance_matrix'][from_node][to_node]
        #
        # transit_callback_index = routing.RegisterTransitCallback(time_callback)
        # routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        # # 回调时间距离代价
        # time = 'Time'
        # routing.AddDimension(transit_callback_index,
        #                      30,  # allow waiting time
        #                      30,  # maximum time per vehicle
        #                      False,  # Don't force start cumul to zero.
        #                      time)
        #
        # time_dimension = routing.GetDimensionOrDie(time)

        def demand_callback(from_index):
            from_node = manager.IndexToNode(from_index)
            return data["demands"][from_node]

        demand_callback_index = routing.RegisterUnaryTransitCallback(
            demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,
            data["vehicle_capacities"],
            True,
            'Capacity')

        for request in data["pickups_deliveries"]:
            pickup_index = manager.NodeToIndex(request[0])
            delivery_index = manager.NodeToIndex(request[1])
            routing.AddPickupAndDelivery(pickup_index, delivery_index)
            routing.solver().Add(
                routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index))
            routing.solver().Add(
                distance_dimension.CumulVar(pickup_index) <=
                distance_dimension.CumulVar(delivery_index))
            routing.AddPickupAndDelivery(pickup_index, delivery_index)
            routing.solver().Add(routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index))

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION)

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        # Print solution on console.
        if solution:
            self.print_solution(data, manager, routing, solution)
            time_cost = (time.time() - start_time)
            print("total cal time cost {}", time_cost)


    def add_time_window(self):

        # def time_callback(from_index, to_index):
        #     from_node = manager.IndexToNode(from_index)
        #     to_node = manager.IndexToNode(to_index)
        #     return data['time_matrix'][from_node][to_node]
        #
        # transit_callback_index = routing.RegisterTransitCallback(time_callback)
        # routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        # # 回调时间距离代价
        # time = 'Time'
        # routing.AddDimension(transit_callback_index,
        #                      30,  # allow waiting time
        #                      30,  # maximum time per vehicle
        #                      False,  # Don't force start cumul to zero.
        #                      time)
        #
        # time_dimension = routing.GetDimensionOrDie(time)
        # # Add time window constraints for each location except depot.
        # for location_idx, time_window in enumerate(data['time_windows']):
        #     if location_idx == data['depot']:
        #         continue
        #     index = manager.NodeToIndex(location_idx)
        #     time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
        # # Add time window constraints for each vehicle start node.
        # depot_idx = data['depot']
        # for vehicle_id in range(data['num_vehicles']):
        #     index = routing.Start(vehicle_id)
        #     time_dimension.CumulVar(index).SetRange(
        #         data['time_windows'][depot_idx][0],
        #         data['time_windows'][depot_idx][1])
        # for i in range(data['num_vehicles']):
        #     routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.Start(i)))
        #     routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.End(i)))

        pass

    def add_lilf(self, routing, total_nodes, solver, index):

        def lifo_fn(a, b):
            """
            Just increment by one
            """
            return 1

        picku_a_index, picku_b_index,  deliv_a_index, deliv_b_index = index[0], index[1], index[2], index[3]

        routing.AddDimension(
            lifo_fn,  # total time function callback
            0,  # allowed time slack
            int(total_nodes),
            True,
            'LIFO')
        lifo_dimension = routing.GetDimensionOrDie('LIFO')

        early_condition = lifo_dimension.CumulVar(picku_a_index) <= lifo_dimension.CumulVar(picku_b_index)
        lifo_constraint = lifo_dimension.CumulVar(deliv_a_index) <= lifo_dimension.CumulVar(deliv_b_index)
        expression = solver.ConditionalExpression(
            early_condition,
            lifo_constraint,
            1)

        solver.AddConstraint(
            expression >= 1
        )

    def print_solution(self, data, manager, routing, solution):
        print(f'Objective: {solution.ObjectiveValue()}')
        total_distance = 0
        for vehicle_id in range(data['num_vehicles']):
            index = routing.Start(vehicle_id)
            plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
            route_distance = 0
            while not routing.IsEnd(index):
                plan_output += ' {} -> '.format(manager.IndexToNode(index))
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id)
            plan_output += '{}\n'.format(manager.IndexToNode(index))
            plan_output += 'Distance of the route: {} seconds\n'.format(route_distance)
            print(plan_output)
            total_distance += route_distance
        print('Total Distance of all routes: {} seconds'.format(total_distance))

    def solver(self):
        pass


class PostHandler():
    def __init__(self, input):
        self.input = input

    def write_result(self):
        pass


def main():
    order_path = "./data_interaction/unallocated_order_items.json"
    map_path = "../benchmark/route_map.csv"
    vehicle_path = "./data_interaction/vehicle_info.json"
    inputs = [map_path, order_path, vehicle_path]
    solver = Solver(inputs)
    solver.add_constraints

    # pass


if __name__ == '__main__':
    main()

