"""
Author(s): Tom Udding, Steven van den Broek
Created: 2019-05-03
Edited: 2019-05-31
"""
from graphion import server
from graphion.graphing.nodelink.graph import generateForceDirectedDiagram, generateHierarchicalDiagram, generateRadialDiagram, generate3DDiagram
from graphion.graphing.matrix.protomatrix import makeMatrix
from graphion.upload import get_filtered_df
import os
import panel as pn
import time
import pandas

def generateBokehApp(doc):
    df = get_filtered_df()
    matrix = makeMatrix(df, df=True)
    graph = generateForceDirectedDiagram(df, False, df=True)
    graph3D = generate3DDiagram(df, df=True)

    pn.extension('plotly')

    pane = pn.Column(pn.Row(graph, matrix), graph3D)
    return pane.get_root(doc)

def getFilePath(file):
    file = file + '.h5'
    return os.path.join(server.config['UPLOAD_FOLDER'], file)