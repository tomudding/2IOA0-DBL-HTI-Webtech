"""
Author(s): Tom Udding
Created: 2019-05-03
Edited: 2019-05-04
"""
import csv
import holoviews as hv
import networkx as nx
import pandas as pd

from bokeh.embed import components
from holoviews.operation.datashader import datashade, bundle_graph

hv.extension('bokeh')

def generateRadialGraph(file, directed):
    if directed == False or directed == None:
        return generateUndirectedRadialGraph(file)
    else:
        return generateDirectedRadialGraph(file)

def generateDirectedRadialGraph(file):
    df = processCSVFile(file)
    return generateComponents(df)

def generateUndirectedRadialGraph(file):
    return ""

############################################################################
# THIS FUNCTION SHOULD PROBABLY BE IN A SEPARATE FILE FOR DATA AGGREGATION #
############################################################################
def processCSVFile(file):
    with open(file, 'r') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.readline())

    df = pd.DataFrame()
    for chunk in pd.read_csv(file, sep=dialect.delimiter, mangle_dupe_cols=True, index_col=False, chunksize=1000):
        df = pd.concat([df, chunk], ignore_index=True)

    nodes = df.columns.values.tolist()
    nodes.pop(0)
    df["Unnamed: 0"] = nodes
    df = df.rename(columns={'Unnamed: 0': 'name'})
    df = df.set_index(keys='name')

    return df

def generateComponents(df):
    G = nx.from_pandas_adjacency(df)
    graph = hv.Graph.from_networkx(G, nx.layout.circular_layout).opts(directed=True)#, width=600, height=600) # width=600, height=600 tools=['hover']
    #bundled = bundle_graph(graph)

    #fig = hv.render(bundled)
    fig = hv.render(graph)
    script, div = components(fig)
    return script, div