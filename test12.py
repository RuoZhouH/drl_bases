

import re

strLine = "2022-05-10 13:31:29,882  INFO [CongestionDetect thread] pl.CongestionTargetInArea:36  - roadWay density:{ROAD_WAY174=0.0, ROAD_WAY461=0.46875, ROAD_WAY925=0.15625, ROAD_WAY838=0.0, ROAD_WAY307=0.3125, ROAD_WAY019=0.5208333333333334, ROAD_WAY920=0.3125, ROAD_WAY612=0.15625, ROAD_WAY148=0.0, ROAD_WAY588=0.0, ROAD_WAY101=0.625, ROAD_WAY663=0.0}|roadWay Speed:{ROAD_WAY174=0.0, ROAD_WAY461=0.24390243902439024, ROAD_WAY925=2.36, ROAD_WAY838=0.0, ROAD_WAY307=0.0, ROAD_WAY019=0.4099591836734694, ROAD_WAY920=0.3285714285714285, ROAD_WAY612=2.2172949002217295, ROAD_WAY148=0.0, ROAD_WAY588=0.0, ROAD_WAY101=0.4601587301587301, ROAD_WAY663=0.0}|density variance:0.04858323085455247|speed variance:0.6677781007399153"

str = "<span><h1>hello world!</h1></span>"
# pattern = "<(?P<key1>.+)><(?P<key2>.+)>(?P<nr>.*)</(?P=key2)></(?P=key1)>"

str2 = "pl.CongestionTargetInArea:36 - roadWay density:{ROAD_WAY174=0.0, ROAD_WAY461=0.46875, ROAD_WAY925=0.15625,ROAD_WAY838=0.0, ROAD_WAY307=0.3125, ROAD_WAY019=0.5208333333333334, ROAD_WAY920=0.3125, ROAD_WAY612=0.15625, ROAD_WAY148=0.0, ROAD_WAY588=0.0, ROAD_WAY101=0.625, ROAD_WAY663=0.0}|roadWay Speed:{ROAD_WAY174=0.0, ROAD_WAY461=0.24390243902439024, ROAD_WAY925=2.36, ROAD_WAY838=0.0, ROAD_WAY307=0.0, ROAD_WAY019=0.4099591836734694, ROAD_WAY920=0.3285714285714285, ROAD_WAY612=2.2172949002217295, ROAD_WAY148=0.0, ROAD_WAY588=0.0, ROAD_WAY101=0.4601587301587301, ROAD_WAY663=0.0}"
strList = str2.split("|")

roadWayList = ["ROAD_WAY174", "ROAD_WAY461", "ROAD_WAY925", "ROAD_WAY838", "ROAD_WAY307", "ROAD_WAY019", "ROAD_WAY920", "ROAD_WAY612", "ROAD_WAY148", "ROAD_WAY588", "ROAD_WAY101", "ROAD_WAY663"]

str21 = strList[0]
str22 = strList[1]

pattern2 = ".*ROAD_WAY174=(.+),|}.*"

# pattern2 = "density:.*" + "ROAD_WAY174" + "=(.+).*?"

# result2 = re.match(pattern2, str21)
# res2 = result2.groups()
#
# print((res2[0].split(",")[0]))

# pattern = "density:.*?" + roadWay + "=(.*?),.*?Speed:.*?" + roadWay + "=(.*?),"

for roadWay in roadWayList:

    # pattern = ".*-\s(.+):{(.+)=(.+),\s(.+)=(.+),\s(.+)=(.+)}|"
    pattern = ".*" + roadWay + "=(.+),.*?"
    density = re.match(pattern, str21)
    speed = re.match(pattern, str22)
    if density is not None:
        resDen = density.groups()
        resSpe = speed.groups()
        print(roadWay+": density:" + resDen[0].split(",")[0][:5] + "  speed: "+ resSpe[0].split(",")[0][:5])


