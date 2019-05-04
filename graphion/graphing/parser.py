"""
Author(s): Tom Udding
Created: 2019-05-03
Edited: 2019-05-05
"""
from csv import Sniffer
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