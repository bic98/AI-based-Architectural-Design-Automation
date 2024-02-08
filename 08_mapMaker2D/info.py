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
import clr
clr.AddReference('System.Web.Extensions')
from System.Web.Script.Serialization import JavaScriptSerializer


bldPolylines = []
strPolylines = []

bucket = [bldPolylines, strPolylines]

for id, result in enumerate(info) : 
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
            except : pass
            bucket[id].append(polyline)

building = bucket[0]
street = bucket[1]