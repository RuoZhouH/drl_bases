#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

import math

import matplotlib.pyplot as plt

Y1 = [3.8, 4.4, 5.4, 6.6, 4.2, 5.9, 4.6, 6.2, 3, 6.8, 4.7, 4.7, 5.1, 3.2, 3.9, 2.8, 5.2, 3.9, 3.6, 3.9, 4.7, 6.4, 6, 3.8, 6.6, 8.3, 3, 4.1, 4.3, 3.1]
X = np.arange(0, len(Y1))

# Y2 = np.sin(2 * X + 1)
Y2 = [5.9, 5.4, 7.2, 4.3, 6.6, 5.8, 3.3, 6.5, 2.9, 3.7, 6.6, 7.7, 5, 6.7, 3.9, 6.2, 7.4, 9.8, 6.6, 6.3, 4, 8.3, 6.3, 3.4, 5.9, 9.2, 6.4, 6.1, 4, 9.1]
# 绘图ß
plt.figure(figsize=(9.6, 7.2))
plt.subplot(1, 1, 1)  # 绘制子图1
plt.plot(X, Y1, c='blue', linestyle=':', marker="o", markersize=5, markeredgewidth=1, markeredgecolor="grey")  # 绘制曲线图
plt.plot(X, Y2, c='red', linestyle='--', marker="D", markersize=5, markeredgewidth=1, markeredgecolor="grey")
# plt.plot(X, Y3, c='green', linestyle=':')

# plt.subplot(1, 3, 2)                  # 绘制子图2
# plt.plot(X, Y2, c='red', linestyle='--')
#
# plt.subplot(1, 3, 3)                  # 绘制子图3
# plt.plot(X, Y3, c='green', linestyle=':')

plt.draw()
plt.grid()
epoch = 4
plt.savefig('./img/pic-{}.png'.format(epoch + 1))
