# -*- coding: utf-8 -*-

import io, sys, json
import math

import matplotlib.pyplot as plt
import pylab as p
import requests
import time
import pymysql
from appdirs import unicode
import queue


def remove_prefix_u(d):
    """为了避免输出的字符串带有unicode前缀(如: u'ha'),
       对加载的json数据进行转换, 以去掉u前缀.
    """
    if isinstance(d, dict):
        return dict([(remove_prefix_u(k), remove_prefix_u(v)) for (k, v) in d.items()])
    elif isinstance(d, list):
        return [remove_prefix_u(i) for i in d]
    elif isinstance(d, unicode):
        return d.encode('utf-8')
    else:
        return d


def load_map_json_file(map_file):
    """加载指定路径的地图文件, 返回加载后的json数据"""
    with io.open(map_file, encoding='utf-8') as json_file:
        try:
            map_json = json.load(json_file)
            if sys.version_info[0] < 3:
                # python3全以unicode编码, 所以没有u前缀, 不用转换
                map_json = remove_prefix_u(map_json)
        except Exception as exc:
            if type(exc) is UnicodeDecodeError:
                print(" 输入的地图文件编码无法识别, 如果文件含有中文, 请确保文件以utf-8编码保存!")
            else:
                # 其他异常，常见错误为JSON数据缺对象值，如 'name':,
                print(exc)
            sys.exit(1)

    return map_json


def get_points(map_file):
    map_json = load_map_json_file(map_file)
    for zl in map_json['zoneList']:
        for p in zl['pointList']:
            pc = p.get('pointCode', None)
            pt = p.get('pointType', None)
            if (pt == "STORAGE"):
                g_point_codes.append(pc)


g_point_codes = []
g_point_coords = []
g_point_coord = {}


def preprocess_point_data(map_json):
    """预处理点数据, 以加速之后使用"""
    map_json = load_map_json_file(map_json)
    global g_point_codes
    global g_point_coords
    global g_point_coord
    for zl in map_json['zoneList']:
        for point in zl['pointList']:
            pc = point['pointCode']
            x, y = point['x'], point['y']
            g_point_codes.append((pc, x, y))
            g_point_coords.append((x, y))
            g_point_coord[pc] = (x, y)


# 生成聚类函数

def cluster_process(g_point_coord, data):
    cluster_distance = 2400
    min_cluster_point = 3
    # 1. 生成距离矩阵
    if data is None:
        return None, None

    distance_map = {}
    for key1 in data.keys():
        for key2 in data.keys():
            distance_map[key1 + key2] = distance_cal(g_point_coord.get(key1), g_point_coord.get(key2))

    # 2. 生成聚类族
    cluster_point_map = {}
    point_cluster_map = {}
    open_list = queue.Queue()
    close_list = set()
    cluster_key = "cluster"
    cluster_num = 0

    time_start = time.time()
    for point in data.keys():

        if point in close_list:
            continue

        close_list.add(point)
        cluster_set = set()
        for pt in data.keys():
            if pt == point:
                continue
            if distance_map.get(point + pt) < cluster_distance:
                open_list.put(pt)
                cluster_set.add(pt)

        if open_list.empty():
            continue

        cluster_set.add(point)
        while not open_list.empty():
            search_point = open_list.get()
            close_list.add(search_point)
            for cluster_pt in data.keys():
                if search_point == cluster_pt:
                    continue
                if cluster_pt in close_list:
                    continue
                if distance_map.get(search_point + cluster_pt) < cluster_distance:
                    open_list.put(cluster_pt)
                    cluster_set.add(cluster_pt)

        if len(cluster_set) > min_cluster_point:
            cluster_point_map[cluster_key + str(cluster_num)] = cluster_set
            # 反映射
            for each_point in cluster_set:
                point_cluster_map[each_point] = cluster_key + str(cluster_num)

        cluster_num += 1

    time_end = time.time()
    print("cluster calculate time cost :")
    print(time_end - time_start)
    print("-----------------------------")
    return cluster_point_map, point_cluster_map


def distance_cal(p1, p2):
    if p1 is None or p2 is None:
        return math.inf
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


if __name__ == '__main__':

    # 1.获取地图的点位数据
    preprocess_point_data("./map/DEBR.json")
    # print(g_point_codes)
    # print(g_point_coords)
    plt.ion()

    # 静态数据查询
    # 3.获取小车货架实时点位（查数据库）
    connect_mysql = pymysql.connect(host="172.31.236.2", port=3306, user="root", password="root123",
                                    database="evo_basic", charset="utf8")
    cursor = connect_mysql.cursor()
    sql = "SELECT roadway_point_code FROM  basic_slot where bucket_layer = \'1\'"
    cursor.execute(sql)
    bucket_point = cursor.fetchall()
    sql1 = "SELECT point_code FROM  basic_station_point where state=\'effective\'"
    cursor.execute(sql1)
    station_point = cursor.fetchall()
    connect_mysql.close()

    # 工作站和货架
    bucket_point_coords = []
    station_point_coords = []
    for i in bucket_point:
        if i[0] is not None and i[0] in g_point_coord.keys():
            bucket_point_coords.append(g_point_coord[i[0]])
    for j in station_point:
        if j[0] is not None and j[0] in g_point_coord.keys():
            station_point_coords.append(g_point_coord[j[0]])
    x_c5, y_c5 = zip(*bucket_point_coords)
    x_c7, y_c7 = zip(*station_point_coords)

    while 1:
        # 2.获取拥堵等级点位数据
        base_url = "http://172.31.236.2:9001"
        # /api/rcs/warehouse/{warehouseId}/lockedZoneQuery/getPointsCongestionLevel
        url = base_url + "/api/rcs/traffic/info/getPointToAgvMap"
        form_headers = {
            "Accept": "*/*"
        }
        data = {
            "username": "root",
            "password": "root123"
        }
        response = requests.get(url=url, data=data, headers=form_headers)
        # data：key为码点pointCode，value为小车agvCode
        data = json.loads(response.text)['data']

        # key为point_point, value为 距离  距离矩阵制造
        distance_map = {}

        # 聚类字典，
        # key为聚类name，
        # value为点集合Set
        # 点位坐标 - 聚类
        cluster_point_map = {}
        point_cluster_map = {}

        cluster_point_map, point_cluster_map = cluster_process(g_point_coord, data)

        cluster_points = []  # 存放每个聚类的x, y坐标
        for i in cluster_point_map.keys():
            each_cluster_set = cluster_point_map[i]
            each_cluster_set_cood = []
            for each_cluster in each_cluster_set:
                each_cluster_set_cood.append(g_point_coord[each_cluster])

            cluster_points.append(each_cluster_set_cood)

        x_c, y_c = [], []
        for item in cluster_points:
            x_each, y_each = zip(*item)
            x_c.append(x_each)
            y_c.append(y_each)

        # agv坐标位置
        connect_mysql = pymysql.connect(host="172.31.236.2", port=3306, user="root", password="root123",
                                        database="evo_rcs", charset="utf8")
        cursor = connect_mysql.cursor()
        sql = "SELECT agv_code, x, y FROM  agv_pd_status"
        cursor.execute(sql)
        agv_data = cursor.fetchall()
        connect_mysql.close()
        agv_coords = []
        for i in agv_data:
            if i is not None:
                pc, x, y = i
                agv_coords.append((x, y))
        x_c6, y_c6 = zip(*agv_coords)

        plt.clf()
        # 4.散点图实时更新状态信息
        x, y = zip(*g_point_coords)
        plt.scatter(x, y, c='g', marker="+")

        # 红色：（3, 4]   # 品红 （2, 3]   # 蓝色（1, 2]    # 青蓝 （0, 1]

        color_dict = {0: 'r', 1: 'm', 2: 'b', 3: 'c', 4: 'darkorange', 5: "aliceblue", 6: "darksalmon", 7: "crimson",
                      8: "darkmagenta", 9: "mediumorchid", 10: "violet"}

        plt.scatter(x_c5, y_c5, c='gray', marker="s")
        plt.scatter(x_c6, y_c6, c='green', marker="s")
        plt.scatter(x_c7, y_c7, c='w', marker="d", edgecolors='k')

        for cluster_index in range(len(x_c)):
            x_plt = x_c[cluster_index]
            y_plt = y_c[cluster_index]
            plt.scatter(x_plt, y_plt, c=color_dict[cluster_index % 10], marker='o', alpha=0.8)

        plt.grid(True, which='both', linewidth=0.2)

        plt.pause(0.1)
        # matplotlib.animation 保存为gif格式
        # plt.savefig('picture.png', dpi=300)
        plt.ioff()
        # plt.show()
