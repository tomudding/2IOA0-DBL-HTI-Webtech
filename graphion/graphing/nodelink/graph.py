"""
Author(s): Tom Udding, Steven van den Broek, Yuqing Zeng, Tim van de Klundert
Created: 2019-05-03
Edited: 2019-05-19
"""
from bokeh.plotting import reset_output
from bokeh.models import Circle
from graphion.graphing.parser import processCSVMatrix
from holoviews import opts, renderer, extension
from holoviews.element.graphs import Graph
import networkx as nx
from networkx import from_pandas_adjacency
from networkx.drawing.layout import circular_layout
from networkx.drawing.nx_agraph import graphviz_layout
import numpy as np
from pandas import read_hdf, Series
import panel as pn
import plotly.graph_objs as go

# Function to decrease the size of the submatrix
def decreaseDiagramSize(file):
    df = read_hdf(file) # !!! TODO: Change implementation, reads whole file into memory, will work for the test datasets but not for larger datasets
    names = df.columns
    # submatrix for quicker development
    if (len(names) > 150):
        df = df.head(150)[names[0:150]]
    return df

# Generate a hierarchical node-link diagram
def generateHierarchicalDiagram(file):
    df = decreaseDiagramSize(file)
    # set defaults for HoloViews
    extension('bokeh')
    renderer('bokeh').webgl = True
    reset_output()
    defaults = dict(width=400, height=400, padding=0.1)
    opts.defaults(opts.EdgePaths(**defaults), opts.Graph(**defaults), opts.Nodes(**defaults))

    G = from_pandas_adjacency(df)
    cutoff = 2 #adjust this parameter to filter edges
    SG = nx.Graph([(u, v, d) for u, v, d in G.edges(data=True) if d['weight'] > cutoff])

    graph = Graph.from_networkx(SG, positions = graphviz_layout(SG, prog ='dot')).opts(directed=isDirected, width=600, height=600, arrowhead_length=0.0005)
    # Make a panel and widgets with param for choosing a layout
    return pn.Column(graph)

# Generate a radial node-link diagram
def generateRadialDiagram(file):
    df = decreaseDiagramSize(file)

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


    print(df.head())
    # set defaults for HoloViews
    extension('bokeh')
    renderer('bokeh').webgl = True
    reset_output()
    defaults = dict(width=200, height=200, padding=0.1)
    opts.defaults(opts.EdgePaths(**defaults), opts.Graph(**defaults), opts.Nodes(**defaults))

    G = from_pandas_adjacency(df)

    graph = Graph.from_networkx(G, circular_layout)

    graph.nodes.data['degree'] = Series(degree_array)
    
    # I tried simply using node_size='degree', but if it only were that easy...
    graph = graph.opts(opts.Graph(node_size=35, directed=False, width=600, height=600, arrowhead_length=0.0005))
    print(graph.nodes.data.head())
    # Make a panel and widgets with param for choosing a layout
    return pn.Column(graph)

# Generate 3D graph
def generate3DDiagram(file):
    df = decreaseDiagramSize(file)
    names = df.columns.tolist()
    N = len(names)

    # remove some noise (assuming author similarity matrix)
    noise = []
    for name in names:
        if (len(df[name][df[name] == 0]) == len(names)):
            noise.append(name)

    for name in noise:
        names.remove(name)
    df.drop(noise, inplace=True)
    df.drop(noise, axis=1, inplace=True)

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
    Edges = np.array([(int(u), int(v), d) for (u, v, d) in G.edges(data=True) if d['weight'] >= 0.5])

    def make_edge(x, y, z, weight):
        return go.Scatter3d(
            x=x,
            y=y,
            z=z,
            line=dict(color='rgb(' + str(int(100 + (weight ** 2 - 0.25) * 100)) + ',100,100)', width=(weight * 3) ** 2),
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
        title="3-dimensional node-link diagram, edge weigthts >= 0.5",
        width=900,
        height=900,
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

    )

    data = [trace2] + edge_traces
    fig = go.Figure(data=data, layout=layout)
    pn.extension('plotly')
    return pn.pane.Plotly(fig)