"""
Author(s): Tom Udding
Created: 2019-05-03
Edited: 2019-05-04
"""
from graphion import server
from graphion.graphing.nodelink.radial import generateRadialGraph
from graphion.graphing.matrix.protomatrix import makeMatrix

import os

def generateNodeLinkGraph(type, file, isDirected=None):
    file = getFilePath(file)
    if type.upper() == "RADIAL":
        return generateRadialGraph(file, isDirected)
    elif type.upper() == "FORCEDIRECTED":
        return generateForceDirectedGraph(file)
    elif type.upper() == "HIERARCHICAL":
        return generateHierarchicalGraph(file)
    else:
        # throw exception, invalid input
        return ""

def generateMatrix(file):
    file = getFilePath(file)
    return makeMatrix(file)

def getFilePath(file):
    file = file + '.csv'
    return os.path.join(server.config['UPLOAD_FOLDER'], file)
