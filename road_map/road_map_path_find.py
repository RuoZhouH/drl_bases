# -*- coding: utf-8 -*-

from xlwings import xrange
import csv
import numpy as np
import json
from itertools import product

INF_val = 9999


class Floyd_Path():
    def __init__(self, node, node_map, path_map):
        self.node = node
        self.node_map = node_map
        self.node_length = len(node_map)
        self.path_map = path_map
        self._init_Floyd()

    def __call__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node
        return self._format_path()

    def _init_Floyd(self):
        for k in range(self.node_length):
            for i in range(self.node_length):
                for j in range(self.node_length):
                    tmp = self.node_map[i][k] + self.node_map[k][j]
                    if self.node_map[i][j] > tmp:
                        self.node_map[i][j] = tmp
                        self.path_map[i][j] = self.path_map[i][k]

        print('_init_Floyd is end')

    def _format_path(self):
        node_list = []
        temp_node = self.from_node
        obj_node = self.to_node
        print("the shortest path is: ")
        print(self.node_map[temp_node][obj_node])
        node_list.append(self.node[temp_node])
        while True:
            node_list.append(self.node[self.path_map[temp_node][obj_node]])
            temp_node = self.path_map[temp_node][obj_node]
            if temp_node == obj_node:
                break

        return node_list


def set_node_map(node_map, node, node_list, path_map):
    for i in range(len(node)):
        # 对角线为0
        node_map[i][i] = 0
    for x, y, val in node_list:
        node_map[node.index(x)][node.index(y)] = node_map[node.index(y)][node.index(x)] = val
        node_map[node.index(x)][node.index(y)] = val
        path_map[node.index(x)][node.index(y)] = node.index(y)
        path_map[node.index(y)][node.index(x)] = node.index(x)


def read_json_from_file(file_name):
    with open(file_name, 'r') as fd:
        data = fd.read()
    return json.loads(data)


def write_json_to_file(file_name, data):
    with open(file_name, 'w') as fd:
        fd.write(json.dumps(data))


if __name__ == "__main__":

    file_name = './config.json'
    rows = read_json_from_file(file_name)
    x_range = rows['xrange']
    y_range = rows['yrange']
    start_point = rows['start_point']
    goal_point = rows['goal_point']
    edge_cost = rows['edge_cost']
    x_point = [i for i in range(x_range[0], x_range[1])]
    y_point = [j for j in range(y_range[0], y_range[1])]
    str_node_map = {}
    node_list = set()
    map_cost = []
    for x, y in product(x_point, y_point):
        node = str(x) + '_' + str(y)
        str_node_map[node] = [x, y]
        node_list.add(node)

    for x, y in product(x_point, y_point):
        node = str(x) + '_' + str(y)
        right_node = str(x + 1) + '_' + str(y)
        up_node = str(x) + '_' + str(y + 1)
        left_node = str(x-1) + '_' + str(y)
        down_node = str(x) + '_' + str(y-1)
        if x == x_range[0] and y == y_range[0]:
            map_cost.append((node, up_node, edge_cost))
            map_cost.append((node, right_node, edge_cost))
        elif x == x_range[0] and y_range[0] < y < y_range[1] - 1:
            map_cost.append((node, up_node, edge_cost))
            map_cost.append((node, right_node, edge_cost))
            map_cost.append((node, down_node, edge_cost))
        elif x_range[0] < x < x_range[1] - 1 and y == y_range[0]:
            map_cost.append((node, up_node, edge_cost))
            map_cost.append((node, right_node, edge_cost))
            map_cost.append((node, left_node, edge_cost))
        elif x_range[0] < x < x_range[1] - 1 and y_range[0] < y < y_range[1] - 1:
            map_cost.append((node, up_node, edge_cost))
            map_cost.append((node, right_node, edge_cost))
            map_cost.append((node, left_node, edge_cost))
            map_cost.append((node, down_node, edge_cost))
        elif x == x_range[1] - 1 and y == y_range[1] - 1:
            map_cost.append((node, left_node, edge_cost))
            map_cost.append((node, down_node, edge_cost))
        elif x == x_range[1] - 1 and y_range[0] < y < y_range[1] - 1:
            map_cost.append((node, up_node, edge_cost))
            map_cost.append((node, left_node, edge_cost))
            map_cost.append((node, down_node, edge_cost))
        elif x_range[0] < x < x_range[1] - 1 and y == y_range[1] - 1:
            map_cost.append((node, right_node, edge_cost))
            map_cost.append((node, left_node, edge_cost))
            map_cost.append((node, down_node, edge_cost))

    n = len(node_list)  # 节点个数

    all_node = list(node_list)

    node_cost = map_cost
    # node_list = factory_time
    # node_map[i][j] 存储i到j的最短距离
    node_map = [[INF_val for val in xrange(len(all_node))] for val in xrange(len(all_node))]
    # path_map[i][j]=j 表示i到j的最短路径是经过顶点j
    path_map = [[0 for val in xrange(len(all_node))] for val in xrange(len(all_node))]

    # set node_map
    set_node_map(node_map, all_node, node_cost, path_map)

    # select one node to obj node, e.g. A --> D(node[0] --> node[3])
    start_point = str(start_point[0]) + '_' + str(start_point[1])
    end_point = str(goal_point[0]) + '_' + str(goal_point[1])
    from_node = all_node.index(start_point)
    to_node = all_node.index(end_point)
    Floydpath = Floyd_Path(all_node, node_map, path_map)
    path = Floydpath(from_node, to_node)
    index_path = []
    for pt in path:
        index_path.append(str_node_map[pt])

    res_data = {}
    for i, j in enumerate(path):
        res_data[j] = index_path[i]
    print(path)
    print(index_path)
    write_json_to_file("./output_path.json", res_data)
