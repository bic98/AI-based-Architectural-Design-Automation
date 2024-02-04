"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "BaekInchan"
__version__ = "2024.02.05"

class Room:
    def __init__ (self, room_name, area, id):
        self.room_name = room_name
        self.area = area
        self.id = id

room = Room