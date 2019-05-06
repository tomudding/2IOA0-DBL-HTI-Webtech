"""
Author(s): Tom Udding
Created: 2019-05-03
Edited: 2019-05-04
"""
from graphion import server
from graphion.graphing.nodelink.graph import generateGraph
from graphion.graphing.matrix.protomatrix import makeMatrix

import os
import panel as pn

def generateBokehApp(file):
    path = getFilePath(file)
    # Put parameters in panel with param to change direction and type of graph.
    pane = pn.Row(makeMatrix(path), generateGraph(path))
    return pane.get_root()

def getFilePath(file):
    file = file + '.csv'
    return os.path.join(server.config['UPLOAD_FOLDER'], file)
