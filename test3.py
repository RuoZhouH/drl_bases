#!/usr/bin/env python
# -*- coding: utf-8 -*-


class binarytree():
    def __init__(self, x):
        self.x = x
        self.left = None
        self.right = None

def toTree(nums):

    def level(index):
        if index >= len(nums) or nums[index] == None:
            return None

        nodeTree = binarytree(nums[index])
        nodeTree.left = level(2 * index + 1)
        nodeTree.right = level(2 * index + 2)

        return nodeTree

    return level(0)


nums = [0, 1, 2, 3, 4, 5, 6]
nn = [3, 9, 20, None, None, 15, 7, None, None, None, None, 1, 2]
res = toTree(nn)
print(res)
