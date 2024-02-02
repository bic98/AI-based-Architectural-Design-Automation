import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import ghpythonlib.componentbase
import math
import time
import System.Drawing as sd
import random
import json



class Room:
    def __init__ (self, room_name, depth, width, location):
        self.room_name = room_name
        self.depth = depth
        self.width = width
        self.location = location

    def area(self):
        return self.depth * self.width
    
    def visual_3d(self):
        crv = rg.Rectangle3d(self.location,rg.Interval(-self.width/2, self.width/2), rg.Interval(-self.depth/2, self.depth/2))
        crv = crv.ToNurbsCurve()
        height = 12
        result = rg.Extrusion.Create(crv, height, True)
        return result, crv
       

room = Room
