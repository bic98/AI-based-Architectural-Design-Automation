"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "BaekInchan"
__version__ = "2024.02.05"

import rhinoscriptsyntax as rs

dict = {}
cnt = 0


for i in listEdges : 
    dict[i] = 1
    
for i in match : 
    if i in dict : cnt += 1
    
print(len(match))
result = float(cnt / len(match)) * 100