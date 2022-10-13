# -*- coding: utf-8 -*-


import requests

"""
万邑通联网移车下发
"""

if __name__ == "__main__":

    base_url = "http://172.31.236.2:9001"
    # /api/rcs/warehouse/{warehouseId}/lockedZoneQuery/getPointsCongestionLevel
    url = base_url + "/api/rcs/warehouse/1/agv/traffic/dispatchmove"

    agv_codes_destPoints = {"CARRIER_10012172024": "py5cMW", "CARRIER_10012172149": "QwkjPW",
                            "CARRIER_10012172090": "fwW6ZG", "CARRIER_10012172062": "6eCByF"}
    dest_points2 = ["py5cMW", "QwkjPW", "fwW6ZG", "6eCByF"]

    agv_codes_destPointInverse = {"CARRIER_10012172062": "WKkYJM", "CARRIER_10012172090": "FBjefs",
                                  "CARRIER_10012172149": "WEh8bw", "CARRIER_10012172024": "bQ6es2"}
    dest_points = ["bQ6es2", "WEh8bw", "FBjefs", "WKkYJM"]

    form_headers = {
        "Accept": "*/*"
    }

    for key, value in agv_codes_destPoints.items():
        json = {"agvCodes": [key], "points": [value]}
        response = requests.post(url=url, json=json)
        print(response.content)
