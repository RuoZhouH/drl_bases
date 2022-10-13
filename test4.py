#!/usr/bin/env python
# -*- coding: utf-8 -*-


grid = [[1, 3, 1], [1, 5, 1], [4, 2, 8], [1,1,1]]

def search(grid):
    xl = len(grid)
    yl = len(grid[0])

    if xl <=1 or yl <=1:
        return

    cost = [[0 for i in range(yl)] for j in range(xl)]

    path = [0]*(xl+yl)

    cost[0][0] = grid[0][0]

    path[0] = (0,0)

    for i in range(1, xl):
        cost[i][0] = cost[i-1][0] + grid[i][0]

    for j in range(1, yl):
        cost[0][j] = cost[0][j-1] + grid[0][j]

    for i in range(1, xl):
        for j in range(1, yl):
            cost[i][j] = min(cost[i-1][j], cost[i][j-1]) + grid[i][j]
            path[i] = (i-1, j) if cost[i-1][j]<cost[i][j-1] else (i, j-1)

    return cost[xl-1][yl-1], path


cost, path = search(grid)
print(cost)
print(path)