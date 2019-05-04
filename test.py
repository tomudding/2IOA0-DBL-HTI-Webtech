#from timeit import default_timer as timer

#start = timer()
from bokeh.document.document import Document
from csv import Sniffer
from holoviews.element.graphs import Graph
from holoviews import opts, renderer, extension
from networkx import from_pandas_adjacency
from networkx.drawing.layout import circular_layout
from pandas.core.frame import DataFrame
from pandas.core.reshape.concat import concat
from pandas.io.parsers import read_csv
#end = timer()
#print(end - start)

#start = timer()
extension('bokeh')
defaults = dict(width=400, height=400, padding=0.1)
opts.defaults(opts.EdgePaths(**defaults), opts.Graph(**defaults), opts.Nodes(**defaults))
#end = timer()
#print(end - start)

#start = timer()
with open("datasets/GephiMatrix_co-citation.csv", 'r') as csvfile:
    dialect = Sniffer().sniff(csvfile.readline())

#pd.set_option('display.width', 120)
#pd.set_option('display.max_columns', 5)
#pd.set_option('display.max_rows', 2000)

df = DataFrame()
for chunk in read_csv("datasets/GephiMatrix_co-citation.csv", sep=dialect.delimiter, mangle_dupe_cols=True, index_col=False, chunksize=1000):
    df = concat([df, chunk], ignore_index=True)

#df.index.name = "delete"
#df = df.drop(index='delete')

nodes = df.columns.values.tolist()
nodes.pop(0)
#print(nodes)
df["Unnamed: 0"] = nodes
df = df.rename(columns={'Unnamed: 0': 'name'})
df = df.set_index(keys='name')
#print(df)
#end = timer()
#print(end - start)

#start = timer()
G = from_pandas_adjacency(df)
#print(nx.info(G))
graph = Graph.from_networkx(G, circular_layout).opts(directed=True, width=600, height=600, arrowhead_length=0.05)
#end = timer()
#print(end - start)

#start = timer()
#circular = bundle_graph(graph)
#plot = datashade(circular, width=800, height=800) * circular.nodes
test = renderer('bokeh').server_doc(graph)
test = test.to_json()
#print(test)
#test = render(graph)
#renderer.save(graph, 'test')

#test = renderer.server_doc(graph)
#test = renderer.server_doc(plot)
#test.title = "test"
#json = dumps(json_item(test, "radialnodelink"))
#print(json)
#end = timer()
#print(end - start)