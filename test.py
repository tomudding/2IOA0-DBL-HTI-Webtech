from timeit import default_timer as timer

#start = timer()
import csv
import holoviews as hv
import json
import networkx as nx
import pandas as pd

from bokeh.embed import components
from holoviews.operation.datashader import datashade, bundle_graph
from holoviews import opts

hv.extension('bokeh')
defaults = dict(width=400, height=400, padding=0.1)
hv.opts.defaults(opts.EdgePaths(**defaults), opts.Graph(**defaults), opts.Nodes(**defaults))
#end = timer()
#print(end - start)

start = timer()
with open("datasets/GephiMatrix_co-citation.csv", 'r') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.readline())

#pd.set_option('display.width', 120)
#pd.set_option('display.max_columns', 5)
#pd.set_option('display.max_rows', 2000)

df = pd.DataFrame()
for chunk in pd.read_csv("datasets/GephiMatrix_co-citation.csv", sep=dialect.delimiter, mangle_dupe_cols=True, index_col=False, chunksize=1000):
    df = pd.concat([df, chunk], ignore_index=True)

#df.index.name = "delete"
#df = df.drop(index='delete')

nodes = df.columns.values.tolist()
nodes.pop(0)
#print(nodes)
df["Unnamed: 0"] = nodes
df = df.rename(columns={'Unnamed: 0': 'name'})
df = df.set_index(keys='name')
#print(df)
end = timer()
print(end - start)

start = timer()
G = nx.from_pandas_adjacency(df)
#print(nx.info(G))
graph = hv.Graph.from_networkx(G, nx.layout.circular_layout).opts(directed=True, width=600, height=600, arrowhead_length=0.05)
end = timer()
print(end - start)

start = timer()
circular = bundle_graph(graph)
plot = datashade(circular, width=800, height=800) * circular.nodes
renderer = hv.renderer('bokeh')
#renderer.save(graph, 'test')

test = renderer.server_doc(plot)
test.title = "test"
#json = json.dumps(json_item(test, "radialnodelink"))
#print(json)
end = timer()
print(end - start)