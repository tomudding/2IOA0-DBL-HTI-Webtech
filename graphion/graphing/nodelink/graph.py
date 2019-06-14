"""
Author(s): Tom Udding, Steven van den Broek, Yuqing Zeng, Tim van de Klundert, Sam Baggen
Created: 2019-05-03
Edited: 2019-06-13
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

import param

import time


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
        color_palette = param.ObjectSelector(default='kbc',
                                             objects=['kbc', 'kgy', 'bgy', 'bmw', 'bmy', 'cividis', 'dimgray', 'fire',
                                                      'inferno', 'viridis'])
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
                # print(layout)
            elif diagramType == "HIERARCHICAL":
                # TODO: refactor hierarchical code from Sophia
                layout = graphviz_layout(nx.Graph([(u, v, d) for u, v, d in G.edges(data=True)]), prog='dot')
                pass
            elif diagramType == "RADIAL":
                layout = circular_layout(G)
                # print(layout)
            else:
                # TODO: throw exception
                pass

            print()

            # get node and edge information from graph
            nodes, nodes_coordinates = zip(*sorted(layout.items()))
            nodes_x, nodes_y = list(zip(*nodes_coordinates))

            # calculate centrality
            centrality = degree_centrality(G)
            _, nodeCentralities = zip(*sorted(centrality.items()))
            # currently not used code below but can easily be used again
            #if max(nodeCentralities) > 0:
            #    centralityList = [10 + 12 * t / max(nodeCentralities) for t in nodeCentralities]
            #else:
            #    centralityList = [10 + 12 * t for t in nodeCentralities]

            # create partitions, currently not used but can easily be used again
            #partition = best_partition(G)
            #_, nodePartitions = zip(*sorted(partition.items()))
            # nodeDataSource.add(nodePartitions, 'partition')
            #partitionColours = ["#b2182b", "#d6604d", "#f4a582", "#fddbc7", "#f7f7f7", "#d1e5f0", "#92c5de", "#4393c3",
            #                    "#2166ac"]  # safe to use for colourblind people
            #partitionList = [partitionColours[t % len(partitionColours)] for t in nodePartitions]

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
            else :
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
            else :
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
                                 'totalweight': totalWeight[n]}
            nx.set_node_attributes(G, attributes)

            # create the plot itself
            # if diagramType == "HIERARCHICAL":
            #     SG = nx.Graph([(u, v, d) for u, v, d in G.edges(data=True)])
            #     plot = hv.Graph.from_networkx(SG, positions=graphviz_layout(SG, prog='dot'))
            # else:
            plot = hv.Graph.from_networkx(G, layout)

            # disabling displaying all node info on hovering over the node
            tooltips = [('Index', '@index'), ('In-Degree', '@indegree'), ('Out-Degree', '@outdegree'), ('Total Degree', '@totaldegree'), 
                        ('In Edge Weight', '@inweight'), ('Out Edge-Weight', '@outweight'), ('Total Edge-Weight', '@totalweight')]
            hover = HoverTool(tooltips=tooltips)

            # begin = time.time()
            # Comment the following two/three lines to disable edgebundling and datashading.
            if max(nodeCentralities) > 0:
                if datashaded:
                    plot = bundle_graph(plot)
            points = plot.nodes
            points.opts(cmap=palette[self.color_palette], color=self.node_color, size=self.node_size,
                        tools=['box_select', 'lasso_select', 'tap', hover], active_tools=['wheel_zoom'], toolbar='above',
                        show_legend=False, width=600, height=600)
            return plot, points

        def view(self):
            if datashaded:
                plot = dynspread(datashade(self.plot, normalization='linear', width=600, height=600, cmap=palette[self.color_palette]))
                self.points.opts(cmap=palette[self.color_palette], color=self.node_color, size=self.node_size)
                return plot * self.points
            # plot = datashade(self.plot, normalization='linear', width=600, height=600)
            return self.plot * self.points

    # print("Edge bundling and datashading took: " + str(time.time()-begin))
    return Nodelink(diagramType)

# Generate a force-directed node-link diagram
def generateForceDirectedDiagram(file, isDirected, df=False):
    if not df:
        df = decreaseDiagramSize(file)
    else:
        df = file
    # convert Pandas DataFrame (Matrix) to NetworkX graph
    G = from_pandas_adjacency(df)
    layout = spring_layout(G, k=1.42/sqrt(number_of_nodes(G)))

    # get node and edge information from graph
    nodes, nodes_coordinates = zip(*sorted(layout.items()))
    nodes_x, nodes_y = list(zip(*nodes_coordinates))

    # calculate centrality
    centrality = degree_centrality(G)
    _, nodeCentralities = zip(*sorted(centrality.items()))
    centralityList = [10 + 12 * t / max(nodeCentralities) for t in nodeCentralities]

    # create partitions
    partition = best_partition(G)
    _, nodePartitions = zip(*sorted(partition.items()))
    #nodeDataSource.add(nodePartitions, 'partition')
    partitionColours = ["#b2182b","#d6604d","#f4a582","#fddbc7","#f7f7f7","#d1e5f0","#92c5de","#4393c3","#2166ac"] # safe to use for colourblind people
    partitionList = [partitionColours[t % len(partitionColours)] for t in nodePartitions]

    #Making a dictionary for all attributes
    attributes = {}
    for n in nodes:
        attributes[n] = {'Centrality': centralityList[nodes.index(n)], 'Partition': partitionList[nodes.index(n)]}
    nx.set_node_attributes(G, attributes)

    # create the plot itself
    plot = hv.Graph.from_networkx(G, layout)

    # colour the nodes based on the partition

    plot.opts(cmap = partitionColours, color_index='Partition', node_size='Centrality', inspection_policy='nodes', tools=['box_select', 'lasso_select', 'tap', 'hover'], toolbar='above', show_legend=False, width=600, height=600)

    renderer = hv.renderer('bokeh')
    renderer.webgl = True
    table = hv.Table(renderer.get_plot(plot).handles['glyph_renderer'].node_renderer.data_source.to_df())
    points = hv.Points((nodes_x, nodes_y, nodes, centralityList, partitionList), vdims=['Index', 'Centrality', 'Partition'])
    points.opts(cmap = partitionColours, color_index='Partition', size='Centrality', line_width = 1.5, line_color='#000000')
    # begin = time.time()

    # Comment the following two/three lines to disable edgebundling and datashading.
    plot = bundle_graph(plot)
    plot = (datashade(plot, normalization='linear', width=600, height=600) * plot.nodes).opts(opts.Nodes(cmap=partitionColours, color='Partition', size='Centrality',
               tools=['box_select', 'lasso_select', 'tap'], active_tools=['wheel_zoom'], toolbar='above', show_legend=False, width=600, height=600))

    # print("Edge bundling and datashading took: " + str(time.time()-begin))
    return (pn.Column(plot * points), points)

# Generate a hierarchical node-link diagram
def generateHierarchicalDiagram(file, isDirected, df=False):
    if not df:
        df = decreaseDiagramSize(file)
    else:
        df = file
    #df = decreaseDiagramSize(file)
    # set defaults for HoloViews
    extension('bokeh')
    renderer('bokeh').webgl = True
    reset_output()
    defaults = dict(width=400, height=400, padding=0.1)
    opts.defaults(opts.EdgePaths(**defaults), opts.Graph(**defaults), opts.Nodes(**defaults))

    G = from_pandas_adjacency(df)
    # cutoff = 2 #adjust this parameter to filter edges
    # SG = nx.Graph([(u, v, d) for u, v, d in G.edges(data=True) if d['weight'] > cutoff])
    SG = nx.Graph([(u, v, d) for u, v, d in G.edges(data=True)])

    graph = hv.Graph.from_networkx(SG, positions = graphviz_layout(SG, prog ='dot')).opts(directed=isDirected, width=600, height=600, show_legend=False, arrowhead_length=0.0005)
    graph = bundle_graph(graph)
    graph = (datashade(graph, normalization='linear', width=600, height=600) * graph.nodes).opts(
        opts.Nodes(width=600, height=600, tools=['box_select', 'lasso_select', 'tap', 'hover'], active_tools=['wheel_zoom'], toolbar='above', show_legend=False))
    # Make a panel and widgets with param for choosing a layout
    return pn.Column(graph)

# Generate a radial node-link diagram
def generateRadialDiagram(file, isDirected, colorpalette, df=False):
    if not df:
        df = decreaseDiagramSize(file)
    else:
        df = file
    #df = decreaseDiagramSize(file)

    node_count = df.shape[0]

    degree_array = node_count * [0]
    degree_index = 0
    #row_index = 0
    for _index,row in df.iterrows():
        degree = 0
        for value in row:
            if value > 0:
                degree += 1
        degree_array[degree_index] = degree
        degree_index += 1

    # print(df.head())
    # set defaults for HoloViews
    extension('bokeh')
    renderer('bokeh').webgl = True
    reset_output()
    defaults = dict(width=200, height=200, padding=0.1)
    opts.defaults(opts.EdgePaths(**defaults), opts.Graph(**defaults), opts.Nodes(**defaults))

    G = from_pandas_adjacency(df)
    layout = circular_layout(G)

    # get node and edge information from graph
    nodes, nodes_coordinates = zip(*sorted(layout.items()))
    nodes_x, nodes_y = list(zip(*nodes_coordinates))

    degreeList = []
    for n in nodes:
        if  (degree_array[nodes.index(n)] == 0 or degree_array[nodes.index(n)] == 1):
            degreeList.append(1)
        else:
            degreeList.append(degree_array[nodes.index(n)])

    degree_dict = {}
    for n in nodes:
        degree_dict[n] = {'Degree': degreeList[nodes.index(n)]}


    nx.set_node_attributes(G, degree_dict)
    graph = hv.Graph.from_networkx(G, circular_layout)
    #graph.nodes.data['degree'] = Series(degree_array)

    # I tried simply using node_size='degree', but if it only were that easy... (it is that easy :D, however most of the time the nodes are really small :( )
    graph.opts(node_size='Degree', directed=isDirected, width=600, height=600, arrowhead_length=0.0005, inspection_policy='nodes', tools=['box_select', 'lasso_select', 'tap', 'hover'], toolbar='above', show_legend=False)
    points = hv.Points((nodes_x, nodes_y, nodes, degreeList), vdims=['Index', 'Degree'])
    points.opts(line_width = 1.5, line_color='#000000', size='Degree')
    graph = bundle_graph(graph)
    graph = dynspread(datashade(graph, normalization='linear', width=600, height=600, cmap=palette[colorpalette]))
    return (pn.Column((graph * points.opts(size='Degree', tools=['box_select', 'lasso_select', 'tap', 'hover'], active_tools=['wheel_zoom'], toolbar='above', show_legend=False, width=600, height=600)))
        , graph, points)


# Generate 3D graph
def generate3DDiagram(file, df=False):

    if not df:
        df = decreaseDiagramSize(file)
    else:
        df = file

    names = df.columns.tolist()
    N = len(names)

    # remove some noise (assuming author similarity matrix)
    # noise = []
    # for name in names:
    #     if (len(df[name][df[name] == 0]) == len(names)):
    #         noise.append(name)
    #
    # for name in noise:
    #     names.remove(name)


    # df.drop(noise, inplace=True)
    # df.drop(noise, axis=1, inplace=True)
    # N = len(names)

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

    # trace1 = go.Scatter3d(x=Xe,
    #                      y=Ye,
    #                      z=Ze,
    #                      mode='lines',
    #                      line=dict(color='rgb(125,125,125)', width=1),
    #                      hoverinfo='none',
    #                      )

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