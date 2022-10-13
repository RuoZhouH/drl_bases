# -*- coding: utf-8 -*-
import re
import gzip
import simulation_simple

import io, sys, json
import math

import matplotlib.pyplot as plt
import pylab as p
import requests
import time
import pymysql
from appdirs import unicode
import queue
import os


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
storage_points = []
station_points = []
waiting_points = []
path_point = []



def preprocess_point_data(map_json):
    """预处理点数据, 以加速之后使用"""
    map_json = load_map_json_file(map_json)
    global g_point_codes
    global g_point_coords
    global g_point_coord
    global storage_points
    global station_points
    global path_point
    for zl in map_json['zoneList']:
        for point in zl['pointList']:
            pc = point['pointCode']
            ptype = point['pointType']
            x, y = point['x'], point['y']
            g_point_codes.append((pc, x, y))
            g_point_coords.append((x, y))
            g_point_coord[pc] = (x, y)
            if ptype == "STORAGE":
                storage_points.append(pc)
            if ptype == "STATION_WORKING":
                station_points.append(pc)
            if ptype == "STATION_WAITING":
                waiting_points.append(pc)
            if ptype == "":
                path_point.append(pc)
    return g_point_codes, g_point_coords, g_point_coord, storage_points, station_points, waiting_points, path_point


def get_file_names(file_dir, content_range):
    # 当前文件夹，文件目录层级（0代表当前层级，1代表1级子文件夹，2代表2级子文件夹）
    i = 0
    for root, dirs, files in os.walk(file_dir):
        # print(root) # 当前目录路径
        # print(dirs) # 当前路径下所有子目录
        print("目录层级：", i)
        print(files)  # 当前路径下所有非目录子文件
        if i == content_range:
            return files
        i += 1


"""
QP青鸾车交叉、排队次数统计
"""
if __name__ == "__main__":

    # 日志路径，按时间段抓取的log，命令行：
    # cd /opt/docker/evo-rcs/logs/traffic/

    # 如 20:30至21:00时间段日志抓取
    # cat log_traffic.log.2022-09-01-* | zgrep "2022-09-01 20:[3-5][0-9]:[0-5][0-9]" > test1.log
    # 打压缩包 tar -zcvf test1.log.gz test1.log

    # 如 12:00至12:30时间段日志抓取
    # cat log_traffic.log.2022-09-01-* | zgrep "2022-09-01 12:[0-2][0-9]:[0-5][0-9]" > test2.log
    # 打压缩包 tar -zcvf test2.log.gz test2.log

    # 最后下载放置到指定目录files_path下，运行脚本即可

    files_path = "F:/QP/wanyitongpath/logData/congestion/crosslog/"
    # files_path = "F:/QP/liupintangdata/logData/congestion1/change/"

    # 地图路径
    map_path = "F:/QP/wanyitong插件/DEBR2_001_10.7.8allcost1.json"
    # map_path = "F:/QP/liupintangdata/map/LPT_LPT_4.4.1.json"
    # log_file = "log_traffic30.log"
    # log_file = "log_traffic.log.2022-08-31-7.gz"
    log_files = get_file_names(files_path, 0)

    cross_times = []

    # 遍历日志文件
    for log_file in log_files:
        print("日志文件：", log_file)
        file = files_path + log_file
        file_name_list = log_file.split(".")
        f = None
        lines = []
        if file_name_list[-1] == "gz":
            f = gzip.open(file, "rb")
            for s in f.readlines():
                line = s.decode()
                lines.append(line)
        elif file_name_list[-1] == "log":
            f = open(file, "r", encoding='UTF-8')
            lines = f

        if f is None or lines is None:
            continue
        _, _, _, storage_points, station_points, waiting_points,_ = preprocess_point_data(map_path)
        pattern_speed = '2022.*?MessageRouterHandler.*?\- (.*?)\|START\|curPos\|(.*?)\|.*?\|speed\|(.*?)\|handler\|.*?\|(.*?)\|'
        pattern_path = '2022.*?"actionId":"(.*?)".*?updateAgvContextPath\|current.*?path\|pathStr:(.*?)->\|turningStr:(.*?)->"'
        cross_agv_times = {}
        agv_cross = set()
        cross_points = set()
        speed_value = set()
        #路径获取
        path_dict = {}
        turning_dict = {}

        for line in lines:
            match_path = re.match(pattern_path, line)
            if match_path:
                action_id = match_path.group(1)
                paths = match_path.group(2).split("->")
                turning_points = match_path.group(3).split("->")
                # start_point = path[0]
                # end_point = path[-1]
                # keyStr = start_point + "_" + end_point + "_" + action_id
                path_dict[action_id] = paths
                turning_dict[action_id] = turning_points

        if not isinstance(lines, list):
            lines.seek(0)

        for sline in lines:
            match_speed = re.match(pattern_speed, sline)
            if match_speed and len(match_speed.groups()) > 3:
                agv_code = match_speed.group(1)
                point = match_speed.group(2)
                speed = match_speed.group(3)
                saction_id = match_speed.group(4)
                # 速度为0，统计青鸾车的, 不是工作站排队，不是起终点，不是拐弯点
                if speed == '0.0' and 'CAR' in agv_code \
                        and point not in station_points \
                        and point not in waiting_points\
                        and saction_id in turning_dict.keys()\
                        and point not in turning_dict[saction_id]:
                    one_key = agv_code + '_' + point + '_' + speed + '_' + saction_id
                    agv_cross.add(one_key)
                    cross_points.add(point)
                if speed != '0.0' and float(speed) > 0.1:
                    speed_value.add(float(speed))

        print("----------交叉次数统计----------")
        print(len(agv_cross))
        cross_times.append(len(agv_cross))

        print("----------平均速度----------")
        if len(speed_value) > 0:
            print(sum(speed_value)/len(speed_value))
        f.close()

    print("----------总次数----------")
    print(sum(cross_times))

