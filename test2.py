#!/usr/bin/env python
# -*- coding: utf-8 -*-


def Dijkstra(network, s, d):
    print("Start Dijstra Path……")
    path = []
    n = len(network)
    fmax = 999
    w = [[0 for i in range(n)] for j in range(n)]
    book = [0 for i in range(n)]
    dis = [fmax for i in range(n)]
    book[s - 1] = 1
    midpath = [-1 for i in range(n)]
    for i in range(n):
        for j in range(n):
            if network[i][j] != 0:
                w[i][j] = network[i][j]
            else:
                w[i][j] = fmax
            if i == s - 1 and network[i][j] != 0:
                dis[j] = network[i][j]
    for i in range(n - 1):
        min = fmax
        u = -1
        for j in range(n):
            if book[j] == 0 and dis[j] < min:
                min = dis[j]
                u = j
        if u == -1: break
        book[u] = 1
        for v in range(n):
            if dis[v] > dis[u] + w[u][v]:
                dis[v] = dis[u] + w[u][v]
                midpath[v] = u + 1
    j = d - 1
    path.append(d)
    while (midpath[j] != -1):
        path.append(midpath[j])
        j = midpath[j] - 1
    path.append(s)
    path.reverse()
    print(path)
    # print(midpath)
    print(dis)
    # return path


inf = 10086

network = [[0, 1, 0, 2, 0, 0],
           [1, 0, 2, 4, 3, 0],
           [0, 2, 0, 0, 1, 4],
           [2, 4, 0, 0, 6, 0],
           [0, 3, 1, 6, 0, 2],
           [0, 0, 4, 0, 2, 0]]

mgraph = [[0, 1, 12, inf, inf, inf],
          [inf, 0, 9, 3, inf, inf],
          [inf, inf, 0, inf, 5, inf],
          [inf, inf, 4, 0, 13, 15],
          [inf, inf, inf, inf, 0, 4],
          [inf, inf, inf, inf, inf, 0]]
Dijkstra(network, 2, 6)
Dijkstra(mgraph, 1, 4)
