vworld_key = "C492AE9A-1701-393D-913A-D080B66D18CC"

import folium
import requests
import json

def get_adress(input_address, vworld_key) : 
    apiurl = "https://api.vworld.kr/req/address?"
    params = {
        "service": "address",
        "request": "getcoord",
        "crs": "epsg:4326",
        "address": f'{input_address}',
        "format": "json",
        "type": "road",
        "key": vworld_key
    }
    response = requests.get(apiurl, params=params)
    if response.status_code == 200:
        return response.json()
    else : 
        return "value error!"

print(get_adress("경기도 수원시 팔달구 효원로308번길 16 (인계동, 한화 꿈에그린 파크)", vworld_key))