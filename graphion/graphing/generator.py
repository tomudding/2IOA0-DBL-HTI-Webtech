"""
Author(s): Tom Udding
Created: 2019-05-03
Edited: 2019-05-04
"""
from graphion import server
from graphion.graphing.nodelink.radial import generateRadialGraph

import os

def generateNodeLinkGraph(type, file, directed=None):
    file = getFilePath(file)
    if type.upper() == "RADIAL":
        return generateRadialGraph(file, directed)
    elif type.upper() == "FORCEDIRECTED":
        return generateForceDirectedGraph(file)
    elif type.upper() == "HIERARCHICAL":
        return generateHierarchicalGraph(file)
    else:
        # throw exception, invalid input
        return ""

def generateMatrix(type, file):
    return ""

def getFilePath(file):
    file = file + '.csv'
    return os.path.join(server.config['UPLOAD_FOLDER'], file)