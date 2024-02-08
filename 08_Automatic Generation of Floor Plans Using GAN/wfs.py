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

# 주어진 params 딕셔너리를 URL 쿼리 스트링으로 변환하는 예시 코드입니다.
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
        "PROPERTYNAME": "mnum,sido_cd,sigungu_cd,dyear,dnum,ucode,bon_bun,bu_bun,uname,sido_name,sigg_name,ag_geom",
        "VERSION": "1.1.0",
        "MAXFEATURES": "40",
        "SRSNAME": "EPSG:900913",
        "OUTPUT": "GML2",
        "EXCEPTIONS": "text/xml",
        "KEY": vworld_key
    }

    apiurl = "https://api.vworld.kr/req/wfs"

    # params 딕셔너리를 URL 쿼리 스트링으로 변환
    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    full_url = "{0}?{1}".format(apiurl,query_string)
    data = read(full_url)
    return data


print(terrain(13987670,3912271,14359383,4642932,"lt_c_uq111", vworld_key))
