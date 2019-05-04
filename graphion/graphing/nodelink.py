"""
Author(s): Sam Baggen, Steven van den Broek, Tom Udding
Created: 2019-04-30
Edited: 2019-05-03
"""
import os
import pandas as pd
import math
import networkx as nx

from graphion import server
from graphion.processing.clean_df import to_pandas_df

from bokeh.io import show, output_file
from bokeh.embed import components
#from bokeh.plotting import figure
from bokeh.models import Plot, GraphRenderer, StaticLayoutProvider, Circle, MultiLine, Arrow, NormalHead, Range1d, PanTool, BoxZoomTool, ResetTool
from bokeh.palettes import Viridis256
from bokeh.models.graphs import from_networkx

def generateNodeLinkGraph(file):
    #Get pandas dataframe and names
    df, names = to_pandas_df(file, 150)
    #Get total amount of nodes
    N = len(names)
    node_indices = list(range(N)) #Create list of numeric node indices

    # Scale for the repeating pattern of the colours
    scale = math.ceil(N / 256)

    #Iterate over dataframe and save non-zero edges
    start = [] #Contains starting node index of each edge
    end = [] #Contains ending node index of each edge
    tolerance = 0.75 #Determine which edges are shown and which are not

    index_count = 0 #Set start node index to 0
    for row in df.itertuples(): #For each row in the dataframe
        index_count += 1 #Increase start node index by 1
        element_count = 0 #(Re)set second node index to 0
        for element in row: #For each element in each row
            element_count += 1 #Increase second node index by 1
            if type(element) == float:
                #if element == 1.0: #Code in case for symmetric matrix, effectively halving running time of this loop
                #    break
                #elif element > tolerance:
                if element > tolerance and not element == 1.0:
                    start.append(index_count) #Add starting node index to the edge starting list
                    end.append(element_count) #Add ending node index to the edge ending list

    #Create the plot with two axes, a title and interaction tools
    #plot = figure(title='Circular Node-Link Diagram', x_range=(0 - (N * 2.1) , N * 2.1), y_range=(0 - (N * 2.1) , N * 2.1),
    #              tools='pan, wheel_zoom, reset', toolbar_location = 'right', frame_height = 400, frame_width = 400, output_backend="webgl")
    plot = Plot(x_range=Range1d(0 - (N * 2.1) , N * 2.1), y_range=Range1d(0 - (N * 2.1) , N * 2.1),
              toolbar_location = 'right', frame_height = 400, frame_width = 400, output_backend="webgl")

    plot.title.text = "Circular Node-Link Diagram"

    plot.add_tools(PanTool(), BoxZoomTool(), ResetTool())

    #Create the graph object
    graph = GraphRenderer()

    #Assign the correct data for the edges
    #graph.edge_renderer.data_source.data = dict(
    #    start = start,
    #    end = end)
    #graph.edge_renderer.glyph = MultiLine(line_color = Viridis256[200])

    #Assign the correct data for the nodes
    graph.node_renderer.data_source.add(node_indices, 'index')
    graph.node_renderer.data_source.add(Viridis256 * scale, 'color')
    graph.node_renderer.glyph = Circle(radius = N * 0.0025, fill_color='color')

    #Start of circular layout code
    circ = [i * 2 * math.pi/N for i in node_indices]
    x = [2 * N * math.cos(i) for i in circ]
    y = [2 * N * math.sin(i) for i in circ]

    #Assign the correct x and y values to all nodes
    graph_layout = dict(zip(node_indices, zip(x, y)))
    graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

    #Arrow code test
    for start_index in start:
        start_index -= 1
        for end_index in end:
            end_index -= 1
            plot.add_layout(Arrow(end = NormalHead(fill_color = Viridis256[200], size = N * 0.1), x_start = x[start_index], y_start = y[start_index],
                                  x_end = x[end_index], y_end = y[end_index], line_color = Viridis256[200]))
            end_index += 1
        start_index += 1

    #Show the plot
    plot.renderers.append(graph)
    script, div = components(plot)
    return script, div