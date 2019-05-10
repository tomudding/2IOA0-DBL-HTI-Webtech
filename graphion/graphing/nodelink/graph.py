"""
Author(s): Tom Udding
Created: 2019-05-03
Edited: 2019-05-05
"""
from bokeh.document.document import Document
from bokeh.plotting import reset_output
from graphion.graphing.parser import processCSVMatrix
from holoviews.element.graphs import Graph
from holoviews import opts, renderer, extension
from networkx import from_pandas_adjacency
from networkx.drawing.layout import circular_layout, spring_layout
import panel as pn

# Generate graph
def generateGraph(file):
    df = processCSVMatrix(file)
    names = df.columns
    # submatrix for quicker development
    if (len(names) > 150):
        df = df.head(150)[names[0:150]]
    # set defaults for HoloViews
    extension('bokeh')
    renderer('bokeh').webgl = True
    reset_output()
    defaults = dict(width=200, height=200, padding=0.1)
    opts.defaults(opts.EdgePaths(**defaults), opts.Graph(**defaults), opts.Nodes(**defaults))

    G = from_pandas_adjacency(df)
    graph = Graph.from_networkx(G, circular_layout).opts(directed=False, width=600, height=600, arrowhead_length=0.0005)
    # Make a panel and widgets with param for choosing a layout
    return pn.Column(graph)