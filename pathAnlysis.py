# -*- coding: utf-8 -*-
import re

import requests
import json
import simulation_simple
import re
from data import road_way


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


if __name__ == "__main__":
    logs = "F:/QP/wanyitongpath/logData/log_traffic123.log"
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
    map_path = "F:/QP/wanyitong插件/DEBR2_001_10.7.8allcost1.json"
    _, _, _, storage_points, station_points, _, _ = simulation_simple.preprocess_point_data(map_path)

    end_stations = ["J3riEw", "Mk8Ki5", "x32ASj", "wsf4DR", "kTAr5m", "45QNwc", "QSkzMG", "PritSc", "DcrWAc", "fB6QX6",
                    "DnGWAW", "e24Dai", "pcFAsk", "KcmZRr", "efhTPN", "mYDApJ", "z6ZcE3", "wNMAKa", "xjhtzZ", "6GcJMz",
                    "WbJYcC", "NekZEM", "Bxr32p", "7NfcyT", "xMsz75", "eQCXtJ", "EbF23i", "Y3byYj"]

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
    roadWay_detour_station = {}
    roadWay_detour_storage = {}
    print("-----------------路径规划数量---------------------")
    print(len(path_dict))
    for roadWay in road_ways:
        area_list = [roadWay]
        # 从巷道存储点出发的点
        road_go_station = {}
        # 去存储点的任务
        station_go_storage = {}
        points_list = get_area(area_list)

        # 获取对应巷道内的存储点
        road_way_storages = []
        for point in points_list:
            if point in storage_points:
                road_way_storages.append(point)

        for key in path_dict:
            path = path_dict[key]
            start_pt = path[0]
            end_pt = path[-1]
            # 出库任务
            if start_pt in road_way_storages and end_pt in end_stations:
                road_go_station[key] = path

            # 带载入库任务
            if end_pt in road_way_storages and key in bucket_dict.keys() and bucket_dict[key]:
                station_go_storage[key] = path

        # 获取理想路径，区分带载状态
        ideal_station_path_dict = {}
        ideal_storage_path_dict = {}
        for key in road_go_station.keys():
            start_p = key.split("_")[0]
            end_p = key.split("_")[1]
            if key not in bucket_dict.keys():
                continue
            base_paths = ideal_base_path(start_p, end_p, bucket_dict[key])
            if len(base_paths) <= 0:
                continue
            ideal_station_path_dict[key] = base_paths

        for key in station_go_storage.keys():
            start_p = key.split("_")[0]
            end_p = key.split("_")[1]
            if key not in bucket_dict.keys():
                continue
            base_paths = ideal_base_path(start_p, end_p, bucket_dict[key])
            if len(base_paths) <= 0:
                continue
            ideal_storage_path_dict[key] = base_paths

        # print(base_path_dict)
        diff_path_dict_station = {}
        diff_path_dict_storage = {}
        # 计算绕路程度 key为 起点_终点
        for key in ideal_station_path_dict.keys():
            diff = (len(path_dict[key]) - len(ideal_station_path_dict[key])) / (len(path_dict[key]))
            if diff == 0:
                continue
            # if diff < 0:
            #     print("--------")
            #     print(path_dict[key])
            #     print(ideal_station_path_dict[key])
            diff_path_dict_station[key] = diff
            roadWay_detour_station[roadWay + "_" + key] = diff

        for key in ideal_storage_path_dict.keys():
            diff = (len(path_dict[key]) - len(ideal_storage_path_dict[key])) / (len(path_dict[key]))
            if diff == 0:
                continue
            # if diff < 0:
            #     print("--------")
            #     print(path_dict[key])
            #     print(ideal_storage_path_dict[key])
            #     print("--------")
            diff_path_dict_storage[key] = diff
            roadWay_detour_storage[roadWay + "_" + key] = diff

        # if diff_path_dict_station is not None:
        #     print("------------------------------------------")
        #     print(roadWay)
        #     print(diff_path_dict_station)
        #     print(diff_path_dict_storage)

    print("-----------------------------------------")
    if len(roadWay_detour_station) > 0:
        average_detour_station = sum(roadWay_detour_station.values()) / len(roadWay_detour_station)
        print("-----------出库绕路平均-------------")
        print(average_detour_station)

    if len(roadWay_detour_station) > 0:
        average_detour_storage = sum(roadWay_detour_storage.values()) / len(roadWay_detour_storage)
        print("-----------返库绕路平均-------------")
        print(average_detour_storage)

    #################################################################################
    # 绕路统计
    # 所有的有绕路的任务
    #################################################################################
    ideal_path_dict = {}
    diff_path_dict = {}
    for key in path_dict.keys():
        start_p = key.split("_")[0]
        end_p = key.split("_")[1]
        if key not in bucket_dict.keys():
            continue
        ideal_path = ideal_base_path(start_p, end_p, bucket_dict[key])
        if len(ideal_path) <= 0:
            # 只统计青鸾车的
            continue
        ideal_path_dict[key] = ideal_path

    detour_paths = {}
    cut_paths = {}
    if len(ideal_path_dict) > 0:
        for key in ideal_path_dict.keys():
            diff = (len(path_dict[key]) - len(ideal_path_dict[key])) / (len(path_dict[key]))
            if diff == 0:
                continue
            if diff > 0:
                print("----------increase paths----------")
                # print(path_dict[key])
                # print(ideal_path_dict[key])
                detour_paths[key] = diff
                if key == "RB2Fk8_ydCKRF_MoveSub_____53f4a145c164c43a":
                    print(path_dict[key])
                    print(ideal_path_dict[key])
            else:
                cut_paths[key] = diff
            diff_path_dict[key] = diff

    print("----------------平均绕路统计-------------------")
    average_detour_all = sum(diff_path_dict.values()) / len(diff_path_dict)
    print(average_detour_all)
    print("-----------------路径规划数量---------------------")
    print(len(path_dict))
    print("-----------------路径绕路数量---------------------")
    print(len(detour_paths))
    print("-----------------路径缩短数量---------------------")
    print(len(cut_paths))
    print("------------------绕路路径-----------------------")
    print(sorted(detour_paths.items(), key=lambda x: x[1], reverse=True))
