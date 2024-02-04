"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "BaekInchan"
__version__ = "2024.02.04"

import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as th

listEdges = []
treeEdges = []
dict = {}

    
for i in range(C.BranchCount):
    branchList = C.Branch(i)
    tmp= []
    for j in range(branchList.Count):
        if branchList[j] == True : 
            if i == j : continue
            edge1 = '{0} - {1}'.format(i, j)
            edge2 = '{0} - {1}'.format(j, i)
            if(edge1 not in dict and edge2 not in dict) : 
                listEdges.append(edge1)
                tmp.append(j)
                dict[edge1] = 1
                dict[edge2] = 1
    treeEdges.append(tmp)

treeEdges = th.list_to_tree(treeEdges, none_and_holes = True)