"""
Author(s): Steven van den Broek
Created: 2019-05-04
Edited: 2019-05-04
"""
#Reading the file
import os
import pandas as pd

from graphion import server

def to_pandas_df(file, amt="all"):
    # open file
    fname = os.path.join(server.config['UPLOAD_FOLDER'], file + '.csv')
    f = open(fname, 'r')
    # Reading first line
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
        names[index] = name + str((i + 1))
        # print(names[index])

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

    if (amt != "all" and isinstance(amt, int)):
        if (amt > 0 and amt < len(names)):
            df = df.head(amt)[names[0:amt]]
            names = df.columns.tolist()
    return df, names
