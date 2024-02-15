"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "BaekInchan"
__version__ = "2024.02.08"

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import random
import clr
clr.AddReference('System.Web.Extensions')
from System.Web.Script.Serialization import JavaScriptSerializer


bldPolylines = {}
buildingHeight = {}
strPolylines = {}
waterPolylines = {}
cadastralMap = {}
greenPolylines = {}
detailstr = {}

bucket = [bldPolylines, strPolylines, waterPolylines, cadastralMap, greenPolylines, detailstr]

for i in info : 
    for id, result in enumerate(i) : 
        if result is not None:
            dataDict = JavaScriptSerializer().DeserializeObject(result)
            features = dataDict["features"]
            for feature in features:
                coords = feature["geometry"]["coordinates"]
                points = []
                for coord in coords[0][0]:
                    try:
                        x, y = gps.LLtoUTM(coord[1], coord[0])
                        pt = rg.Point3d(x, y, 0)
                        points.append(pt)
                    except: continue
                if(len(points) == 0) : continue
                try : 
                    polyline = rs.AddPolyline(points)
                    bucket[id][polyline] = 1
                    if id == 0 : 
                        height = feature["properties"]["gro_flo_co"]
                        if(height == 0) : 
                            height = random.randint(1, 3)
                        buildingHeight[polyline] = height * 3
                except : pass


building = bucket[0].keys()
building_height = buildingHeight.values()
street = bucket[1].keys()
water = bucket[2].keys()
cadastral = bucket[3].keys()
green = bucket[4].keys()
detail_street = bucket[5].keys()
