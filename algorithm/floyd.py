
# -*- coding: utf-8 -*-
from xlwings import xrange
import csv
import numpy as np
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
        # node_map[node.index(x)][node.index(y)] = node_map[node.index(y)][node.index(x)] = val
        node_map[node.index(x)][node.index(y)] = val
        path_map[node.index(x)][node.index(y)] = node.index(y)
        path_map[node.index(y)][node.index(x)] = node.index(x)


if __name__ == "__main__":

    with open('../benchmark/route_map.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader]
    data = np.array(rows)  # rows是数据类型是‘list',转化为数组类型好处理
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
    # print(factory_id_map)
    inf = 9999999999

    # 排序factory_id，并建立(u, v, cost)
    factory_distance = []
    factory_time = []
    factory_id = []
    for l in data[1:]:
        # u, v, time
        factory_id.append([factory_id_map_opposite[l[1]], factory_id_map_opposite[l[2]], l[4]])
        factory_distance.append((l[1], l[2], float(l[3])))
        factory_time.append((l[1], l[2], int(l[4])))
    factory_id = sorted(factory_id, key=lambda x: (x[0], x[1]))
    # print(len(factory_id)) 23562 = 154 * 154 - 154，说明是完全图

    # 构图
    graph = [[(lambda x: 0 if x[0] == x[1] else inf)([i, j]) for j in range(n)] for i in range(n)]
    parents = [[i] * n for i in range(n)]  # 关键地方，i-->j 的父结点初始化都为i

    for u, v, c in factory_id:
        graph[u][v] = int(c)  # 因为是有向图，边权只赋给graph[u][v]


    # node = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    # node_list = [('A', 'F', 9), ('A', 'B', 10), ('A', 'G', 15), ('B', 'F', 2),
    #              ('G', 'F', 3), ('G', 'E', 12), ('G', 'C', 10), ('C', 'E', 1),
    #              ('E', 'D', 7)]

    node = factory_id_unique

    node_list = factory_distance
    # node_list = factory_time

    # node_map[i][j] 存储i到j的最短距离
    node_map = [[INF_val for val in xrange(len(node))] for val in xrange(len(node))]
    # path_map[i][j]=j 表示i到j的最短路径是经过顶点j
    path_map = [[0 for val in xrange(len(node))] for val in xrange(len(node))]

    # set node_map
    set_node_map(node_map, node, node_list, path_map)

    # select one node to obj node, e.g. A --> D(node[0] --> node[3])
    start_point = node[8]
    end_point = node[9]
    from_node = node.index(start_point)
    to_node = node.index(end_point)
    Floydpath = Floyd_Path(node, node_map, path_map)
    path = Floydpath(from_node, to_node)
    index_path = []
    for pt in path:
        index_path.append(factory_id_map_opposite[pt])
    print(path)
    print(index_path)
