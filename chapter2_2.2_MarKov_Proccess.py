#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
一个简单的马尔科夫决策过程求解
'''

import  sympy
from sympy import symbols

sympy.init_printing()

v_hungry, v_full = symbols('v_hurgry v_full')

q_hungry_eat, q_hungry_none, q_full_eat, q_full_none = symbols('q_hungry_eat q_hungry_none q_full_eat q_full_none')

alpha, beta, x, y, gama = symbols('alpha beta x y gama')

system = sympy.Matrix(((1, 0, x-1, -x, 0, 0, 0), (0, 1, 0, 0, -y, y-1, 0),
                       (-gama, 0, 1, 0, 0, 0, 2), ((alpha-1)*gama, -alpha*gama, 0, 1, 0, 0, -4*alpha+3),
                       (-beta*gama, (beta-1)*gama, 0, 0, 1, 0, 4*beta-2),
                       (0, -gama, 0, 0, 0, 1, -1)))

# 求解的结果为字典格式
result = sympy.solve_linear_system(system, v_hungry, v_full, q_hungry_eat, q_hungry_none, q_full_eat, q_full_none)

for k, v in result.items():
    print(k)
    print(v)