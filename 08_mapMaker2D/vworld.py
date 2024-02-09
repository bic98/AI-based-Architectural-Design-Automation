vworld_key = "valid - key"

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
