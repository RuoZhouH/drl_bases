#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Solution(object):
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """

        lb = lambda i, j: i == j

        if strs is None or len(strs) == 0:
            return ""

        res = []

        firsts = strs[0]
        i = 0
        for j in firsts:
            ls = [lb(j, k[i] if len(k) > i else "") for k in strs[1:]]
            i += 1
            if all(ls):
                res.append(j)
            else:
                break

        return "".join(res)





