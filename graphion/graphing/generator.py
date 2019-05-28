"""
Author(s): Tom Udding, Steven van den Broek
Created: 2019-05-03
Edited: 2019-05-22
"""
from graphion import server
from graphion.graphing.nodelink.graph import generateForceDirectedDiagram, generateHierarchicalDiagram, generateRadialDiagram, generate3DDiagram
from graphion.graphing.matrix.protomatrix import makeMatrix
from graphion.api.filter.distribution import get_filtered_df
import os
import panel as pn
import time
import pandas

def generateBokehApp(doc):
    try:
        path = doc.session_context.request.arguments['file'][0]
        path = getFilePath(str(doc.session_context.request.arguments['file'][0].decode('utf-8')))
        matrix = makeMatrix(path)
        graph = generateForceDirectedDiagram(path, False)
    except KeyError:
        df = get_filtered_df()
        matrix = makeMatrix(df, df=True)
        graph = generateForceDirectedDiagram(df, False, df=True)
    # Put parameters in panel with param to change direction and type of graph.
    pn.extension('plotly')

    pane = pn.Row(graph, matrix)
    return pane.get_root(doc)

def getFilePath(file):
    file = file + '.h5'
    return os.path.join(server.config['UPLOAD_FOLDER'], file)
