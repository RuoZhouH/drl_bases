#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

# Import Data
origin_data = pd.read_excel("./raw_algo_with_20agvs.xls", sheet_name=[0, 1])
whca_data = pd.read_excel("./whca_algo_with_20agvs.xls", sheet_name=[0, 1])

print(origin_data)

##### 柱状图 ###### 统计对比图
fig, ax = plt.subplots(nrows=4, ncols=1, figsize=(16, 12), dpi=80)
plt.subplots_adjust(left=None, bottom=1, right=None, top=2,
                wspace=None, hspace=None)
axList = list(ax.ravel())
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 输出图像的标题可以为中文正常输出
plt.rcParams["axes.unicode_minus"] = False  # 可以正常输出图线里的负号

columns = list(origin_data[0].columns)
name_list = list(origin_data[0][columns[0]])

ax_index = 0
for ind in [2, 3, 4, 7]:
    raw_columns = list(origin_data[0][columns[ind]])
    whca_columns = list(whca_data[0][columns[ind]])
    x = list(range(len(raw_columns)))
    total_width, n = 0.6, 2
    width = total_width / n
    axList[ax_index].bar(x, raw_columns, width=width, label="raw_algorithm", fc="g")
    for a, b in zip(x, raw_columns):  # 柱子上的数字显示
        axList[ax_index].text(a, b, '%.2f' % b, ha='center', va='bottom', fontsize=10);
    for i in range(len(x)):
        x[i] = x[i] + width
    axList[ax_index].bar(x, whca_columns, width=width, label="whca_algorithm", tick_label=name_list, fc="orange")
    axList[ax_index].set_xlabel("数据统计", fontsize=12)
    axList[ax_index].set_ylabel(columns[ind], fontsize=12)
    # ax1.set_title("不同算法指标表现", fontsize=15)
    for a, b in zip(x, whca_columns):  # 柱子上的数字显示
        axList[ax_index].text(a, b, '%.2f' % b, ha='center', va='bottom', fontsize=10);
    axList[ax_index].legend(fontsize=14)
    plt.tight_layout()
    ax_index +=1


# plt.title("不同算法指标表现", fontsize=15)
plt.savefig(r'./colormap_total.png')
plt.show()


##### 折线 ###### 趋势对比图
fig, ax = plt.subplots(nrows=4, ncols=1, figsize=(16, 12), dpi=80)
plt.subplots_adjust(left=None, bottom=1, right=None, top=2,
                wspace=None, hspace=None)
axList = list(ax.ravel())
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 输出图像的标题可以为中文正常输出
plt.rcParams["axes.unicode_minus"] = False  # 可以正常输出图线里的负号
columns = list(origin_data[1].columns)
name_list = list(origin_data[1][columns[2]])

ax_index = 0
for ind in [3, 4, 5, 8]:
    raw_columns = list(origin_data[1][columns[ind]])
    whca_columns = list(whca_data[1][columns[ind]])
    x = list(range(len(raw_columns)))
    axList[ax_index].plot(x, raw_columns, marker='o', mec='r', mfc='w',label=u'raw_algorithm', color='green')
    axList[ax_index].plot(x, whca_columns, marker='*', ms=10, label=u'whca_algorithm', color='orange')
    axList[ax_index].set_xticks(x)
    axList[ax_index].grid(True, which='major')
    axList[ax_index].legend(fontsize=14)  # 让图例生效
    axList[ax_index].set_xlabel("测试样本编号", fontsize=12)
    axList[ax_index].set_ylabel(columns[ind], fontsize=12)
    plt.tight_layout()
    # ax1.set_title("不同算法指标表现", fontsize=15)
    ax_index +=1

# plt.title("不同算法指标表现", fontsize=15)
plt.savefig(r'./colormap_sample.png')
plt.show()