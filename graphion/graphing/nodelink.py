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

from bokeh.io import show, output_file
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Circle, MultiLine, Arrow, NormalHead
from bokeh.palettes import Viridis256
from bokeh.models.graphs import from_networkx

def createNodeLinkGraph(file):
    #Reading the file
    file = file + '.csv'
    fname = os.path.join(server.config['UPLOAD_FOLDER'], file)
    f = open(fname, 'r')

    #Reading first line
    line1 = f.readline()
    names = line1[1:].split(';')

    # Rename duplicates since there are people with the same name
    seen = {}
    dupes = []

    for index, name in enumerate(names):
        if name not in seen:
            seen[name] = 1
        else:
            if seen[name] == 1:
                dupes.append((index, name))
            seen[name] += 1

    # add 1, 2 etc after the name
    for pair in dupes:
        index = pair[0]
        name = pair[1]
        for i in range(seen[name]):
            names[index] = name + str((i+1))
            #print(names[index])

    # Read csv
    df = pd.read_csv(f, names=names, sep=';')

    # Fix it
    df = df.reset_index(level=1)
    names.append("delete")
    df.columns = names
    del df["delete"]
    df.set_index([df.columns], inplace=True)

    # Get names again for later use
    names = df.columns.tolist()

    # Get 150*150 sub matrix since otherwise the plot is very slow..
    df = df.head(150)[names[0:150]]
    names = df.columns.tolist()

    #Get total amount of nodes
    N = len(names)
    node_indices = list(range(N)) #Create list of numeric node indices

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
    plot = figure(title='Circular Node-Link Diagram', x_range=(0 - (N * 2.1) , N * 2.1), y_range=(0 - (N * 2.1) , N * 2.1),
                  tools='pan, wheel_zoom, reset', toolbar_location = 'right', frame_height = 800, frame_width = 800)

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