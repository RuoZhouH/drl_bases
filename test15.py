#!usr/bin/env python
# encoding:utf-8
from __future__ import division

'''
平均速度对比
'''

import matplotlib
import matplotlib.pyplot as plt
import random


def plot_sctter1(n=12, savepath='test.png'):
    '''
    绘制样本数据的散点图（对比）
    '''
    # x_list = ["ROAD_WAY010", "ROAD_WAY004sub", "ROAD_WAY008sub", "ROAD_WAY001sub", "ROAD_WAY008", "ROAD_WAY009",
    #           "ROAD_WAY006", "ROAD_WAY007", "ROAD_WAY004", "ROAD_WAY005", "ROAD_WAY002", "ROAD_WAY003", "ROAD_WAY011"]


    y_list1, y_list2 = [], []
    # for i in range(n):
    #     y_list1.append(random.randint(2000, 5000))
    # for i in range(n):
    #     y_list2.append(random.randint(10, 1000))
    # y_list2 = [0.379863636, 1.20575, 0.866318182, 0.767, 0.69368, 0.373428571, 0.494772727, 0.406125, 0.32308, 0.358571429, 0.6233, 0.292333333, 0.589333333]
    y_list2 = [0.088, 0.7195,0.307666667, 0,	0, 0.5234, 1.137, 0.7976, 0.27,	0.896666667, 0.689,	1.111, 0.983555556,	0.762, 1.4185,	0,	0.275,	0.971333333, 0.501666667, 0.888, 0.79125, 0.946, 0.629333333, 0.669166667,
               0.475, 0.505333333, 1.2965,	0,	0.509333333,	0.535,	0.338,	0.53725,	0,	1.074,	0.9763,	0.888,	0.945,	0.839714286,	0.592,	0.818,	0.718555556,	0.354857143,	0,	0.5595,	0.557764706,
               0.613,	0.57375,	0.685428571,	0.747823529,	0.529333333,	0.69375,	0.678,	0.485181818,	1.303142857,	0,	0.8635,	0.581571429,	0.694,	0.8148125,	0.445,	0.848230769,	0.4325,	0.585866667,
               0.784,	1.047666667,	0.5292,	0.5324,	0.5137,	0.746428571,	0.745866667,	0.779,	0.987352941,	0.813222222,	1.250076923,	0.223,	0,	0.59525,	0.381285714,	1.262666667,	0.636142857,	1.473666667,
               0.544153846,	0.8295,	0.724125,	0.3074,		0.585888889,	1.0455,	0.648,	0.488625,	0, 0.685615385,	1.114333333,	0.965,		0, 0.493,		0,0.8155,	0.713,0	,0.8164,	0.456533333,	0.6825]
    # y_list1 = [0.331241379, 1.088625, 0.494136364, 0, 0.533681818, 0.389526316, 0.400392857, 0.295545455, 0.3877, 0.350588235, 0.36505, 0.234777778, 0.366666667]
    y_list1 = [0.578,	0,	0.384,	0.57,	0,	0.09,	0,	0.8864,	0.337,	0.221,	0,	0,	0.2215,	0.90,	0.17,	1.981,	0.4,	0.236,	0.6505,	0.886,	0,	0.2224,	0,	0.533,	0,	0.844,	0,	0,	0,	0.243,	0,	0.86,	0,	1.083666667,	0,	0.587,	0.859,	0.570375,
               1.204,	1.1453,	0.8226,	0,	0.425,	0.276571429,	0.441846154,	0.432,	0.391,	1.072125,	0.355363636,	0.468916667,	0.413666667,	0.901615385,	0.662,	0,	0.339,	0,	1.05,	0.422882353,	0.474,	0.435,	0,	0.335388889,	0,	0.287833333,
               0.222666667,	0.5345,	0.692,	0,	0.3388,	0.4285,	0.742,	0.916,	0.566444444,	0.359333333,	0,	0.640333333,	0.630333333,	0,	0.6738,	0.4885,	0.3778,	0.734333333,	1.001666667,	0.619818182,	0.193,	0.416,	0,	0.625428571,	0.712,	1.292,
               0.6002,	0.307,	0.9065,	0,	0.6942,	0,	1.175,	0,	0,	0.84,	0.484294118,	0.3625]

    x_list  = list(range(len(y_list2)))
    plt.clf()
    plt.scatter(x_list, y_list1, color='r', label='origin', marker="o")
    plt.scatter(x_list, y_list2, color='b', label='congestion', marker="D")
    plt.grid()
    plt.xticks(rotation='vertical', fontsize=3)
    plt.legend(loc='upper left', ncol=1, fancybox=True, shadow=True)
    plt.savefig(savepath)



def plot_sctter2(n=12, savepath='test.png'):
    '''
    绘制样本数据的散点图（对比）
    '''
    x_list = ["461", "925", "838", "307", "019", "920", "612", "101"]
    y_list1, y_list2 = [], []
    # for i in range(n):
    #     y_list1.append(random.randint(2000, 5000))
    # for i in range(n):
    #     y_list2.append(random.randint(10, 1000))
    y_list1 = [0.549305556, 0.727111111, 0.626129032, 0.44675, 0.783060606, 0.450827586, 0.714068966, 0.311945946]
    y_list2 = [0.701653846, 0.8005, 0.878647059, 0.41816, 0.613642857, 0.688095238, 0.886478261, 0.762925926]
    plt.clf()
    plt.scatter(x_list, y_list1, color='r', label='origin', marker="o")
    plt.scatter(x_list, y_list2, color='b', label='congestion', marker="D")
    plt.grid()
    plt.legend(loc='upper left', ncol=1, fancybox=True, shadow=True)
    plt.savefig(savepath)


if __name__ == '__main__':
    plot_sctter1(n=12, savepath='test2.png')