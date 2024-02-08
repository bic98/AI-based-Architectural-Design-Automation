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

def AddressToCoord(input_address, vworld_key):
    apiurl = "https://api.vworld.kr/req/address?service=address&request=getcoord&crs=epsg:4326&address={0}&format=json&type=road&key={1}".format(input_address, vworld_key)
    request = WebRequest.Create(apiurl)
    request.Method = "GET"
    response = request.GetResponse()
    stream = response.GetResponseStream()
    reader = StreamReader(stream)
    responseText = reader.ReadToEnd()
    response_data = json.loads(responseText)
    x_coord = response_data['response']['result']['point']['x']
    y_coord = response_data['response']['result']['point']['y']
    return x_coord, y_coord

if Run : 
    x_coord, y_coord = AddressToCoord(input_address, vworld_key)