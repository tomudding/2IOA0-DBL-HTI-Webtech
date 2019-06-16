"""
Author(s): Tom Udding, Steven van den Broek, Yuqing Zeng, Tim van de Klundert, Sam Baggen
Created: 2019-05-03
Edited: 2019-06-15
"""
from bokeh.plotting import figure, reset_output
from bokeh.models import Circle, ColumnDataSource, HoverTool
from community import best_partition
from graphion import server
from graphion.graphing.parser import processCSVMatrix
from holoviews import opts, renderer, extension
from holoviews.element.graphs import Graph
from math import sqrt, log
import networkx as nx
from networkx import DiGraph, Graph, from_pandas_adjacency
from networkx.algorithms.centrality import degree_centrality
from networkx.drawing.layout import circular_layout, spring_layout
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.drawing.nx_pylab import draw_networkx_edges
from networkx.classes.function import number_of_nodes, is_directed
import numpy as np
from pandas import read_hdf, Series
import panel as pn
import plotly.graph_objs as go
import holoviews as hv
from holoviews.operation.datashader import datashade, bundle_graph, dynspread
from colorcet import palette
from sys import maxsize
from bokeh.palettes import Cividis256, Viridis256, Inferno256
import param

hv.extension('bokeh')

"""
Function to decrease the size of the submatrix.
"""
def decreaseDiagramSize(file):
    df = read_hdf(file) # !!! TODO: Change implementation, reads whole file into memory, will work for the test datasets but not for larger datasets
    names = df.columns
    # submatrix for quicker development
    if (len(names) > 400):
        df = df.head(400)[names[0:400]]
    return df

"""
Function to generate a node-link diagram based on a
```filePath```, a ```diagramType```, and ```isDirected```.

Returns a Panel.Column of the diagram.
"""
def generateNodeLinkDiagram(df, diagramType, datashaded=True):
    diagramType = diagramType.upper()

    class Nodelink(param.Parameterized):
        colorList = ['kbc', 'kgy', 'bgy', 'bmw', 'bmy', 'cividis', 'dimgray', 'fire', 'inferno', 'viridis']
        colorMap = {}
        color_palette = param.ObjectSelector(default='kbc',
                                             objects=colorList)
        node_size = param.ObjectSelector(default='indegreesize',
                                            objects=['indegreesize', 'outdegreesize', 'totaldegreesize', 'inweightsize', 'outweightsize', 'totalweightsize'])
        node_color = param.ObjectSelector(default='totalweight',
                                            objects=['indegree', 'outdegree', 'totaldegree', 'inweight', 'outweight', 'totalweight'])

        def __init__(self, diagramType):
            self.diagramType = diagramType
            super(Nodelink, self).__init__()
            self.plot, self.points = self.make_plot()

        def make_plot(self):
            G = from_pandas_adjacency(df)

            """
            Create NetworkX graph layout manager
            """
            if diagramType == "FORCE":
                layout = spring_layout(G, k=1.42 / sqrt(number_of_nodes(G)), seed=server.config['SEED'])
            elif diagramType == "HIERARCHICAL":
                layout = graphviz_layout(nx.Graph([(u, v, d) for u, v, d in G.edges(data=True)]), prog='dot')
                pass
            elif diagramType == "RADIAL":
                layout = circular_layout(G)
            else:
                pass

            # get node and edge information from graph
            nodes, nodes_coordinates = zip(*sorted(layout.items()))
            nodes_x, nodes_y = list(zip(*nodes_coordinates))

            # calculate centrality
            centrality = degree_centrality(G)
            _, nodeCentralities = zip(*sorted(centrality.items()))

            # get degree information
            if is_directed(G):
                inDegreeSize = dict(G.in_degree)
                inDegree = inDegreeSize.copy()
                outDegreeSize = dict(G.out_degree)
                outDegree = outDegreeSize.copy()
                totalDegreeSize = {}
                for n in nodes:
                    totalDegreeSize[n] = {n: inDegreeSize[n] + outDegreeSize[n]}
                totalDegree = totalDegreeSize.copy()
            else:
                inDegreeSize = dict(G.degree)
                inDegree = inDegreeSize.copy()
                outDegreeSize = inDegreeSize.copy()
                outDegree = inDegreeSize.copy()
                totalDegreeSize = inDegreeSize.copy()
                totalDegree = inDegreeSize.copy()

            # get weight information
            if is_directed(G):
                inWeightSize = dict(G.in_degree(weight='weight'))
                inWeight = inWeightSize.copy()
                outWeightSize = dict(G.out_degree(weight='weight'))
                outWeight = outWeightSize.copy()
                totalWeightSize = {}
                for n in nodes:
                    totalWeightSize[n] = {n: inWeightSize[n] + outWeightSize[n]}
                totalWeight = totalWeightSize.copy()
            else:
                inWeightSize = dict(G.degree(weight='weight'))
                inWeight = inWeightSize.copy()
                outWeightSize = inWeightSize.copy()
                outWeight = inWeightSize.copy()
                totalWeightSize = inWeightSize.copy()
                totalWeight = inWeightSize.copy()

            # Creating a scale to ensure that the node sizes don't go bananas
            minNodeSize = 0.1 # minNodeSize * maxNodeSize = minimum node size
            maxIn = -maxsize - 1
            minIn = maxsize
            maxOut = -maxsize - 1
            minOut = maxsize
            maxTot = -maxsize - 1
            minTot = maxsize
            maxInw = -maxsize - 1
            minInw = maxsize
            maxOutw = -maxsize - 1
            minOutw = maxsize
            maxTotw = -maxsize - 1
            minTotw = maxsize
            for n in nodes:
                ind = inDegreeSize[n]
                outd = outDegreeSize[n]
                totd = totalDegreeSize[n]
                inw = inWeightSize[n]
                outw = outWeightSize[n]
                totw = totalWeightSize[n]
                if ind > maxIn:
                    maxIn = ind
                elif ind < minIn:
                    minIn = ind
                if outd > maxOut:
                    maxOut = outd
                elif outd < minOut:
                    minOut = outd
                if totd > maxTot:
                    maxTot = totd
                elif totd < minTot:
                    minTot = totd
                if inw > maxInw:
                    maxInw = inw
                elif inw < minInw:
                    minInw = inw
                if outw > maxOutw:
                    maxOutw = outw
                elif outw < minOutw:
                    minOutw = outw
                if totw > maxTotw:
                    maxTotw = totw
                elif totw < minTotw:
                    minTotw = totw

            if maxIn == minIn:
                sameInDegree = True
            else:
                sameInDegree = False
                for n in nodes:
                    result = (inDegreeSize[n] - minIn) / maxIn
                    if result < minNodeSize:
                        inDegreeSize[n] = minNodeSize
                    else:
                        inDegreeSize[n] = result
            if maxOut == minOut:
                sameOutDegree = True
            else:
                sameOutDegree = False
                for n in nodes:
                    result = (outDegreeSize[n] - minOut) / maxOut
                    if result < minNodeSize:
                        outDegreeSize[n] = minNodeSize
                    else:
                        outDegreeSize[n] = result
            if maxTot == minTot:
                sameTotalDegree = True
            else:
                sameTotalDegree = False
                for n in nodes:
                    result = (totalDegreeSize[n] - minTot) / maxTot
                    if result < minNodeSize:
                        totalDegreeSize[n] = minNodeSize
                    else:
                        totalDegreeSize[n] = result
            if maxInw == minInw:
                sameInWeight = True
            else:
                sameInWeight = False
                for n in nodes:
                    result = (inWeightSize[n] - minInw) / maxInw
                    if result < minNodeSize:
                        inWeightSize[n] = minNodeSize
                    else:
                        inWeightSize[n] = result
            if maxOutw == minOutw:
                sameOutWeight = True
            else:
                sameOutWeight = False
                for n in nodes:
                    result = (outWeightSize[n] - minOutw) / maxOutw
                    if result < minNodeSize:
                        outWeightSize[n] = minNodeSize
                    else:
                        outWeightSize[n] = result
            if maxTotw == minTotw:
                sameTotalWeight = True
            else:
                sameTotalWeight = False
                for n in nodes:
                    result = (totalWeightSize[n] - minTotw) / maxTotw
                    if result < minNodeSize:
                        totalWeightSize[n] = minNodeSize
                    else:
                        totalWeightSize[n] = result

            # Making a dictionary for all attributes, and ensuring none of the values go crazy.
            attributes = {}
            maxNodeSize = 30
            for n in nodes:
                outd = outDegreeSize[n]
                totd = totalDegreeSize[n]
                inw = inWeightSize[n]
                outw = outWeightSize[n]
                totw = totalWeightSize[n]

                if sameInDegree:
                    ind = 1
                else:
                    ind = inDegreeSize[n]
                if sameOutDegree:
                    outd = 1
                else:
                    outd = outDegreeSize[n]
                if sameTotalDegree:
                    totd = 1
                else:
                    totd = totalDegreeSize[n]
                if sameInWeight:
                    inw = 1
                else:
                    inw = inWeightSize[n]
                if sameOutWeight:
                    outw = 1
                else:
                    outw = outWeightSize[n]
                if sameTotalWeight:
                    totw = 1
                else:
                    totw = totalWeightSize[n]

                attributes[n] = {'indegreesize': ind * maxNodeSize,
                                 'outdegreesize': outd * maxNodeSize,
                                 'totaldegreesize': totd * maxNodeSize,
                                 'inweightsize': inw * maxNodeSize,
                                 'outweightsize': outw * maxNodeSize,
                                 'totalweightsize': totw * maxNodeSize,
                                 'indegree': inDegree[n],
                                 'outdegree': outDegree[n],
                                 'totaldegree': totalDegree[n],
                                 'inweight': inWeight[n],
                                 'outweight': outWeight[n],
                                 'totalweight': totalWeight[n],
                                 'count': 0}

            nx.set_node_attributes(G, attributes)
            plot = hv.Graph.from_networkx(G, layout)

            # disabling displaying all node info on hovering over the node
            tooltips = [('Index', '@index'), ('In-Degree', '@indegree'), ('Out-Degree', '@outdegree'), ('Total Degree', '@totaldegree'),
                        ('In Edge Weight', '@inweight'), ('Out Edge-Weight', '@outweight'), ('Total Edge-Weight', '@totalweight')]
            hover = HoverTool(tooltips=tooltips)

            # Make custom dictionary with color palettes
            for c in self.colorList:
                if c == 'cividis':
                    self.colorMap[c] = Cividis256
                elif c == 'viridis':
                    self.colorMap[c] = Viridis256
                elif c == 'inferno':
                    self.colorMap[c] = Inferno256
                else:
                    self.colorMap[c] = palette[c]

            # Comment the following two/three lines to disable edgebundling and datashading.
            if max(nodeCentralities) > 0:
                if datashaded:
                    plot = bundle_graph(plot)
            points = plot.nodes
            points.opts(cmap=self.colorMap[self.color_palette], color=self.node_color, size=self.node_size,
                        tools=['box_select', 'lasso_select', 'tap', hover], active_tools=['wheel_zoom'], toolbar='above',
                        show_legend=False, width=600, height=600)
            return plot, points

        def view(self):
            if datashaded:
                plot = dynspread(datashade(self.plot, normalization='linear', width=600, height=600, cmap=self.colorMap[self.color_palette]))
                self.points.opts(cmap=self.colorMap[self.color_palette], color=self.node_color, size=self.node_size)
                return (plot, self.points)
            return (self.plot, self.points)

    return Nodelink(diagramType)

# Generate 3D graph
def generate3DDiagram(file, df=False):
    if not df:
        df = decreaseDiagramSize(file)
    else:
        df = file

    names = df.columns.tolist()
    N = len(names)

    G = nx.from_pandas_adjacency(df)
    G = nx.convert_node_labels_to_integers(G)
    # 3d spring layout
    pos = nx.spring_layout(G, dim=3)
    # numpy array of x,y,z positions in sorted node order
    layt = np.array([pos[v] for v in sorted(G)])
    # scalar colors
    scalars = np.array(list(G.nodes())) + 5
    # edges

    maximum = 0
    for (u, v, d) in G.edges(data=True):
        w = d['weight']
        if w > maximum:
            maximum = w

    Edges = np.array([(int(u), int(v), {'weight': d['weight']/maximum}) for (u, v, d) in G.edges(data=True) if d['weight'] > 0])

    def make_edge(x, y, z, weight):
        return go.Scatter3d(
            x=x,
            y=y,
            z=z,
            # line=dict(color='rgb(' + str(int(100 + (weight ** 2 - 0.25) * 100)) + ',100,100)', width=(weight * 3) ** 2),
            line=dict(color='rgb(' + str(int(weight)*180) + ', 0, 0)', width=(weight * 3) ** 2),
            hoverinfo='none',
            mode='lines')

    Xn = [layt[k][0] for k in range(N)]  # x-coordinates of nodes
    Yn = [layt[k][1] for k in range(N)]  # y-coordinates
    Zn = [layt[k][2] for k in range(N)]  # z-coordinates
    edge_traces = []

    for e in Edges:
        x_edge_ends = [layt[e[0]][0], layt[e[1]][0], None]  # x-coordinates of edge ends
        y_edge_ends = [layt[e[0]][1], layt[e[1]][1], None]
        z_edge_ends = [layt[e[0]][2], layt[e[1]][2], None]
        edge_traces.append(make_edge(x_edge_ends, y_edge_ends, z_edge_ends, e[2]['weight']))

    trace2 = go.Scatter3d(x=Xn,
                          y=Yn,
                          z=Zn,
                          mode='markers',
                          marker=dict(symbol='circle',
                                      size=6,
                                      color=scalars,
                                      colorscale='Viridis',
                                      line=dict(color='rgb(50,50,50)', width=0.5)
                                      ),
                          text=names,
                          hoverinfo='text'
                          )

    axis = dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title=''
                )

    layout = go.Layout(
        title="Force-directed layout",
        width=600,
        height=600,
        showlegend=False,
        scene=dict(
            xaxis=dict(axis),
            yaxis=dict(axis),
            zaxis=dict(axis),
        ),
        margin=dict(
            t=100
        ),
        hovermode='closest',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'

    )

    data = [trace2] + edge_traces
    fig = go.Figure(data=data, layout=layout)
    pn.extension('plotly')
    painful = pn.pane.Plotly(fig)
    return painful