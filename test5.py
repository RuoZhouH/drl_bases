#!/usr/bin/env python
# -*- coding: utf-8 -*-


ls = []

ls.append(1)
ls.append(2)
ls.append(3)
ls.append(4)


for i in range(len(ls)):
    k = ls.pop(0)
    print(k)