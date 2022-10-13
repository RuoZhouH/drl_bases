#!/usr/bin/env python
# -*- coding: utf-8 -*-


def dijkstra(graph, startIndex, path, cost, max):
    lenth = len(graph)
    v = [0] * lenth
    for i in range(lenth):
        if i == startIndex:
            v[startIndex] = 1
        else:
            cost[i] = graph[startIndex][i]
            path[i] = (startIndex if (cost[i] < max) else -1)

    for i in range(1, lenth):
        minCost = max
        curNode = -1
        for w in range(lenth):
            if v[w] == 0 and cost[w] < minCost:
                minCost = cost[w]
                curNode = w
        if curNode == -1: break
        v[curNode] = 1

        for w in range(lenth):
            if v[w] == 0 and (cost[curNode] + graph[curNode][w] < cost[w]):
                cost[w] = cost[curNode] + graph[curNode][w]
                path[w] = curNode

    return path


if __name__ == '__main__':
    inf = 10086
    mgraph = [[0, 1, 12, inf, inf, inf],
              [inf, 0, 9, 3, inf, inf],
              [inf, inf, 0, inf, 5, inf],
              [inf, inf, 4, 0, 13, 15],
              [inf, inf, inf, inf, 0, 4],
              [inf, inf, inf, inf, inf, 0]]

    path = [0]*6
    cost = [0]*6
    res = dijkstra(mgraph, 1, path, cost, inf)
    print(res)


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def pseudoPalindromicPaths(self, root: TreeNode) -> int:

        queue = [(root, set([]))] if root is not None else []
        total = 0

        while queue != []:

            # pop node
            node, seen = queue[0]
            queue = queue[1:]

            # check if leaf and palindrome path
            if node.left is None and node.right is None:
                if node.val in seen:
                    seen.remove(node.val)
                else:
                    seen.add(node.val)
                if len(seen) <= 1:
                    total += 1

            else:
                new_seen_left = seen.copy()
                new_seen_right = seen.copy()

                if node.val in seen:
                    new_seen_left.remove(node.val)
                    new_seen_right.remove(node.val)
                else:
                    new_seen_left.add(node.val)
                    new_seen_right.add(node.val)

                if node.left is not None:
                    queue.append((node.left, new_seen_left))
                if node.right is not None:
                    queue.append((node.right, new_seen_right))

        return total