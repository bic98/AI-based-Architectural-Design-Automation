import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import ghpythonlib.componentbase
import math
import time
import System.Drawing as sd
import random
import json
from Rhino.Geometry import *
import rhinoscriptsyntax as rs
import scriptcontext as sc

# START Squarify code by Uri Laserson
def normalize_sizes(sizes, dx, dy):
    total_size = sum(sizes)
    total_area = dx * dy
    sizes = map(float, sizes)
    sizes = map(lambda size: size * total_area / total_size, sizes)
    return list(sizes)

def pad_rectangle(rect):
    if rect['dx'] > 2:
        rect['x'] += 1
        rect['dx'] -= 2
    if rect['dy'] > 2:
        rect['y'] += 1
        rect['dy'] -= 2

def layoutrow(sizes, x, y, dx, dy):
    # generate rects for each size in sizes
    # dx >= dy
    # they will fill up height dy, and width will be determined by their area
    # sizes should be pre-normalized wrt dx * dy (i.e., they should be same units)
    covered_area = sum(sizes)
    width = covered_area / dy
    rects = []
    for size in sizes:
        rects.append({'x': x, 'y': y, 'dx': width, 'dy': size / width})
        y += size / width
    return rects

def layoutcol(sizes, x, y, dx, dy):
    # generate rects for each size in sizes
    # dx < dy
    # they will fill up width dx, and height will be determined by their area
    # sizes should be pre-normalized wrt dx * dy (i.e., they should be same units)
    covered_area = sum(sizes)
    height = covered_area / dx
    rects = []
    for size in sizes:
        rects.append({'x': x, 'y': y, 'dx': size / height, 'dy': height})
        x += size / height
    return rects

def layout(sizes, x, y, dx, dy):
    return layoutrow(sizes, x, y, dx, dy) if dx >= dy else layoutcol(sizes, x, y, dx, dy)

def leftoverrow(sizes, x, y, dx, dy):
    # compute remaining area when dx >= dy
    covered_area = sum(sizes)
    width = covered_area / dy
    leftover_x = x + width
    leftover_y = y
    leftover_dx = dx - width
    leftover_dy = dy
    return (leftover_x, leftover_y, leftover_dx, leftover_dy)

def leftovercol(sizes, x, y, dx, dy):
    # compute remaining area when dx >= dy
    covered_area = sum(sizes)
    height = covered_area / dx
    leftover_x = x
    leftover_y = y + height
    leftover_dx = dx
    leftover_dy = dy - height
    return (leftover_x, leftover_y, leftover_dx, leftover_dy)

def leftover(sizes, x, y, dx, dy):
    return leftoverrow(sizes, x, y, dx, dy) if dx >= dy else leftovercol(sizes, x, y, dx, dy)

def worst_ratio(sizes, x, y, dx, dy):
    return max([max(rect['dx'] / rect['dy'], rect['dy'] / rect['dx']) for rect in layout(sizes, x, y, dx, dy)])

def squarify(sizes, x, y, dx, dy):
    # sizes should be pre-normalized wrt dx * dy (i.e., they should be same units)
    # or dx * dy == sum(sizes)
    # sizes should be sorted biggest to smallest
    sizes = list(map(float, sizes))
    
    if len(sizes) == 0:
        return []
    
    if len(sizes) == 1:
        return layout(sizes, x, y, dx, dy)
    
    # figure out where 'split' should be
    i = 1
    while i < len(sizes) and worst_ratio(sizes[:i], x, y, dx, dy) >= worst_ratio(sizes[:(i+1)], x, y, dx, dy):
        i += 1
    current = sizes[:i]
    remaining = sizes[i:]
    
    (leftover_x, leftover_y, leftover_dx, leftover_dy) = leftover(current, x, y, dx, dy)
    return layout(current, x, y, dx, dy) + \
            squarify(remaining, leftover_x, leftover_y, leftover_dx, leftover_dy)
# END Squarify code by Uri Laserson

R = rg.Rectangle3d(location, width, sum(V) / width)

if not R:
    raise ValueError("Input R failed to collect data")

if type(R) == Rectangle3d:
    rectangles = []
    
    sizes_normalized = normalize_sizes(V, R.X.Length, R.Y.Length)
    #print normalized
    
    squarified = squarify(sizes_normalized, R.X.Min, R.Y.Min, R.X.Length, R.Y.Length)
    #print squarified
    
    for square in squarified:
#        print square['x']
        origin = Point3d(square['x'], square['y'], 0)
        rectangle_plane = Plane(origin, Vector3d(1,0,0), Vector3d(0,1,0))
        rectangle = Rectangle3d(rectangle_plane, square['dx'], square['dy'])
        rectangles.append(rectangle)
    
    transform = Transform.ChangeBasis(R.Plane, Plane(Point3d(0,0,0), Vector3d(1,0,0), Vector3d(0,1,0)))
    [a.Transform(transform) for a in rectangles]
    
    R = rectangles
    
else:
    raise TypeError("Input R must be a rectangle")