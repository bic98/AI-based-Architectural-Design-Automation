import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import ghpythonlib.componentbase
import random
import math
import time

random.seed(seed)

class Floorplan:
    def __init__ (self, room_names, widths, depths, origin):
        self.room_names = room_names
        self.widths = widths
        self.depths = depths
        self.origin = origin
        self.rooms = []
        self.areas = []
    
    def initialize(self):
        self.initialize_rooms()
        
    def initialize_rooms(self):
        initial_room_names = self.room_names
        initial_widths = self.widths
        initial_depths = self.depths
        self.network, initial_locations = self.distribution_network()
        for i in range(len(initial_room_names)):
            cur_room = room(initial_room_names[i], initial_depths[i], initial_widths[i], initial_locations[i])
            self.rooms.append(cur_room)

    
    def distribution_network(self):
        cnt = self.origin
        print(cnt)
        nums = len(self.room_names)
        lines = []
        locations = []
        rotation = 2 * math.pi / nums;
        for num in range(nums):
            r = nums * 15
            pt = rg.Point3d(cnt.X + random.uniform(r/2, r) * math.cos(rotation*num), cnt.Y + random.uniform(r/2, r) * math.sin(rotation*num),0)
            pt_plane = rg.Plane(pt, rg.Vector3d.ZAxis)
            pt_plane.Rotate(0, rg.Vector3d.ZAxis, pt_plane.Origin)
            locations.append(pt_plane)
            line = rg.Line(cnt, pt)
            lines.append(line)
        return lines, locations
        



floor = Floorplan(rooms, widths, depths,origin)
floor.initialize()
initial_rooms = []
rooms_3d = []
rooms_areas = []
floor_network = floor.network

for room in floor.rooms:
    room_3d,room_2d = room.visual_3d()
    initial_rooms.append(room_2d)
    rooms_3d.append(room_3d)
    rooms_areas.append(room.area())


