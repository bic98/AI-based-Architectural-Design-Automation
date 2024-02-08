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
        "BBOX": "{0:.10f},{1:.10f},{2:.10f},{3:.10f}".format(ymin, xmin, ymax, xmax),
        "VERSION": "2.0.0",
        "MAXFEATURES": "1000",
        "SRSNAME": "EPSG:4326",
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

def AddressToCoord(input_address, vworld_key):
    apiurl = "https://api.vworld.kr/req/address?service=address&request=getcoord&crs=EPSG:4326&address={0}&format=json&type=road&key={1}".format(input_address, vworld_key)
    responseText = requests.get(apiurl)
    response_data = responseText.json()
    x_coord = response_data['response']['result']['point']['x']
    y_coord = response_data['response']['result']['point']['y']
    return float(x_coord), float(y_coord)

input_address1 = "강원 춘천시 동부시장길 8"
input_address2 = "강원 춘천시 삭주로 77"
xmin, ymin = AddressToCoord(input_address1, vworld_key)
xmax, ymax = AddressToCoord(input_address2, vworld_key)


print(terrain(ymin,xmin, ymax, xmax,"lt_c_spbd", vworld_key))