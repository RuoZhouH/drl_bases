# -*- coding: utf-8 -*-
import re
import datetime
import time

'''
正则匹配测试
'''


def get_time_stamp(valid_time):
    dd = datetime.datetime.strptime(valid_time, '%Y-%m-%d %H:%M:%S,%f')
    # dd = datetime.datetime.strptime(valid_time, '%H:%M:%S')
    ts = int(time.mktime(dd.timetuple()) * 1000.0 + (dd.microsecond / 1000.0))
    return ts


line = '2022-09-24 15:52:23,466  INFO [traffic-14] .service.PointPushService:91  - datas=>$#{"content":{"actionId":"MoveSub_____c17baa32b04cb58d","agvId":"CARRIER_10012172109","jobId":"SIQPMove_166400588106392597","mes":"CARRIER_10012172109|push points|PushLockPointsAO(agvId=CARRIER_10012172109, lastPushVersion=0, startPos=null, destPos=TeG2eJ, isLastPush=true, canFollow=false, wayPoints=[XWFBic, BPcnBd, TeG2eJ], directionWayPoints={XWFBic=UP, TeG2eJ=RIGHT, BPcnBd=RIGHT}, specialMap={}, topFaces=null, nextPoints=[], turningCodeAndDirection={}, jumpCode=null, remaindNotPushPiontNum=0)","stage":"push","time":"2022-09-24 15:52:23,466"},"generator":"RCS","type":"TRAFFIC","version":"1.0"}#$'

pattern_push_points = '2022\-(.*?)\ INFO.*?PointPushService.*?wayPoints=\[(.*?)\].*'

match_path = re.match(pattern_push_points, line)

if match_path:
    print(match_path.groups())
    print(match_path.group(1))
    print(match_path.group(1).split(',')[0])
    listpoint = match_path.group(2).split(', ')
    print(listpoint[0])

day = "2022-"
ts = get_time_stamp(day + match_path.group(1).split(' ')[0] + ' ' + match_path.group(1).split(' ')[1])
delata_time = get_time_stamp("2022-09-24 15:52:23,466") - get_time_stamp("2022-09-24 15:52:20,466")
print(ts)
print(delata_time)