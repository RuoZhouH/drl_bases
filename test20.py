# -*- coding: utf-8 -*-
import re

line = '2022-09-24 15:52:23,466  INFO [traffic-14] .service.PointPushService:91  - datas=>$#{"content":{"actionId":"MoveSub_____c17baa32b04cb58d","agvId":"CARRIER_10012172109","jobId":"SIQPMove_166400588106392597","mes":"CARRIER_10012172109|push points|PushLockPointsAO(agvId=CARRIER_10012172109, lastPushVersion=0, startPos=null, destPos=TeG2eJ, isLastPush=true, canFollow=false, wayPoints=[XWFBic, BPcnBd, TeG2eJ], directionWayPoints={XWFBic=UP, TeG2eJ=RIGHT, BPcnBd=RIGHT}, specialMap={}, topFaces=null, nextPoints=[], turningCodeAndDirection={}, jumpCode=null, remaindNotPushPiontNum=0)","stage":"push","time":"2022-09-24 15:52:23,466"},"generator":"RCS","type":"TRAFFIC","version":"1.0"}#$'

pattern_push_points = '2022.*?PointPushService.*?wayPoints=\[(.*?)\].*'

match_path = re.match(pattern_push_points, line)

if match_path:
    print(match_path.groups())
    print(match_path.group(1))
    listpoint = match_path.group(1).split(', ')
    print(listpoint[0])