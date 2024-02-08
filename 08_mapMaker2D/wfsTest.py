"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "BaekInchan"
__version__ = "2024.02.08"

import requests
import json

vworld_key = "C492AE9A-1701-393D-913A-D080B66D18CC"


def terrain(ymin,xmin,ymax,xmax, typeCol, vworld_key) :
    params = {
        "SERVICE": "WFS",
        "REQUEST": "GetFeature",
        "TYPENAME": typeCol,
        "BBOX": "{0},{1},{2},{3}".format(ymin, xmin, ymax, xmax),
      
        "VERSION": "1.1.0",
        "MAXFEATURES": "40",
        "SRSNAME": "EPSG:900913",
        "OUTPUT": "application/json",
        "EXCEPTIONS": "text/xml",
        "KEY": vworld_key
    }

    apiurl = "https://api.vworld.kr/req/wfs"

    # params 딕셔너리를 URL 쿼리 스트링으로 변환
    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    full_url = "{0}?{1}".format(apiurl,query_string)
    response = requests.get(full_url)

    if response.status_code == 200:
        return response.json()
    else : 
        return "value error!"

ymin = 14141391.534656113
xmin = 4475449.690336543
ymax = 14142012.267387545
xmax = 4476127.974275076

print(terrain(ymin,xmin, ymax, xmax,"lt_c_spbd", vworld_key))
