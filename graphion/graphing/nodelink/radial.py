"""
Author(s): Tom Udding
Created: 2019-05-03
Edited: 2019-05-05
"""
from bokeh.document.document import Document
from graphion.graphing.parser import processCSVMatrix
from holoviews.element.graphs import Graph
from holoviews import opts, renderer, extension
from networkx import from_pandas_adjacency
from networkx.drawing.layout import circular_layout

# Radial Node-Link Graph Generator
def generateRadialGraph(file, isDirected):
    if isDirected == None:
        isDirected = False
    df = processCSVMatrix(file)
    return generateJSON(df, isDirected)

# Generate BokehJS compatible JSON
def generateJSON(df, isDirected):
    # set defaults for HoloViews
    extension('bokeh')
    defaults = dict(width=400, height=400, padding=0.1)
    opts.defaults(opts.EdgePaths(**defaults), opts.Graph(**defaults), opts.Nodes(**defaults))

    G = from_pandas_adjacency(df)
    graph = Graph.from_networkx(G, circular_layout).opts(directed=isDirected, width=600, height=600, arrowhead_length=0.05)

    renderedGraph = renderer('bokeh').server_doc(graph)
    return renderedGraph.roots[0]