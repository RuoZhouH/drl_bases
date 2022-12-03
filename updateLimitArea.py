# -*- coding: utf-8 -*-

import json
import requests
import pymysql
import paramiko
import datetime


def preprocess_point_data(map_data, road_way_entry_points):
    """预处理点数据, 以加速之后使用"""
    from_to_entry = {}
    for zl in map_data['lineList']:
        # for line in zl['pointList']:
        start_point = zl["startPointCode"]
        to_point = zl["endPointCode"]
        if to_point in road_way_entry_points:
            from_to_entry[start_point] = to_point
    return from_to_entry


###############################################
# 1. 取巷道入口点
###############################################

base_url = "http://172.31.236.2"
base_ip = "172.31.236.2"
url = base_url + ":9001" + "/rcs/agv/cache/basic/getArea"
form_headers = {
    "Accept": "*/*"
}
data = {
    "username": "root",
    "password": "root123"
}
response = requests.post(url=url, data=data, headers=form_headers)
# data：key为码点pointCode，value为小车agvCode
data = json.loads(response.text)['data']

road_way_entry_points = []
for area in data["ROAD_WAY"]:
    area_value = area["jsonData"]
    agvEntry = json.loads(area_value)
    road_way_entry_points.append(agvEntry["carryAgvEntry"])

limit_area_name = []
for area in data["LimitArea"]:
    area_id = area["id"]
    limit_area_name.append(int(area_id))


###############################################
# 2. 取地图文件数据
###############################################
# 获取小车货架实时点位（查数据库）
connect_mysql = pymysql.connect(host=base_ip, port=3306, user="root", password="root123",
                                database="evo_rcs", charset="utf8")
cursor = connect_mysql.cursor()
sql = "SELECT map_path,map_url FROM  base_map where map_state = \'OnLine\' and state = \'effective\'"
sql_id = "SELECT id FROM  base_area"
sql_area = "SELECT id,area_code FROM  base_area where area_type = \'LimitArea\' and state = \'effective\'"
cursor.execute(sql)
map_info = cursor.fetchall()

# 获取id区域信息
cursor.execute(sql_id)
id_info = cursor.fetchall()
id_total = []
for id_single in id_info:
    id_total.append(id_single[0])
max_id = max(id_total)

# 获取区域信息
cursor.execute(sql_area)
area_list = []
area_info = cursor.fetchall()
for area_single in area_info:
    area_list.append(area_single[1])


map_data_url = map_info[0][1]
# map_data = json.loads(map_data_url)

## 一种方式，登录服务器获取地图文件数据

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect("主机名", 端口22, "用户名", "密码", "超时时间")
ssh.connect(base_ip, 22, "root", "123qweasd", timeout=30)

file_path = map_info[0][0].split("/")
name_file = file_path[-1]
cd_path = "/" + file_path[1] + "/docker/" + file_path[2] + "/" + file_path[3]
# 执行多条命令直接在exec_command()使用；分隔即可
# stdin, stdout, stderr = ssh.exec_command("cd "+cd_path)

sftp_client = ssh.open_sftp()
# remote_file = sftp_client.open(map_path[0][0])
# '/opt/docker/evo-rcs/maps/001_13.2.1.json'
remote_file = sftp_client.open(cd_path + "/" + name_file)
map_data = json.loads(remote_file.read().decode())

## 另一种方式，根据URL获取
# forms_headers = {
#     "Accept": "*/*"
# }
# map_data = requests.post(url=map_data_url, data=data, headers = forms_headers)

## 读取本地文件


###############################################
# 3. 获取需要纳入限流区的点集合
###############################################
from_to_entry = preprocess_point_data(map_data, road_way_entry_points)
limit_area_sql = "INSERT IGNORE INTO evo_rcs.base_area(id,create_time,create_user,update_time,update_user,agv_type_code,area_code,area_name,area_type," \
                 "json_data,point_code,state,super_area_id,warehouse_id,zone_code,zone_id)VALUES(%s,%s,'admin',%s,'admin',-1, %s,'','LimitArea','{}',%s,'effective',NULL,1,'kckq',1);"
start_id = max_id + 1
limit_area_str = 'LimitArea' + str(start_id)
for k, v in from_to_entry.items():
    while limit_area_str in area_list:
        limit_area_str = 'LimitArea' + str(start_id + 1)
    timenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(limit_area_sql, (start_id, timenow, timenow, limit_area_str, k+','+v))
    connect_mysql.commit()
    start_id += 1
    limit_area_str = 'LimitArea' + str(start_id)
    print("insert limit area for " + str(start_id) + " " + k+','+v)
    print("-------------------------")

connect_mysql.close()
print("-------------------------")
print("this is the end")
# ROAD_WAY
# road_way_area = response.text