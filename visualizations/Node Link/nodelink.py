# pylint: disable = E0611, E1101
import pandas as pd 
import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval
from bokeh.palettes import Spectral8

df_data = pd.read_csv("datasets/GephiMatrix_author_similarity.csv")

N = 8
node_indices = list(range(N))

plot = figure(title='Graph Layout Demonstration', x_range=(-10.1,10.1), y_range=(-10.1,10.1),
              tools='', toolbar_location=None)

graph = GraphRenderer()

graph.edge_renderer.data_source.data = dict(
    start=[0]*N,
    end=node_indices)

graph.node_renderer.data_source.add(node_indices, 'index')
graph.node_renderer.data_source.add(Spectral8, 'color')
graph.node_renderer.glyph = Oval(height=0.1, width=0.2, fill_color='color')

### start of layout code
circ = [i*2*math.pi/8 for i in node_indices]
x = [10*math.cos(i) for i in circ]
y = [10*math.sin(i) for i in circ]

graph_layout = dict(zip(node_indices, zip(x, y)))
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

plot.renderers.append(graph)

output_file('graph.html')
show(plot)
