"""
Author(s): Tom Udding, Steven van den Broek
Created: 2019-05-03
Edited: 2019-05-22
"""
from graphion import server
from graphion.graphing.nodelink.graph import generateForceDirectedDiagram, generateHierarchicalDiagram, generateRadialDiagram, generate3DDiagram
from graphion.graphing.matrix.protomatrix import makeMatrix

import os
import panel as pn

def generateBokehApp(doc):
    path = getFilePath(str(doc.session_context.request.arguments['file'][0].decode('utf-8')))
    # Put parameters in panel with param to change direction and type of graph.
    pn.extension('plotly')
    pane = pn.Row(generateForceDirectedDiagram(path, False), makeMatrix(path))
    return pane.get_root(doc)

def getFilePath(file):
    file = file + '.h5'
    return os.path.join(server.config['UPLOAD_FOLDER'], file)
