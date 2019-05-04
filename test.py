import csv
import holoviews as hv
import networkx as nx
import pandas as pd

from bokeh.embed import components
from holoviews.operation.datashader import datashade, bundle_graph

hv.extension('bokeh')

with open("datasets/GephiMatrix_co-citation.csv", 'r') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.readline())

pd.set_option('display.width', 120)
pd.set_option('display.max_columns', 5)
pd.set_option('display.max_rows', 2000)

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

G = nx.from_pandas_adjacency(df)
print(nx.info(G))
graph = hv.Graph.from_networkx(G, nx.layout.circular_layout).opts(directed=True, width=600, height=600)
circular = bundle_graph(graph)
plot = datashade(circular, width=800, height=800) * circular.nodes

renderer = hv.renderer('bokeh')
#renderer.save(graph, 'test')

renderer.save(plot, 'test')