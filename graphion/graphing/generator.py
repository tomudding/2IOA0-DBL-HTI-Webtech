"""
Author(s): Tom Udding, Steven van den Broek, Sam Baggen
Created: 2019-05-03
Edited: 2019-06-06
"""
from graphion import server
from graphion.graphing.nodelink.graph import generateForceDirectedDiagram, generateHierarchicalDiagram, generateRadialDiagram, generate3DDiagram
from graphion.graphing.linking import SelectEdgeCallback, SelectMatrixToNodeCallback, SelectNodeToMatrixCallback
from graphion.graphing.linking import SelectEdgeLink, SelectMatrixToNodeLink, SelectNodeToMatrixLink
from graphion.graphing.matrix.protomatrix import makeMatrix
from graphion.upload import get_filtered_df
import os
import panel as pn
import time

import param
import holoviews as hv


def generateBokehApp(doc):
    global visApp, matrix, hierarchical, graph3D, force, radial
    matrix = None
    hierarchical = None
    graph3D = None
    force = None
    radial = None

    class VisApp(param.Parameterized):
        Screen1 = param.ObjectSelector(default="force",
                                          objects=["none", "radial", "force", "hierarchical", "3d"])
        Screen2 = param.ObjectSelector(default="matrix",
                                      objects=["none", "matrix"])
        
        Ordering = param.ObjectSelector(default="none",
                                          objects=["none", "single", "average", "complete", "centroid", "weighted",
                                                   "median", "ward"])

        Metric = param.ObjectSelector(default="euclidean",
                                      objects=["euclidean", "minkowski", "cityblock", "sqeuclidean", "cosine",
                                               "correlation", "hamming", "jaccard", "chebyshev", "canberra",
                                               "braycurtis"])

        Color_palette = param.ObjectSelector(default='kbc',
                                             objects=['kbc', 'kgy', 'bgy', 'bmw', 'bmy', 'cividis', 'dimgray', 'fire',
                                                      'inferno', 'viridis'])

        @param.depends('Screen1', 'Screen2', 'Ordering', 'Metric', 'Color_palette')
        def view(self):
            global s1
            s1 = None
            if self.Screen1 == "radial":
                s1 = getRadial(df)
            if self.Screen1 == "force":
                s1 = getForce(df)
            if self.Screen1 == "hierarchical":
                s1 = getHierarchical(df)
            if self.Screen1 == "3d":
                s1 = getGraph3D(df)
            # print(s1[1])
            s2 = None
            if self.Screen2 == "matrix":
                s2 = getMatrix(df)

            # Setting up the linking, generateDiagram functions return two-tuple (graph, points). Points is the selection layer
            # makeMatrix returns matrix_dropdown object. matrix.view returns the heatmap object
            #SelectMatrixToNodeLink.register_callback('bokeh', SelectMatrixToNodeCallback)
            #SelectEdgeLink.register_callback('bokeh', SelectEdgeCallback)
            #SelectNodeToMatrixLink.register_callback('bokeh', SelectNodeToMatrixCallback)

            # Link matrix to the nodelink (both graph and points)
            #SelectMatrixToNodeLink(s2.view, s1[1])
            #SelectEdgeLink(s2.view, s1[0])

            # Link nodelink to matrix (points only)
            #SelectNodeToMatrixLink(s1[1], s2.view)

            s2.reordering = self.Ordering
            s2.metric = self.Metric
            s2.color_palette = self.Color_palette
            s2Pane = pn.Column(s2.view)

            return pn.Row(s1[0], s2Pane)

    df = get_filtered_df()

    visApp = VisApp()

    # begin = time.time()
    # m = getMatrix(df)
    # print("Matrix generation took: " + str(time.time()-begin))
    # begin = time.time()
    # h = getHierarchical(df)
    # print("Graph generation took: " + str(time.time()-begin))
    # begin = time.time()
    # threeD = getGraph3D(df)
    # print("3D generation took: " + str(time.time() - begin))



    # pane = pn.Column(pn.Row(graph, matrix), graph3D)
    # pane = pn.Column(pn.Row(h, m), threeD)
    # pane = pn.Pane(graph)



    pn.extension('plotly')
    return pn.Pane(visApp.view).get_root(doc)


def changeScreen1(new_type):
    visApp.Screen1 = new_type

def changeOrdering(new_ordering):
    visApp.Ordering = new_ordering

def changeMetric(new_metric):
    visApp.Metric = new_metric

def changePalette(new_palette):
    visApp.Color_palette = new_palette

def getFilePath(file):
    file = file + '.h5'
    return os.path.join(server.config['UPLOAD_FOLDER'], file)

def getMatrix(df):
    global matrix
    if 'matrix' in globals() and matrix is not None:
        return matrix
    else:
        matrix = makeMatrix(df.copy(), s1[1], df=True)
        return matrix

def getHierarchical(df):
    global hierarchical
    if 'hierarchical' in globals() and hierarchical is not None:
        return hierarchical
    else:
        hierarchical = generateHierarchicalDiagram(df.copy(), False, df=True)
        return hierarchical

def getGraph3D(df):
    global graph3D
    if 'graph3D' in globals() and graph3D is not None:
        return graph3D
    else:
        graph3D = generate3DDiagram(df.copy(), df=True)
        return graph3D

def getForce(df):
    global force
    if 'force' in globals() and force is not None:
        return force
    else:
        force = generateForceDirectedDiagram(df, False, df=True)
        return force

def getRadial(df):
    global radial
    if 'radial' in globals() and radial is not None:
        return radial
    else:
        radial = generateRadialDiagram(df, False, df=True)
        return radial
