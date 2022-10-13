

import json
import requests

base_url = "http://172.31.236.2:9001"
# get_area = "api/rcs/basic/warehouse/1/area/getAreaByType"
post_area = "/api/rcs/basic/warehouse/1/area/getAreaByCodeList"
find_area = base_url + post_area

form_headers = {
    "Accept": "*/*",
    "Content-Type": "application/json"
}
data = ["ROAD_WAY0322"]

response = requests.post(url=find_area, data=json.dumps(data), headers=form_headers)
print(response.content)
result = json.loads(response.text)['data']
print(result[0]["pointCodeList"])

