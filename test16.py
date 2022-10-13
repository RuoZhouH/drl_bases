import matplotlib.pyplot as plt
import random
import queue

"""
任务完成时间
"""


def draw1():
    x_data = [0, 30, 60, 90]
    y2_data = [196.9395709, 181.7946636, 155.4991125, 155.9568921]
    y_data = [138.3654317, 164.5681337, 206.7983441, 135.4357305]

    x_width = range(0, len(x_data))
    x2_width = [i + 0.3 for i in x_width]

    plt.barh(x2_width, y2_data, lw=0.5, fc="y", height=0.3, label="origin")

    plt.barh(x_width, y_data, lw=0.5, fc="g", height=0.3, label="congestion")

    plt.yticks(range(0, 4), x_data)

    # for i in range(len(x_data)):
    #     plt.barh(x_data[i], y_data[i], color=(0.2 * i, 0.2 * i, 0.2 * i), linestyle="--", hatch="0")

    plt.legend()

    plt.title(u"job time cost")
    plt.ylabel(u"time snap")
    plt.xlabel(u"time cost")

    savepath = "./testbar1.png"

    plt.savefig(savepath)

    plt.close()


def draw2():
    x_data = [0, 30, 60, 90]
    y_data = [103.933135, 98.6604698, 99.93923224, 86.60252729]
    y2_data = [84.63132517, 75.93472785, 80.09099527, 78.49945775]

    x_width = range(0, len(x_data))
    x2_width = [i + 0.3 for i in x_width]

    plt.barh(x2_width, y2_data, lw=0.5, fc="r", height=0.3, label="congestion")

    plt.barh(x_width, y_data, lw=0.5, fc="b", height=0.3, label="origin")

    plt.yticks(range(0, 5), x_data)

    # for i in range(len(x_data)):
    #     plt.barh(x_data[i], y_data[i], color=(0.2 * i, 0.2 * i, 0.2 * i), linestyle="--", hatch="0")

    plt.legend()

    plt.title(u"job time cost")
    plt.ylabel(u"time snap")
    plt.xlabel(u"time cost")

    savepath = "./testbar2.png"

    plt.savefig(savepath)

    plt.close()


if __name__ == "__main__":

    draw1()
    # draw2()
