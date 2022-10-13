#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import pandas as pd

path = "F:/QP/congestion/压测任务/LogData/"
file_name = "density01.log"
file = path + file_name
pattern = ""
roadWayList = ["ROAD_WAY0112", "ROAD_WAY0233", "ROAD_WAY0113", "ROAD_WAY0234", "ROAD_WAY0110", "ROAD_WAY0231",
               "ROAD_WAY0111", "ROAD_WAY0232", "ROAD_WAY0116", "ROAD_WAY0117", "ROAD_WAY0114", "ROAD_WAY0115",
               "ROAD_WAY0118", "ROAD_WAY0119", "ROAD_WAY573", "ROAD_WAY0101sub", "ROAD_WAY0120", "ROAD_WAY0123",
               "ROAD_WAY0124", "ROAD_WAY0121", "ROAD_WAY0122", "ROAD_WAY0127", "ROAD_WAY0128", "ROAD_WAY0125",
               "ROAD_WAY0126", "ROAD_WAY0129", "ROAD_WAY0201sub" ,"ROAD_WAY0130", "ROAD_WAY0134", "ROAD_WAY0135", "ROAD_WAY0132",
               "ROAD_WAY0133", "ROAD_WAY0121sub", "ROAD_WAY0303", "ROAD_WAY0304", "ROAD_WAY0301", "ROAD_WAY0302",
               "ROAD_WAY0307", "ROAD_WAY0308", "ROAD_WAY0305", "ROAD_WAY0306", "ROAD_WAY0309", "ROAD_WAY0310",
               "ROAD_WAY0311", "ROAD_WAY0314", "ROAD_WAY0315", "ROAD_WAY0312", "ROAD_WAY0313", "ROAD_WAY0318",
               "ROAD_WAY0319", "ROAD_WAY0316", "ROAD_WAY0317", "ROAD_WAY0221sub", "ROAD_WAY0321", "ROAD_WAY0201", "ROAD_WAY0322",
               "ROAD_WAY0320", "ROAD_WAY0204", "ROAD_WAY0325", "ROAD_WAY0205", "ROAD_WAY0326", "ROAD_WAY0202",
               "ROAD_WAY0323", "ROAD_WAY0203", "ROAD_WAY0324", "ROAD_WAY0208", "ROAD_WAY0329", "ROAD_WAY0209",
               "ROAD_WAY0206", "ROAD_WAY0327", "ROAD_WAY0207", "ROAD_WAY0328", "ROAD_WAY0211", "ROAD_WAY0332",
               "ROAD_WAY0212", "ROAD_WAY0333", "ROAD_WAY0331", "ROAD_WAY0215", "ROAD_WAY0301sub", "ROAD_WAY0216",
               "ROAD_WAY0213", "ROAD_WAY0214", "ROAD_WAY0219", "ROAD_WAY0217", "ROAD_WAY0218", "ROAD_WAY0101",
               "ROAD_WAY0222", "ROAD_WAY0102", "ROAD_WAY0223", "ROAD_WAY0221", "ROAD_WAY0105", "ROAD_WAY0226",
               "ROAD_WAY0106", "ROAD_WAY0227", "ROAD_WAY0103", "ROAD_WAY0224", "ROAD_WAY0104", "ROAD_WAY0225",
               "ROAD_WAY0109", "ROAD_WAY0107", "ROAD_WAY0228", "ROAD_WAY0321sub", "ROAD_WAY0108", "ROAD_WAY0229"]


densityDict = {}.fromkeys(roadWayList)
speedDict = {}.fromkeys(roadWayList)
densityTimeList = []
speedTimeList = []

densityData = pd.DataFrame(columns=("ROAD_WAY0112", "ROAD_WAY0233", "ROAD_WAY0113", "ROAD_WAY0234", "ROAD_WAY0110", "ROAD_WAY0231",
               "ROAD_WAY0111", "ROAD_WAY0232", "ROAD_WAY0116", "ROAD_WAY0117", "ROAD_WAY0114", "ROAD_WAY0115",
               "ROAD_WAY0118", "ROAD_WAY0119", "ROAD_WAY573", "ROAD_WAY0101sub", "ROAD_WAY0120", "ROAD_WAY0123",
               "ROAD_WAY0124", "ROAD_WAY0121", "ROAD_WAY0122", "ROAD_WAY0127", "ROAD_WAY0128", "ROAD_WAY0125",
               "ROAD_WAY0126", "ROAD_WAY0129", "ROAD_WAY0201sub" ,"ROAD_WAY0130", "ROAD_WAY0134", "ROAD_WAY0135", "ROAD_WAY0132",
               "ROAD_WAY0133", "ROAD_WAY0121sub", "ROAD_WAY0303", "ROAD_WAY0304", "ROAD_WAY0301", "ROAD_WAY0302",
               "ROAD_WAY0307", "ROAD_WAY0308", "ROAD_WAY0305", "ROAD_WAY0306", "ROAD_WAY0309", "ROAD_WAY0310",
               "ROAD_WAY0311", "ROAD_WAY0314", "ROAD_WAY0315", "ROAD_WAY0312", "ROAD_WAY0313", "ROAD_WAY0318",
               "ROAD_WAY0319", "ROAD_WAY0316", "ROAD_WAY0317", "ROAD_WAY0221sub", "ROAD_WAY0321", "ROAD_WAY0201", "ROAD_WAY0322",
               "ROAD_WAY0320", "ROAD_WAY0204", "ROAD_WAY0325", "ROAD_WAY0205", "ROAD_WAY0326", "ROAD_WAY0202",
               "ROAD_WAY0323", "ROAD_WAY0203", "ROAD_WAY0324", "ROAD_WAY0208", "ROAD_WAY0329", "ROAD_WAY0209",
               "ROAD_WAY0206", "ROAD_WAY0327", "ROAD_WAY0207", "ROAD_WAY0328", "ROAD_WAY0211", "ROAD_WAY0332",
               "ROAD_WAY0212", "ROAD_WAY0333", "ROAD_WAY0331", "ROAD_WAY0215", "ROAD_WAY0301sub", "ROAD_WAY0216",
               "ROAD_WAY0213", "ROAD_WAY0214", "ROAD_WAY0219", "ROAD_WAY0217", "ROAD_WAY0218", "ROAD_WAY0101",
               "ROAD_WAY0222", "ROAD_WAY0102", "ROAD_WAY0223", "ROAD_WAY0221", "ROAD_WAY0105", "ROAD_WAY0226",
               "ROAD_WAY0106", "ROAD_WAY0227", "ROAD_WAY0103", "ROAD_WAY0224", "ROAD_WAY0104", "ROAD_WAY0225",
               "ROAD_WAY0109", "ROAD_WAY0107", "ROAD_WAY0228", "ROAD_WAY0321sub", "ROAD_WAY0108", "ROAD_WAY0229"))
speedData = pd.DataFrame(columns=("ROAD_WAY0112", "ROAD_WAY0233", "ROAD_WAY0113", "ROAD_WAY0234", "ROAD_WAY0110", "ROAD_WAY0231",
               "ROAD_WAY0111", "ROAD_WAY0232", "ROAD_WAY0116", "ROAD_WAY0117", "ROAD_WAY0114", "ROAD_WAY0115",
               "ROAD_WAY0118", "ROAD_WAY0119", "ROAD_WAY573", "ROAD_WAY0101sub", "ROAD_WAY0120", "ROAD_WAY0123",
               "ROAD_WAY0124", "ROAD_WAY0121", "ROAD_WAY0122", "ROAD_WAY0127", "ROAD_WAY0128", "ROAD_WAY0125",
               "ROAD_WAY0126", "ROAD_WAY0129", "ROAD_WAY0201sub" ,"ROAD_WAY0130", "ROAD_WAY0134", "ROAD_WAY0135", "ROAD_WAY0132",
               "ROAD_WAY0133", "ROAD_WAY0121sub", "ROAD_WAY0303", "ROAD_WAY0304", "ROAD_WAY0301", "ROAD_WAY0302",
               "ROAD_WAY0307", "ROAD_WAY0308", "ROAD_WAY0305", "ROAD_WAY0306", "ROAD_WAY0309", "ROAD_WAY0310",
               "ROAD_WAY0311", "ROAD_WAY0314", "ROAD_WAY0315", "ROAD_WAY0312", "ROAD_WAY0313", "ROAD_WAY0318",
               "ROAD_WAY0319", "ROAD_WAY0316", "ROAD_WAY0317", "ROAD_WAY0221sub", "ROAD_WAY0321", "ROAD_WAY0201", "ROAD_WAY0322",
               "ROAD_WAY0320", "ROAD_WAY0204", "ROAD_WAY0325", "ROAD_WAY0205", "ROAD_WAY0326", "ROAD_WAY0202",
               "ROAD_WAY0323", "ROAD_WAY0203", "ROAD_WAY0324", "ROAD_WAY0208", "ROAD_WAY0329", "ROAD_WAY0209",
               "ROAD_WAY0206", "ROAD_WAY0327", "ROAD_WAY0207", "ROAD_WAY0328", "ROAD_WAY0211", "ROAD_WAY0332",
               "ROAD_WAY0212", "ROAD_WAY0333", "ROAD_WAY0331", "ROAD_WAY0215", "ROAD_WAY0301sub", "ROAD_WAY0216",
               "ROAD_WAY0213", "ROAD_WAY0214", "ROAD_WAY0219", "ROAD_WAY0217", "ROAD_WAY0218", "ROAD_WAY0101",
               "ROAD_WAY0222", "ROAD_WAY0102", "ROAD_WAY0223", "ROAD_WAY0221", "ROAD_WAY0105", "ROAD_WAY0226",
               "ROAD_WAY0106", "ROAD_WAY0227", "ROAD_WAY0103", "ROAD_WAY0224", "ROAD_WAY0104", "ROAD_WAY0225",
               "ROAD_WAY0109", "ROAD_WAY0107", "ROAD_WAY0228", "ROAD_WAY0321sub", "ROAD_WAY0108", "ROAD_WAY0229"))


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
print(len(roadWayList))
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