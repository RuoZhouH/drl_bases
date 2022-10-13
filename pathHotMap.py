# -*- coding: utf-8 -*-
import re

import requests
import json
import simulation_simple
import re
from data import road_way

import pandas as pd
import numpy as np
import cmapTest as cm
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors


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


if __name__ == "__main__":
    # logs = "F:/QP/liupintangdata/logData/origin/testOrigins.log"
    # testCongestions.log
    logs = "F:/QP/liupintangdata/logData/congestion1/testCongestions.log"
    pattern = ".*mes\":(.*)| .*"
    pattern_path = '2022.*?"actionId":"(.*?)".*?updateAgvContextPath\|current.*?path\|pathStr:(.*?)->\|turningStr:(.*?)->"'
    pattern_bucket = '2022.*?"actionId":"(.*?)".*?preMove.*?withBucket=(.*?),.*?startPos=(.*?),.*?trueDestCode=\'(.*?)\''
    path_dict = {}
    turning_dict = {}
    bucket_dict = {}

    road_ways = road_way.Road_way.ROADWAYS
    # 提取更新后的路径
    for line in open(logs, "r", encoding='UTF-8'):
        match_path = re.match(pattern_path, line)
        match_bucket = re.match(pattern_bucket, line)
        if match_path:
            action_id = match_path.group(1)
            path = match_path.group(2).split("->")
            turning_points = match_path.group(3).split("->")
            start_point = path[0]
            end_point = path[-1]
            keyStr = start_point + "_" + end_point + "_" + action_id
            path_dict[keyStr] = path
            turning_dict[keyStr] = turning_points

        if match_bucket:
            isLoading = False
            action_id = match_bucket.group(1)
            with_bucket = match_bucket.group(2)
            start_point = match_bucket.group(3)
            end_point = match_bucket.group(4)
            keyStr = start_point + "_" + end_point + "_" + action_id
            if with_bucket is not None:
                if "true" == with_bucket:
                    isLoading = True
            bucket_dict[keyStr] = isLoading

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
    map_path = "F:/QP/liupintangdata/map/LPT_LPT_4.4.1.json"
    _, _, g_point_coord, storage_points, station_points, _ = simulation_simple.preprocess_point_data(map_path)

    end_stations = ["J3riEw", "Mk8Ki5", "x32ASj", "wsf4DR", "kTAr5m", "45QNwc", "QSkzMG", "PritSc", "DcrWAc", "fB6QX6",
                    "DnGWAW", "e24Dai", "pcFAsk", "KcmZRr", "efhTPN", "mYDApJ", "z6ZcE3", "wNMAKa", "xjhtzZ", "6GcJMz",
                    "WbJYcC", "NekZEM", "Bxr32p", "7NfcyT", "xMsz75", "eQCXtJ", "EbF23i", "Y3byYj"]

    main_way_points = ["eCi2KG","hWSJcB","NMNM67","WtJwWy","H5ycDZ","inxZYY","4b6SME","wwZa4R","KXAWK8","7yRXPy","JGrFtf",
                       "fJbzG7","QfydHW","nDRcNC","FeYmBj","M4zdAA","3ymWnT","7rB6SZ","X4HxtW","xpd2zi","efFiX5","szMP6E",
                       "fJccnT","BddDXA","dmPrWx","cWQDyP","thGwnw","tcPzY7","DNTz45","6BCcXw","KSB4DM","jdpRhD","kkpwGx",
                       "aMriZh","wpnx83","FRTEMD","twJiwi","xCZTR2","Z5BEah","6R5fYX","2WMjYc","HcPfyJ","6zjjyd","ReBwbe",
                       "Z7C3Dz","Z537yP","Xk6mr5","i6wFFX","ZDtRJt","2tYZs8","Z4f3eY","GwJCNp","e6njxh","7ZFaPa","B6C2fh",
                       "c2SKtm","wbjTp5","5CrmdK","NJi534","cCB4j8","tkxRhZ","kzf3dH","fkNKk4","h4Nhwh","nDaf8m","5ACbPM",
                       "G52Wip","GpbQsc","fRxrQ2","xYZcyC","Cb2fPN","6M7eHJ","7ZbweC","3rT3p2","bjdzBm","8m4r3Z","2QpktB",
                       "Fem4ar","2NT8ty","KjepQt","t3GfZy","AY6eFC","65xjBb","aHkBmr","k63FFz","erPBHM","7Nef4c","S86MiS",
                       "E6m6DG","x5t24b","44TyB4","dYAaJs","5wiH3D","3xETWY","F8GN53","GWKaDJ","i5jZDi","rxhrjA","NAWXRY",
                       "tXT665","KzfQib","JBEZT8","jKGjcz","JwJBHh","dsWnJy","h8NjhN","FD3WHH","XE7RaQ","RZJWN2","8ZTtZC",
                       "wjKmSz","NM5cYr","KtAwZw","ERRb7f","yzHtRP","rkfWBK","2wtRwe","7hNMef","HK5RpC","m23eTf","ckKMez",
                       "rjwBs5","esBW2x","PAG7C8","bzk3pt","cWApQB","w32SRh","ndmCws"]

    go_station_path = {}
    go_storage_path = {}
    #
    # for key in path_dict:
    #     path = path_dict[key]
    #     start_pt = path[0]
    #     end_pt = path[1]
    #     if start_pt in storage_points and end_pt in station_points:
    #         go_station_path[key] = path

    #################################################################################
    # 绕路统计
    # 出库任务  返库任务等
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
    print(len(path_dict))
    for path in path_dict.values():
        for point in path:
            if point not in main_way_points:
                continue
            point_belong[point] += 1

    for pt in main_way_points:
        x = g_point_coord[pt][0]
        y = g_point_coord[pt][1]
        X_coord.append(x)
        Y_coord.append(y)
        C_cmap.append(point_belong[pt])

    #vmin=0, vmax=20, s=35
    plt.figure(figsize=(12, 4))
    # fig = plt.figure()
    # ax = plt.add_subplot(111)
    plt.scatter(X_coord, Y_coord, marker='o', c=C_cmap, s=100, cmap='cool')
    plt.show()







