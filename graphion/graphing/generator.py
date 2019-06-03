"""
Author(s): Tom Udding, Steven van den Broek, Sam Baggen
Created: 2019-05-03
Edited: 2019-06-03
"""
from graphion import server
from graphion.graphing.nodelink.graph import generateForceDirectedDiagram, generateHierarchicalDiagram, generateRadialDiagram, generate3DDiagram, generateForceDirectedDiagramPane
from graphion.graphing.linking import SelectEdgeCallback, SelectMatrixToNodeCallback, SelectNodeToMatrixCallback
from graphion.graphing.linking import SelectEdgeLink, SelectMatrixToNodeLink, SelectNodeToMatrixLink
from graphion.graphing.matrix.protomatrix import makeMatrix, makeMatrixPane
from graphion.upload import get_filtered_df
import os
import panel as pn
import time
import pandas
import holoviews as hv

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

    #Setting up the linking, generateDiagram functions return two-tuple (graph, points). Points is the selection layer
    #makeMatrix returns matrix_dropdown object. matrix.view returns the heatmap object
    SelectMatrixToNodeLink.register_callback('bokeh', SelectMatrixToNodeCallback)
    SelectEdgeLink.register_callback('bokeh', SelectEdgeCallback)
    SelectNodeToMatrixLink.register_callback('bokeh', SelectNodeToMatrixCallback)

    #Link matrix to the nodelink (both graph and points)
    SelectMatrixToNodeLink(matrix.view(), graph[0])
    SelectMatrixToNodeLink(matrix.view(), graph[1])
    SelectEdgeLink(matrix.view(), graph[0])

    #Link nodelink to matrix (points only)
    SelectNodeToMatrixLink(graph[1], matrix.view())
    
    #Generates the panels
    graphPane = generateForceDirectedDiagramPane(graph)
    matrixPane = makeMatrixPane(matrix)

    pn.extension('plotly')

    # pane = pn.Column(pn.Row(graph, matrix), graph3D)
    pane = pn.Row(graphPane, matrixPane)
    # pane = pn.Pane(graph)

    return pane.get_root(doc)

def getFilePath(file):
    file = file + '.h5'
    return os.path.join(server.config['UPLOAD_FOLDER'], file)