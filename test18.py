# -*- coding: utf-8 -*-
import time

import requests
import datetime

"""
万邑通联网移车下发
"""

if __name__ == "__main__":

    base_url = "http://172.31.236.2:9001"
    # /api/rcs/warehouse/{warehouseId}/lockedZoneQuery/getPointsCongestionLevel
    url = base_url + "/api/rcs/warehouse/1/agv/traffic/dispatchmove"

    ## 巷道间主干道测试1   车对应终点
    agv_codes_destPoints = {"CARRIER_10012172024": "py5cMW",
                            "CARRIER_10012172149": "QwkjPW",
                            "CARRIER_10012172090": "fwW6ZG",
                            "CARRIER_10012172062": "6eCByF"}

    # dest_points2 = ["py5cMW", "QwkjPW", "fwW6ZG", "6eCByF"]

    ## 巷道间的主干道测试2  车对应终点
    agv_codes_destPointInverse = {"CARRIER_10012172062": "ZhGQnA",
                                  "CARRIER_10012172090": "cA5FFh",
                                  "CARRIER_10012172149": "EhxwGi",
                                  "CARRIER_10012172024": "xnwTY4"}

    # dest_points = ["ZhGQnA", "cA5FFh", "cA5FFh", "xnwTY4"]

    # 工作站的主干道测试
    agv_codes_destPointStation1 = {"CARRIER_10012172062": "MCyCm8",
                                  "CARRIER_10012172090": "yTHaam",
                                  "CARRIER_10012172149": "XXP4ZB",
                                  "CARRIER_10012172024": "HP8Eai",
                                   "CARRIER_10012172087": "FGyf2X",
                                   "CARRIER_10012172060": "7b85fn",
                                   "CARRIER_10012172147": "ApWsJe",
                                   "CARRIER_10012172052": "yQypwb",
                                   "CARRIER_10012172033": "xeGQcY",
                                   "CARRIER_10012172082": "kRWyac",
                                   "CARRIER_10012172035": "xTM7aD",
                                   "CARRIER_10012172139": "TFKB8K"
                                   }

    agv_codes_destPointStation1bak = {"CARRIER_10012172062": "3sRcDm",
                                   "CARRIER_10012172090": "d6MFJC",
                                   "CARRIER_10012172149": "xeBWF4",
                                   "CARRIER_10012172024": "kF6NRr",
                                   "CARRIER_10012172087": "4zWDPG",
                                   "CARRIER_10012172060": "irQjAp",
                                   "CARRIER_10012172147": "wRFY5G",
                                   "CARRIER_10012172052": "myye6x",
                                   "CARRIER_10012172033": "Zbck6j",
                                   "CARRIER_10012172082": "XM4Sys",
                                   "CARRIER_10012172035": "3i4Da2",
                                   "CARRIER_10012172139": "zdCjyH"
                                   }

    agv_codes_destPointStation11 = {"CARRIER_10012172062": "Qiicdx",
                                   "CARRIER_10012172090": "ZAz2TB",
                                   "CARRIER_10012172149": "pmrwb8",
                                   "CARRIER_10012172024": "RJPTHJ",
                                   "CARRIER_10012172087": "kNr3ke",
                                   "CARRIER_10012172060": "GyXErc",
                                   "CARRIER_10012172147": "sAQ4QP",
                                   "CARRIER_10012172052": "mQmJHN",
                                   "CARRIER_10012172033": "ZhGQnA",
                                   "CARRIER_10012172082": "WW8PJA",
                                   "CARRIER_10012172035": "nrAAaK",
                                   "CARRIER_10012172139": "62Kan8"
                                   }

    agv_codes_destPointStation11bak= {"CARRIER_10012172062": "JWZPS3",
                                    "CARRIER_10012172090": "pFQwDQ",
                                    "CARRIER_10012172149": "EsW6P2",
                                    "CARRIER_10012172024": "GGBWJh",
                                    "CARRIER_10012172087": "J8SnjF",
                                    "CARRIER_10012172060": "bfckyS",
                                    "CARRIER_10012172147": "DxsaDd",
                                    "CARRIER_10012172052": "hzw3pH",
                                    "CARRIER_10012172033": "QmnPrR",
                                    "CARRIER_10012172082": "BstwnA",
                                    "CARRIER_10012172035": "GMa6eE",
                                    "CARRIER_10012172139": "dMWJwj"
                                    }

    agv_codes_destPointStation11bakremote = {"CARRIER_10012172062": "EK6ARS",
                                       "CARRIER_10012172090": "EK6ARS",
                                       "CARRIER_10012172149": "EK6ARS",
                                       "CARRIER_10012172024": "EK6ARS",
                                       "CARRIER_10012172087": "EK6ARS",
                                       "CARRIER_10012172060": "EK6ARS",
                                       "CARRIER_10012172147": "EK6ARS",
                                       "CARRIER_10012172052": "EK6ARS",
                                       "CARRIER_10012172033": "EK6ARS",
                                       "CARRIER_10012172082": "EK6ARS",
                                       "CARRIER_10012172035": "EK6ARS",
                                       "CARRIER_10012172139": "EK6ARS"
                                       }

    ## 工作站点
    agv_codes_destPointStation2 = {"CARRIER_10012172056": "JWZPS3",
                                   "CARRIER_10012172114": "pFQwDQ",
                                   "CARRIER_10012172072": "EsW6P2",
                                   "CARRIER_10012172136": "GGBWJh",
                                   "CARRIER_10012172115": "J8SnjF",
                                   "CARRIER_10012172109": "bfckyS",
                                   "CARRIER_10012172048": "DxsaDd",
                                   "CARRIER_10012172103": "hzw3pH",
                                   "CARRIER_10012172070": "QmnPrR",
                                   "CARRIER_10012172108": "BstwnA",
                                   # "CARRIER_10012172042": "GMa6eE",
                                   "CARRIER_10012172113": "dMWJwj"
                                   }



    ## 工作站点
    agv_codes_destPointStation21 = {"CARRIER_10012172056": "3sRcDm",
                                   "CARRIER_10012172114": "d6MFJC",
                                   "CARRIER_10012172072": "xeBWF4",
                                   "CARRIER_10012172136": "kF6NRr",
                                   "CARRIER_10012172115": "4zWDPG",
                                   "CARRIER_10012172109": "irQjAp",
                                   "CARRIER_10012172048": "wRFY5G",
                                   "CARRIER_10012172103": "myye6x",
                                   "CARRIER_10012172070": "Zbck6j",
                                   "CARRIER_10012172108": "XM4Sys",
                                   # "CARRIER_10012172042": "3i4Da2",
                                   "CARRIER_10012172113": "zdCjyH"
                                   }

    ## 工作站点
    agv_codes_destPointStation22 = {"CARRIER_10012172056": "rcGh4A",
                                   "CARRIER_10012172114": "rcGh4A",
                                   "CARRIER_10012172072": "rcGh4A",
                                   "CARRIER_10012172136": "rcGh4A",
                                   "CARRIER_10012172115": "rcGh4A",
                                   "CARRIER_10012172109": "rcGh4A",
                                   "CARRIER_10012172048": "rcGh4A",
                                   "CARRIER_10012172103": "rcGh4A",
                                   "CARRIER_10012172070": "rcGh4A",
                                   "CARRIER_10012172108": "rcGh4A",
                                   # "CARRIER_10012172042": "GMa6eE",
                                   "CARRIER_10012172113": "rcGh4A"
                                   }

    ## 工作站点
    agv_codes_destPointStation3 = {"CARRIER_10012172056": "JCpA3A",
                                    "CARRIER_10012172114": "SiME56",
                                    "CARRIER_10012172072": "xeBWF4",
                                    "CARRIER_10012172136": "4ppPzj",
                                    "CARRIER_10012172115": "RSJZfH"
                                    # "CARRIER_10012172109": "irQjAp",
                                    # "CARRIER_10012172048": "wRFY5G",
                                    # "CARRIER_10012172103": "myye6x",
                                    # "CARRIER_10012172070": "Zbck6j",
                                    # "CARRIER_10012172108": "XM4Sys",
                                    # # "CARRIER_10012172042": "3i4Da2",
                                    # "CARRIER_10012172113": "zdCjyH"
                                    }


    # 5CsYzN 终点


    form_headers = {
        "Accept": "*/*"
    }

    # for key, value in agv_codes_destPointStation11bakremote.items():
    #     json = {"agvCodes": [key], "points": [value]}
    #     response = requests.post(url=url, json=json)
    #     # time.sleep(1)
    #     print(response.content)
    timenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for key, value in agv_codes_destPointStation2.items():
        json = {"agvCodes": [key], "points": [value]}
        response = requests.post(url=url, json=json)
        time.sleep(1.5)
        print(response.content)
        print(timenow)
