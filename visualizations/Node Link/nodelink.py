# pylint: disable = E0611, E1101

"""
Author(s): Sam Baggen and Steven van den Broek (for the data processing part)
Created: 2019-04-30
Edited: 2019-05-01
"""

import pandas as pd 
import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Circle, MultiLine
from bokeh.palettes import Viridis256

#Reading the file
fname = 'datasets/GephiMatrix_author_similarity.csv'
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

#Get total amount of nodes
N = len(names)
node_indices = list(range(N))

scale = math.ceil(N / 256)

#Iterate over dataframe and save non-zero edges
start = list() #Contains starting node index of each edge
end = list() #Contains ending node index of each edge
tolerance = 0.7 #Determine which edges are shown and which are not

index_count = 0 #Set start node index to 0
for row in df.itertuples(): #For each row in the dataframe
    index_count += 1 #Increase start node index by 1
    element_count = 0 #(Re)set second node index to 0
    for element in row: #For each element in each row
        element_count += 1 #Increase second node index by 1
        if type(element) == float:
            if element > tolerance and not element == 1.0:
                start.append(index_count) #Add starting node index to the edge starting list
                end.append(element_count) #Add ending node index to the edge ending list

#Create the plot with two axes, a title and interaction tools
plot = figure(title='Circular Node-Link Diagram', x_range=(0 - (N * 1.1) , N * 1.1), y_range=(0 - (N * 1.1) , N * 1.1),
              tools='pan, wheel_zoom, reset', toolbar_location = 'right', frame_height = 800, frame_width = 800)

#Create the graph object
graph = GraphRenderer()

#Assign the correct data for the edges
graph.edge_renderer.data_source.data = dict(
    start = start,
    end = end)
graph.edge_renderer.glyph = MultiLine(line_color = Viridis256[200])

#Assign the correct data for the nodes
graph.node_renderer.data_source.add(node_indices, 'index')
graph.node_renderer.data_source.add(Viridis256 * scale, 'color')
graph.node_renderer.glyph = Circle(radius = N * 0.02, fill_color='color')

#Start of circular layout code
circ = [i*2*math.pi/N for i in node_indices]
x = [N*math.cos(i) for i in circ]
y = [N*math.sin(i) for i in circ]

#Assign the correct x and y values to all nodes
graph_layout = dict(zip(node_indices, zip(x, y)))
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

#Show the plot
plot.renderers.append(graph)
show(plot)