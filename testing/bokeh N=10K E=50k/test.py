import random
import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval, PanTool, WheelZoomTool, ResetTool, HoverTool
from bokeh.palettes import Spectral8

N = 10000
E = 50000
node_indices = list(range(N))

plot = figure(title='Performance test', x_range=(-0.1,1.1), y_range=(-0.1,1.1), tools="")
plot.grid.visible = False
plot.axis.visible = False
graph = GraphRenderer()

graph.node_renderer.data_source.add(node_indices, 'index')
graph.node_renderer.data_source.add(Spectral8, 'color')
graph.node_renderer.glyph = Oval(height=0.01, width=0.01, fill_color='color')

graph.edge_renderer.data_source.data = dict(
    start=[random.randint(0, N) for i in range(E)],
    end=[random.randint(0, N) for i in range(E)])

print(graph.edge_renderer.data_source.data)

### start of layout code
circ = [i*2*math.pi/8 for i in node_indices]
x = [random.random() for i in circ]
y = [random.random() for i in circ]

node_hover_tool = HoverTool(tooltips=[("index", "@index")])
wheel_zoom = WheelZoomTool()
plot.add_tools(node_hover_tool, PanTool(), wheel_zoom, ResetTool())
plot.toolbar.active_scroll = wheel_zoom
graph_layout = dict(zip(node_indices, zip(x, y)))
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

plot.renderers.append(graph)

output_file('graph.html')
show(plot)