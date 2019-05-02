"""
Author(s): Steven van den Broek
Created: 2019-04-29
Edited: 2019-04-30
"""

import numpy as np
import pandas as pd

from bokeh.plotting import figure, show, output_file
fname = 'GephiMatrix_author_similarity.csv'
f = open(fname, 'r')

# Get author names
line1 = f.readline()
names = line1[1:].split(';');

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
df

# Get 150*150 sub matrix since otherwise the plot is very slow..
df = df.head(150)[names[0:150]]
names = df.columns.tolist()
df

flatten = lambda l: [item for sublist in l for item in sublist]
values = flatten(df.values.tolist())

import panel as pn
import plotly.plotly as py
import plotly.graph_objs as go
colorscale = [[0, 'white'],[1, '#1f78b4']]
#hover_text = ["Value: " + str(value) for value in values]
#data = [go.Heatmap(z=df.values.tolist(), x=names, y=names, colorscale=colorscale, text=hover_text)]
data = [go.Heatmap(z=df.values.tolist(), x=names, y=names, colorscale=colorscale)]
fig = go.Figure(data=data, layout=go.Layout(yaxis=dict(showticklabels=False, ticks=''), xaxis=dict(showticklabels=False, ticks=''), width=800, height=800));
pn.extension('plotly')
pane = pn.Row(fig)
pane.servable()
