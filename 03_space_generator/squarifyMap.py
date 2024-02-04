"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "BaekInchan"
__version__ = "2024.02.05"

import Rhino.Geometry as rg
import random


class Squarifier:
    def __init__(self, room_names, widths, areas, origin, relations, seed=None) :
        self.areas = areas
        self.room_names = room_names
        self.widths = widths
        self.origin = origin
        self.relations = relations
        self.rooms = {}
        self.sizes = []
        self._relations = []
        self.result = []
        self.sequence = list(range(len(areas)))
        if seed is not None: random.seed(seed)
        random.shuffle(self.sequence)

    def initialize(self) : 
        for id, i in enumerate(self.sequence, 0) : 
            cur_room = room(self.room_names[i], self.areas[i], id)
            self.sizes.append(self.areas[i])
            self.rooms[self.room_names[i]] = cur_room
        self.relation_initialize()
        pt_plane = rg.Plane(self.origin, rg.Vector3d.ZAxis)
        rectangle = rg.Rectangle3d(pt_plane, self.widths, sum(self.areas) / self.widths)
        sizes_normalized = self.normalize_sizes(self.sizes, rectangle.X.Length, rectangle.Y.Length)
        squarified = self.squarify(sizes_normalized, rectangle.X.Min, rectangle.Y.Min, rectangle.X.Length, rectangle.Y.Length)
        for square in squarified:
            origin = rg.Point3d(self.origin.X + square['x'], self.origin.Y + square['y'], 0)
            rectangle_plane = rg.Plane(origin, rg.Vector3d(1,0,0), rg.Vector3d(0,1,0))
            rectangle = rg.Rectangle3d(rectangle_plane, square['dx'], square['dy'])
            self.result.append(rectangle)
    
    def relation_initialize(self) : 
        for i in self.relations : 
            a, b = i.split("-")
            a_edges = self.rooms[a].id
            b_edges = self.rooms[b].id
            if(a_edges > b_edges) : 
                a_edges, b_edges = b_edges, a_edges
            s = '{0} - {1}'.format(a_edges, b_edges)
            print(self.room_names[self.sequence[a_edges]], self.room_names[self.sequence[b_edges]])
            self._relations.append(s)
            
    @staticmethod
    def normalize_sizes(sizes, dx, dy):
        total_size = sum(sizes)
        total_area = dx * dy
        sizes = map(float, sizes)
        sizes = map(lambda size: size * total_area / total_size, sizes)
        return list(sizes)

    @staticmethod
    def layoutrow(sizes, x, y, dx, dy):
        covered_area = sum(sizes)
        width = covered_area / dy
        rects = []
        for size in sizes:
            rects.append({'x': x, 'y': y, 'dx': width, 'dy': size / width})
            y += size / width
        return rects

    @staticmethod
    def layoutcol(sizes, x, y, dx, dy):
        covered_area = sum(sizes)
        height = covered_area / dx
        rects = []
        for size in sizes:
            rects.append({'x': x, 'y': y, 'dx': size / height, 'dy': height})
            x += size / height
        return rects

    @staticmethod
    def layout(sizes, x, y, dx, dy):
        return Squarifier.layoutrow(sizes, x, y, dx, dy) if dx >= dy else Squarifier.layoutcol(sizes, x, y, dx, dy)

    @staticmethod
    def leftover(sizes, x, y, dx, dy):
        if dx >= dy:
            covered_area = sum(sizes)
            width = covered_area / dy
            return (x + width, y, dx - width, dy)
        else:
            covered_area = sum(sizes)
            height = covered_area / dx
            return (x, y + height, dx, dy - height)

    @staticmethod
    def worst_ratio(sizes, x, y, dx, dy):
        return max([max(rect['dx'] / rect['dy'], rect['dy'] / rect['dx']) for rect in Squarifier.layout(sizes, x, y, dx, dy)])

    def squarify(self, sizes, x, y, dx, dy):
        sizes = list(map(float, sizes))
        if len(sizes) == 0:
            return []
        if len(sizes) == 1:
            return self.layout(sizes, x, y, dx, dy)
        i = 1
        while i < len(sizes) and self.worst_ratio(sizes[:i], x, y, dx, dy) >= self.worst_ratio(sizes[:(i+1)], x, y, dx, dy):
            i += 1
        current = sizes[:i]
        remaining = sizes[i:]
        leftover_x, leftover_y, leftover_dx, leftover_dy = self.leftover(current, x, y, dx, dy)
        return self.layout(current, x, y, dx, dy) + self.squarify(remaining, leftover_x, leftover_y, leftover_dx, leftover_dy)

floor = Squarifier(room_names, widths, areas, origin, relations, seed)
floor.initialize()
space = floor.result
match = floor._relations
id = floor.sequence
room_name = []
space_areas = []
for i in floor.sequence : 
    room_name.append(floor.room_names[i])
    space_areas.append(floor.rooms[floor.room_names[i]].area)

