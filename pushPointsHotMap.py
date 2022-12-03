# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import copy
import re

import requests
import json
import simulation_simple
import re
from data import road_way

import pandas as pd
import numpy as np
import matplotlib.cm as cm
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import datetime
import time
import gif

def ideal_base_path(start, end, withBucket):
    # 代价最小路径规划查询接口
    hostIp = "172.31.236.2"

    baseUrl = "http://172.31.236.2:9001"
    findPath = "/api/rcs/traffic/info/getPath"
    findPath2 = "/api/rcs/traffic/info/getPath2"
    urlPath1 = baseUrl + findPath
    urlPath2 = baseUrl + findPath2
    form_headers = {
        "Accept": "*/*"
    }
    data = {
        "agvCode": "CARRIER_10012172100",
        "startPoint": start,
        "destPoint": end,
        "withBucket": withBucket,
        "follow": True
    }
    response = requests.post(url=urlPath1, data=data, headers=form_headers)
    result = json.loads(response.text)['data']
    basePath = []
    for point in result:
        basePath.append(point['code'])

    # simulation = simulation_simple.Simulation(basePath, "./map/DEBR.json")
    # simulation.pic_make()

    # print(data["agvCode"])
    # print(basePath)

    return basePath


def manhadun_base_path(start, end):
    pass


def get_area(areaCodeList):
    base_url = "http://172.31.236.2:9001"
    # get_area = "api/rcs/basic/warehouse/1/area/getAreaByType"
    post_area = "/api/rcs/basic/warehouse/1/area/getAreaByCodeList"
    find_area = base_url + post_area

    form_headers = {
        "Accept": "*/*",
        "Content-Type": "application/json"
    }
    data = areaCodeList

    response = requests.post(url=find_area, data=json.dumps(data), headers=form_headers)
    result = json.loads(response.text)['data']
    return result[0]["pointCodeList"]

def hot_map(data, name):
    img = plt.imread(r'E:\运营分析\临沂六品堂\lpt.png')
    fig, ax = plt.subplots(figsize=(5, 5), dpi=200)
    # print(map.x.min(), map.y.min(), map.x.max(), map.y.max())
    map = pd.read_csv(r'E:\运营分析\临沂六品堂\LPT_map.csv', engine='python')
    ax.imshow(img, extent=[map.x.min(), map.x.max(), map.y.min(), map.y.max()])
    p = sorted(set(data['job_id'].tolist()))
    colormap = cm.autumn_r
    colorlist = [colors.rgb2hex(colormap(i)) for i in np.linspace(0, 0.9, len(p))]
    print(p, colorlist)
    print(type(p))
    c = 0
    for _p in p:
        # print(_p)
        ax.scatter(data[data['job_id'] == _p]['x'], data[data['job_id'] == _p]['y'], s=3, c=colorlist[c])
        c += 1
    plt.legend(p,
               fontsize=3.5,
               bbox_to_anchor=(1.0, 1),
               ncol=math.ceil(len(p)/20))
    plt.show()
    fig = ax.get_figure()
    fig.savefig(r'd:/%s.svg' % name, format='svg', dpi=150)


def map_scatter(map_path):
    g_point_codes, g_coords, g_point_coord, storage_points, station_points, waiting_points,_ = simulation_simple.preprocess_point_data(map_path)
    return g_point_codes, g_coords, g_point_coord, storage_points, station_points, waiting_points


def get_time_stamp(valid_time):
    dd = datetime.datetime.strptime(valid_time, '%Y-%m-%d %H:%M:%S,%f')
    # dd = datetime.datetime.strptime(valid_time, '%H:%M:%S')
    ts = int(time.mktime(dd.timetuple()) * 1000.0 + (dd.microsecond / 1000.0))
    return ts


if __name__ == "__main__":
    # logs = "F:/QP/liupintangdata/logData/congestion1/testCongestions.log"
    # logs = "F:/QP/liupintangdata/logData/origin/testOrigins.log"
    # logs = 'F:/QP/wanyitongpath/logData/origin/pushPointso1.log'

    #################################################################################
    # 按时间段提取推点信息
    #
    #################################################################################
    # 按时间提取
    logs = 'F:/QP/wanyitongpath/logData/congestion/test2.log'
    # pattern = ".*mes\":(.*)| .*"
    # pattern_path = '2022.*?"actionId":"(.*?)".*?updateAgvContextPath\|current.*?path\|pathStr:(.*?)->\|turningStr:(.*?)->"'
    # pattern_bucket = '2022.*?"actionId":"(.*?)".*?preMove.*?withBucket=(.*?),.*?startPos=(.*?),.*?trueDestCode=\'(.*?)\''
    # pattern_push_points = '2022.*?PointPushService.*?wayPoints=\[(.*?)\].*'
    pattern_last_push_points = '2022\-(.*?)\ INFO.*?PointPushService.*?wayPoints=\[(.*?)\].*'

    # 日志年份
    years = "2022-"
    start_time = None
    end_time = None
    # path_dict = {}
    # turning_dict = {}
    # bucket_dict = {}

    push_list = []
    push_total_list = []
    time_list = []
    delata_time = 2*60*1000
    road_ways = road_way.Road_way.ROADWAYS
    # 提取时间戳
    for line in open(logs, "r", encoding='UTF-8'):
        match_path = re.match(pattern_last_push_points, line)
        # match_bucket = re.match(pattern_bucket, line)
        if match_path:
            ts1 = get_time_stamp(years + match_path.group(1).split(' ')[0] + ' ' + match_path.group(1).split(' ')[1])
            time_list.append(ts1)

    #################################################################################
    # 根据时间戳获取开始时间与结束时间
    # 然后根据时间段获取各个时间段的锁闭信息
    #################################################################################
    # delata_time为时间段间隔
    start_time = min(time_list)
    end_time = max(time_list)
    n = 0
    for line in open(logs, "r", encoding='UTF-8'):
        match_path = re.match(pattern_last_push_points, line)
        if match_path:
            ts2 = get_time_stamp(years + match_path.group(1).split(' ')[0] + ' ' + match_path.group(1).split(' ')[1])
            if start_time + delata_time * n < ts2 < start_time + delata_time * (n + 1) and ts2 < end_time:
                listpoint = match_path.group(2).split(', ')
                if listpoint is not None:
                    push_list.append(listpoint)
            elif ts2 >= start_time + delata_time * (n+1):
                push_total_list.append(push_list)
                push_list = []
                listpoint = match_path.group(2).split(', ')
                if listpoint is not None:
                    push_list.append(listpoint)
                n += 1


        # agv_code = agv_code_pattern.group(1).split("|")[0].split("\"")[1]
        # path = agv_code_pattern.group(1).split("|")[5].split(":")[1].split("->")[:-1]
        # start_point = path[0]
        # end_point = path[-1]
        # keyStr = start_point + "_" + end_point
        # turning_points = agv_code_pattern.group(1).split("|")[6].split(",")[0].split(":")[1].split("->")[:-1]
        # path_dict[keyStr] = path
        # turning_dict[keyStr] = turning_points

    # print(path_dict)
    # print(turning_dict)

    # 获取是出库任务或者入库任务的起终点路径
    # 获取离线站任务的起终点路径
    # map_path = "F:/QP/liupintangdata/map/LPT_LPT_4.4.1.json"
    map_path = u'F:/QP/wanyitong插件/DEBR2_001_10.7.8allcost1.json'
    _, g_coords, g_point_coord, storage_points, station_points, _, path_points = simulation_simple.preprocess_point_data(map_path)

    # end_stations = ["J3riEw", "Mk8Ki5", "x32ASj", "wsf4DR", "kTAr5m", "45QNwc", "QSkzMG", "PritSc", "DcrWAc", "fB6QX6",
    #                 "DnGWAW", "e24Dai", "pcFAsk", "KcmZRr", "efhTPN", "mYDApJ", "z6ZcE3", "wNMAKa", "xjhtzZ", "6GcJMz",
    #                 "WbJYcC", "NekZEM", "Bxr32p", "7NfcyT", "xMsz75", "eQCXtJ", "EbF23i", "Y3byYj"]

    # main_way_points = ["eCi2KG","hWSJcB","NMNM67","WtJwWy","H5ycDZ","inxZYY","4b6SME","wwZa4R","KXAWK8","7yRXPy","JGrFtf",
    #                    "fJbzG7","QfydHW","nDRcNC","FeYmBj","M4zdAA","3ymWnT","7rB6SZ","X4HxtW","xpd2zi","efFiX5","szMP6E",
    #                    "fJccnT","BddDXA","dmPrWx","cWQDyP","thGwnw","tcPzY7","DNTz45","6BCcXw","KSB4DM","jdpRhD","kkpwGx",
    #                    "aMriZh","wpnx83","FRTEMD","twJiwi","xCZTR2","Z5BEah","6R5fYX","2WMjYc","HcPfyJ","6zjjyd","ReBwbe",
    #                    "Z7C3Dz","Z537yP","Xk6mr5","i6wFFX","ZDtRJt","2tYZs8","Z4f3eY","GwJCNp","e6njxh","7ZFaPa","B6C2fh",
    #                    "c2SKtm","wbjTp5","5CrmdK","NJi534","cCB4j8","tkxRhZ","kzf3dH","fkNKk4","h4Nhwh","nDaf8m","5ACbPM",
    #                    "G52Wip","GpbQsc","fRxrQ2","xYZcyC","Cb2fPN","6M7eHJ","7ZbweC","3rT3p2","bjdzBm","8m4r3Z","2QpktB",
    #                    "Fem4ar","2NT8ty","KjepQt","t3GfZy","AY6eFC","65xjBb","aHkBmr","k63FFz","erPBHM","7Nef4c","S86MiS",
    #                    "E6m6DG","x5t24b","44TyB4","dYAaJs","5wiH3D","3xETWY","F8GN53","GWKaDJ","i5jZDi","rxhrjA","NAWXRY",
    #                    "tXT665","KzfQib","JBEZT8","jKGjcz","JwJBHh","dsWnJy","h8NjhN","FD3WHH","XE7RaQ","RZJWN2","8ZTtZC",
    #                    "wjKmSz","NM5cYr","KtAwZw","ERRb7f","yzHtRP","rkfWBK","2wtRwe","7hNMef","HK5RpC","m23eTf","ckKMez",
    #                    "rjwBs5","esBW2x","PAG7C8","bzk3pt","cWApQB","w32SRh","ndmCws"]

    go_station_path = {}
    go_storage_path = {}
    main_way_points = []

    # 工作站和货架
    bucket_point_coords = []
    station_point_coords = []
    for i in storage_points:
        if i is not None and i in g_point_coord.keys():
            bucket_point_coords.append(g_point_coord[i])
    for j in station_points:
        if j is not None and j in g_point_coord.keys():
            station_point_coords.append(g_point_coord[j])
    x_c5, y_c5 = zip(*bucket_point_coords)
    x_c7, y_c7 = zip(*station_point_coords)
    x, y = zip(*g_coords)


    # 用坐标限定统计的主干道的范围
    for pp in path_points:
        if g_point_coord[pp][0] > 12200 and g_point_coord[pp][0] < 79700 \
                and g_point_coord[pp][1] < 9700 and g_point_coord[pp][1] > 5500:
            main_way_points.append(pp)

    print("main way points size", len(main_way_points))

    #################################################################################
    # 主干道锁闭点统计
    # 根据码点申请次数来计数
    #################################################################################

    # 获取指定巷道的存储点
    point_belong = {}.fromkeys(main_way_points)
    for pt in point_belong.keys():
        point_belong[pt] = 0

    point_coord = {}.fromkeys(main_way_points)
    # for pt in point_coord.keys():
    #     # 找到点对应的x和y的坐标
    #     point_coord[pt] = g_point_coord[pt]
    roadWay_detour_station = {}
    roadWay_detour_storage = {}
    X_coord = []
    Y_coord = []
    C_cmap = []

    print("-----------------路径流量统计---------------------")
    print(len(push_total_list))
    plt.ion()
    # gif.options.matplotlib["dpi"] = 1080

    @gif.frame
    def plot(g_point_coord, main_way_points, point_belong_copy):
        for pt in main_way_points:
            x = g_point_coord[pt][0]
            y = g_point_coord[pt][1]
            X_coord.append(x)
            Y_coord.append(y)
            C_cmap.append(point_belong_copy[pt])
        plt.scatter(X_coord, Y_coord, marker='o', c=C_cmap, s=20, cmap='cool')

    frames = []
    for push_list in push_total_list:
        point_belong_copy = copy.deepcopy(point_belong)
        for path in push_list:
            for point in path:
                if point not in main_way_points:
                    continue
                point_belong_copy[point] += 1

        for pt in main_way_points:
            x = g_point_coord[pt][0]
            y = g_point_coord[pt][1]
            X_coord.append(x)
            Y_coord.append(y)
            C_cmap.append(point_belong_copy[pt])

        plt.clf()
        plt.scatter(x, y, c='g', marker="+")
        plt.scatter(x_c5, y_c5, c='gray', marker="s")
        plt.scatter(x_c7, y_c7, c='w', marker="d", edgecolors='k')
        # plt.figure(figsize=(12, 4))
        # fig = plt.figure()
        # ax = plt.add_subplot(111)
        plt.scatter(X_coord, Y_coord, marker='o', c=C_cmap, s=100, cmap='cool')
        # frame = plot(g_point_coord, main_way_points, point_belong_copy)
        # frames.append(frame)
        # plt.show()
        # time.sleep(5)
        plt.pause(0.9)
        # matplotlib.animation 保存为gif格式
        # plt.savefig('picture.png', dpi=300)
        plt.ioff()
        # plt.show()

    # gif.save(frames, './img/example.gif', duration=3.5, unit="s", between="startend")






