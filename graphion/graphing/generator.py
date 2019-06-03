"""
Author(s): Tom Udding, Steven van den Broek, Sam Baggen
Created: 2019-05-03
Edited: 2019-06-03
"""
from graphion import server
from graphion.graphing.nodelink.graph import generateForceDirectedDiagram, generateHierarchicalDiagram, generateRadialDiagram, generate3DDiagram
from graphion.graphing.nodelink.graph import SelectEdgeCallback, SelectMatrixToNodeCallback, SelectNodeToMatrixCallback
from graphion.graphing.nodelink.graph import SelectEdgeLink, SelectMatrixToNodeLink, SelectNodeToMatrixLink
from graphion.graphing.matrix.protomatrix import makeMatrix
from graphion.graphing.matrix.protomatrix import SelectCallback, SelectedDataCallback
from graphion.graphing.matrix.protomatrix import SelectedDataLink, SelectLink
from graphion.upload import get_filtered_df
import os
import panel as pn
import time
import pandas

def generateBokehApp(doc):
    df = get_filtered_df()
    begin = time.time()
    matrix = makeMatrix(df.copy(), df=True)
    print("Matrix generation took: " + str(time.time()-begin))
    begin = time.time()
    graph = generateForceDirectedDiagram(df.copy(), False, df=True)
    print("Graph generation took: " + str(time.time()-begin))
    begin = time.time()
    #graph3D = generate3DDiagram(df.copy(), df=True)
    print("3D generation took: " + str(time.time() - begin))

    pn.extension('plotly')

    # pane = pn.Column(pn.Row(graph, matrix), graph3D)
    pane = pn.Row(graph[0], matrix[0])
    # pane = pn.Pane(graph)

    #Setting up the linking, generateDiagram functions return three-tuple (panel, graph, points). Points is the selection layer
    #makeMatrix returns three-tuple (panel, matrix, names). Names are the indices of the matrix nodes
    SelectMatrixToNodeLink.register_callback('bokeh', SelectMatrixToNodeCallback)
    SelectEdgeLink.register_callback('bokeh', SelectEdgeCallback)
    SelectNodeToMatrixLink.register_callback('bokeh', SelectNodeToMatrixCallback)

    #Link matrix to the nodelink (both graph and points)
    SelectMatrixToNodeLink(matrix[1], graph[1])
    SelectNodeToMatrixLink(matrix[1], graph[2])
    SelectEdgeLink(matrix[1], graph[1])

    #Link nodelink to matrix (points only)
    SelectNodeToMatrixLink(graph[2], matrix[1])

    #Stevens linking (need to look at it)
    SelectedDataLink.register_callback('bokeh', SelectedDataCallback)
    SelectLink.register_callback('bokeh', SelectCallback)
    

    return pane.get_root(doc)

def getFilePath(file):
    file = file + '.h5'
    return os.path.join(server.config['UPLOAD_FOLDER'], file)