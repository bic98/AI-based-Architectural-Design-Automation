"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "BaekInchan"
__version__ = "2024.02.08"

import rhinoscriptsyntax as rs
from System.Net import HttpWebRequest, WebRequest
from System.IO import StreamReader
import json
import clr
clr.AddReference('System.Web.Extensions')
from System.Web.Script.Serialization import JavaScriptSerializer
vworld_key = "valid - key"

def read(apiurl) : 
    request = WebRequest.Create(apiurl)
    request.Method = "GET"
    response = request.GetResponse()
    stream = response.GetResponseStream()
    reader = StreamReader(stream)
    responseText = reader.ReadToEnd()
    return json.loads(responseText)

def terrain(ymin,xmin,ymax,xmax, typeCol, vworld_key) :
    params = {
        "SERVICE": "WFS",
        "REQUEST": "GetFeature",
        "TYPENAME": typeCol,
        "BBOX": "{0},{1},{2},{3}".format(ymin, xmin, ymax, xmax),
        "VERSION": "2.0.0",
        "MAXFEATURES": "1000",
        "SRSNAME": "EPSG:4326",
        "OUTPUT": "application/json",
        "EXCEPTIONS": "text/xml",
        "KEY": vworld_key
    }

    apiurl = "https://api.vworld.kr/req/wfs"

    # params 딕셔너리를 URL 쿼리 스트링으로 변환
    query_string = "&".join(["{0}={1}".format(key, value) for key, value in params.items()])
    full_url = "{0}?{1}".format(apiurl,query_string)
    data = read(full_url)
    return data


def AddressToCoord(input_address, vworld_key):
    apiurl = "https://api.vworld.kr/req/address?service=address&request=getcoord&crs=EPSG:4326&address={0}&format=json&type=road&key={1}".format(input_address, vworld_key)
    request = WebRequest.Create(apiurl)
    request.Method = "GET"
    response = request.GetResponse()
    stream = response.GetResponseStream()
    reader = StreamReader(stream)
    responseText = reader.ReadToEnd()
    response_data = json.loads(responseText)
    x_coord = response_data['response']['result']['point']['x']
    y_coord = response_data['response']['result']['point']['y']
    return float(x_coord), float(y_coord)

def divideMap(t, ymin, xmin, ymax, xmax) : 
    rectangles = []
    current_x = xmin
    while current_x < xmax:
        next_x = min(current_x + t, xmax)
        current_y = ymin
        while current_y < ymax:
            next_y = min(current_y + t, ymax)
            rectangles.append((current_y, current_x, next_y, next_x))
            current_y += t
        current_x += t
    return rectangles
    
    
info = []

if Run : 
    xmin, ymin = AddressToCoord(input_address1, vworld_key)
    xmax, ymax = AddressToCoord(input_address2, vworld_key)
    if(ymin > ymax) : ymin, ymax = ymax, ymin
    if(xmin > xmax) : xmin, xmax = xmax, xmin
    dm = divideMap(0.005, ymin,xmin, ymax, xmax)
    print(len(dm))
    if(len(dm) <= 80) : 
        for i in dm : 
            typeM = ["lt_c_spbd", "lt_c_upisuq151", "lt_c_wkmstrm", "lp_pa_cbnd_bubun", "lt_c_uq162", "lt_c_upisuq152"]
            obj = []
            for s in typeM : 
                result = JavaScriptSerializer().Serialize(terrain(i[0],i[1],i[2],i[3], s, vworld_key))
                obj.append(result)
            info.append(obj)


info



