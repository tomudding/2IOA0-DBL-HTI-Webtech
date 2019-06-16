"""
Author(s): Tom Udding
Created: 2019-05-03
Edited: 2019-06-16
"""
from csv import Sniffer
from networkx.classes.digraph import DiGraph
from networkx.convert_matrix import to_pandas_adjacency
from networkx.readwrite.edgelist import read_edgelist
from pandas.core.frame import DataFrame
from pandas.core.reshape.concat import concat
from pandas.io.parsers import read_csv

def processCSVMatrix(file):
    with open(file, 'r') as csvfile:
        dialect = Sniffer().sniff(csvfile.readline())

    df = DataFrame()
    for chunk in read_csv(file, sep=dialect.delimiter, mangle_dupe_cols=True, index_col=False, chunksize=1000):
        df = concat([df, chunk], ignore_index=True)

    nodes = df.columns.values.tolist()
    nodes.pop(0)
    df["Unnamed: 0"] = nodes
    df = df.rename(columns={'Unnamed: 0': 'name'})
    df = df.set_index(keys='name')

    return df

def processEdgeList(file):
    with open(file, 'rb') as edgelist:
        G = read_edgelist(edgelist, create_using=DiGraph(), data=(('weight', float),))

    df = to_pandas_adjacency(G)
    return df