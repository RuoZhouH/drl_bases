#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
最优策略及其性质
'''

from IPython.display import display
import sympy
from sympy import symbols
sympy.init_printing()


alpha, beta, gama = symbols('alpha beta gama')
v_hungry, v_full = symbols('v_hungry v_full')
q_hungry_eat,  q_hungry_none, q_full_eat, q_full_none = symbols('q_hungry_eat q_hungry_none q_full_eat q_full_none')
xyu_tuples = ((1, 1), (1, 0), (0, 1), (0, 0))
for x, y in xyu_tuples:
    system = sympy.Matrix(((1, 0, x-1, -x, 0, 0, 0), (0, 1, 0, 0, -y, y-1, 0),
                       (-gama, 0, 1, 0, 0, 0, 2), ((alpha-1)*gama, -alpha*gama, 0, 1, 0, 0, 2*alpha-3),
                       (-beta*gama, (beta-1)*gama, 0, 0, 1, 0, -5*beta+3),
                       (-2*gama, 0, 0, 0, 0, 1, 2)))
    result = sympy.solve_linear_system(system, v_hungry, v_full, q_hungry_eat, q_hungry_none, q_full_eat, q_full_none)
    print('\n')
    print('[+]*****==== x = {}, y = {} ===*****'.format(x, y))
    display(result)
    print('q_hungry_eat - q_hungry_none = ')
    display(sympy.simplify(result[q_hungry_eat]- result[q_hungry_none]))
    print('q_full_eat - q_full_none = ')
    display(sympy.simplify(result[q_full_eat] - result[q_full_none]))