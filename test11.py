#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import pandas as pd

path = "F:/QP/congestion/cubynLogData/"
file_name = "density182.log"
file = path + file_name
pattern = ""
roadWayList = ["ROAD_WAY010", "ROAD_WAY004sub", "ROAD_WAY008sub", "ROAD_WAY001sub", "ROAD_WAY008", "ROAD_WAY009",
               "ROAD_WAY006", "ROAD_WAY007", "ROAD_WAY004", "ROAD_WAY005", "ROAD_WAY002", "ROAD_WAY003", "ROAD_WAY011", "ROAD_WAY001"]


densityDict = {}.fromkeys(roadWayList)
speedDict = {}.fromkeys(roadWayList)
densityTimeList = []
speedTimeList = []

densityData = pd.DataFrame(columns=("ROAD_WAY010", "ROAD_WAY004sub", "ROAD_WAY008sub", "ROAD_WAY001sub", "ROAD_WAY008", "ROAD_WAY009",
               "ROAD_WAY006", "ROAD_WAY007", "ROAD_WAY004", "ROAD_WAY005", "ROAD_WAY002", "ROAD_WAY003", "ROAD_WAY011", "ROAD_WAY001"))
speedData = pd.DataFrame(columns=("ROAD_WAY010", "ROAD_WAY004sub", "ROAD_WAY008sub", "ROAD_WAY001sub", "ROAD_WAY008", "ROAD_WAY009",
               "ROAD_WAY006", "ROAD_WAY007", "ROAD_WAY004", "ROAD_WAY005", "ROAD_WAY002", "ROAD_WAY003", "ROAD_WAY011", "ROAD_WAY001"))


i = 0

for line in open(file, "r", encoding='UTF-8'):
    if roadWayList is None or line is None:
        continue

    strList = line.split("|")
    strDensity = strList[0]
    strSpeed = strList[1]
    densityVariance = strList[2]
    speedVariance = strList[3]
    densityTimeList.append(densityVariance.split(":")[1][:5])
    speedTimeList.append(speedVariance.strip("\n").split(":")[1][:5])

    for roadWay in roadWayList:
        densityDict[roadWay] = 0
        speedDict[roadWay] = 0
        # pattern = ".*-\s(.+):{(.+)=(.+),\s(.+)=(.+),\s(.+)=(.+)}|"
        pattern = ".*" + roadWay + "=(.+),.*?"
        density = re.match(pattern, strDensity)
        speed = re.match(pattern, strSpeed)
        if density is not None:
            resDen = density.groups()
            resSpe = speed.groups()
            densityDict[roadWay] = resDen[0].split(",")[0][:5]
            speedDict[roadWay] = resSpe[0].split(",")[0][:5]
            print(roadWay + ": density:" + resDen[0].split(",")[0][:5] + "  speed: " + resSpe[0].split(",")[0][:5])
    # print(line)

    tempData1 = [densityDict]
    tempDf1 = pd.DataFrame(tempData1, index=[i], columns=densityDict.keys())
    tempData2 = [speedDict]
    tempDf2 = pd.DataFrame(tempData2, index=[i], columns=speedDict.keys())
    densityData = densityData.append(tempDf1)
    speedData = speedData.append(tempDf2)

    i+=1

# densityData.to_csv()
# speedData.to_csv()

print("---------------------------------")
print(densityTimeList)
print("---------------------------------")
print(speedTimeList)
#保存
densityData["Variance"] = densityTimeList
speedData["Variance"] = speedTimeList
writer = pd.ExcelWriter('./result.xlsx')
for i in ['densityData', 'speedData']:
       eval(i).to_excel(excel_writer=writer, sheet_name=i, index=False)
writer.save()
writer.close()