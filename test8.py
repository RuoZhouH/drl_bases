#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 输入：
# [2,1,5,3,6,4,8,9,7]
# 复制
# 返回值：
# [1,3,4,8,9]

def longestSubList(ls):
    subList = []
    maxLenth = 0
    for i in range(len(ls)):
        tempLs = ls[i:]
        subLs1 = findSub(tempLs)
        subLs2 = findMinSub(tempLs)

        if len(subLs1) > len(subLs2):
            finalSubLs = subLs1
        else:
            finalSubLs = subLs2

        if len(finalSubLs) >= maxLenth:
            maxLenth = len(finalSubLs)
            subList = finalSubLs

    return subList


def findSub(ls):
    subLs = [ls[0]]
    startPoint = ls[0]
    for i in ls:
        if i > startPoint:
            subLs.append(i)
            startPoint = i

    return subLs


def findMinSub(ls):
    subLs = [ls[0]]
    startPoint = ls[0]
    for i in range(len(ls)):
        subTempLs = ls[i:]
        minPoint = min(subTempLs)
        if minPoint > startPoint:
            subLs.append(minPoint)
            startPoint = minPoint
    return subLs


if __name__ == "__main__":
    ls = [2, 1, 5, 3, 6, 4, 8, 9, 7]

    print(ls)
    print(longestSubList(ls))
