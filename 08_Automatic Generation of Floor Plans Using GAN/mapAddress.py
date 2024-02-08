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
vworld_key = "C492AE9A-1701-393D-913A-D080B66D18CC"

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

info = []
if Run : 
    xmin, ymin = AddressToCoord(input_address1, vworld_key)
    xmax, ymax = AddressToCoord(input_address2, vworld_key)
    if(ymin > ymax) : ymin, ymax = ymax, ymin
    if(xmin > xmax) : xmin, xmax = xmax, xmin
    print(xmin, xmax)
    typeM = ["lt_c_upisuq151", "lt_c_spbd"]
    for s in typeM : 
        result = JavaScriptSerializer().Serialize(terrain(ymin,xmin,ymax,xmax, s, vworld_key))
        print(result)
        info.append(result)
    print(info[0])
    info



