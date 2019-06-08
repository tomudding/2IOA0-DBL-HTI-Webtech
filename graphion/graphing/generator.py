"""
Author(s): Tom Udding, Steven van den Broek, Sam Baggen
Created: 2019-05-03
Edited: 2019-06-08
"""
from graphion import server
from graphion.graphing.nodelink.graph import generateForceDirectedDiagram, generateHierarchicalDiagram, generateRadialDiagram, generate3DDiagram
from graphion.graphing.linking import SelectEdgeCallback, SelectMatrixToNodeCallback, SelectNodeToMatrixCallback
from graphion.graphing.linking import SelectEdgeLink, SelectMatrixToNodeLink, SelectNodeToMatrixLink
from graphion.graphing.matrix.protomatrix import makeMatrix
from graphion.upload import get_filtered_df, is_directed
import os
import panel as pn
import time

import param
import holoviews as hv

def generateBokehApp(doc):
    sid = str(doc.session_context.request.arguments['sid'][0].decode('utf-8'))
    print(sid)
    gsh = GraphionSessionHandler(sid)
    print("---------------------------------------------------")
    print(gsh.identifier)
    print(gsh.cache)
    print("---------------------------------------------------")
    print(type(gsh.get("")))
    print(gsh.get("sparce"))
    print("---------------------------------------------------")
    gsh.set("test", True)
    print(gsh.get("test"))
    print(gsh.get(""))
    print("---------------------------------------------------")

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
            gsh.set("s1", None)
            if self.Screen1 == "radial":
                gsh.set("s1", getRadial(df, gsh))
            if self.Screen1 == "force":
                gsh.set("s1", getForce(df, gsh))
            if self.Screen1 == "hierarchical":
                gsh.set("s1", getHierarchical(df, gsh))
            if self.Screen1 == "3d":
                gsh.set("s1", getGraph3D(df, gsh))
            # print(s1[1])
            s2 = None
            if self.Screen2 == "matrix":
                s2 = getMatrix(df, gsh)

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

            return pn.Row(session.get("s1")[0], s2Pane)

    df = get_filtered_df(gsh)
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

def getMatrix(df, gsh):
    if gsh.has("matrix"):
        return gsh.get("matrix")
    else:
        generatedMatrix = makeMatrix(df.copy(), gsh.get("s1")[1], df=True)
        # do not generate in gsh.set(), this requires return gsh.get() which will be expensive.
        gsh.set("matrix", generatedMatrix)
        return generatedMatrix

def getHierarchical(df, gsh):
    if gsh.has("hierarchical"):
        return gsh.get("hierarchical")
    else:
        generatedDiagram = generateHierarchicalDiagram(df.copy(), False, df=True)
        # do not generate in gsh.set(), this requires return gsh.get() which will be expensive.
        gsh.set("hierarchical", generatedDiagram)
        return generatedDiagram

def getGraph3D(df, gsh):
    if gsh.has("graph3D"):
        return gsh.get("graph3D")
    else:
        generatedDiagram = generate3DDiagram(df.copy(), df=True)
        # do not generate in gsh.set(), this requires return gsh.get() which will be expensive.
        gsh.set("graph3D", generatedDiagram)
        return generatedDiagram

def getForce(df, gsh):
    if gsh.has("force"):
        return gsh.get("force")
    else:
        generatedDiagram = generateForceDirectedDiagram(df.copy(), False, df=True)
        # do not generate in gsh.set(), this requires return gsh.get() which will be expensive.
        gsh.set("force", generatedDiagram)
        return generatedDiagram

def getRadial(df, gsh):
    if gsh.has("radial"):
        return gsh.get("radial")
    else:
        generatedDiagram = generateRadialDiagram(df.copy(), False, df=True)
        # do not generate in gsh.set(), this requires return gsh.get() which will be expensive.
        gsh.set("radial", generatedDiagram)
        return generatedDiagram