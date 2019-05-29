"""
Author(s): Steven van den Broek, Tom Udding
Created: 2019-05-18
Edited: 2019-05-22
"""
from bokeh.embed import json_item
from flask import Flask, render_template, request, redirect, Response, Blueprint
from json import dump, dumps
from graphion.filtering.degree_selection import generate_selection
from graphion.filtering.edge_weight_selection import generate_degree_selection, generate_edge_selection
from graphion.filter import get_df
import time

from os.path import exists
import os
from graphion import server



apiDegreeBlueprint = Blueprint('apiMatrixBlueprint', __name__, template_folder='templates')

@apiDegreeBlueprint.route('/api/filter/distribution/<type>/<dir>/<file>', methods=['GET'], strict_slashes=False)
@apiDegreeBlueprint.route('/api/filter/distribution/<type>/<dir>', methods=['GET'], strict_slashes=False)
@apiDegreeBlueprint.route('/api/filter/distribution/<type>/', methods=['GET'], strict_slashes=False)
def degreeAPI(file=None, type=None, dir=None):
    # Not used
    if file is not None:
        filePath = 'api/filter/cached_plots/{}-{}-{}.json'.format(file, type, dir)
        if (exists(filePath)):
            with open(filePath, 'r') as json_file:
                return json_file.read()
        else:
            with open(filePath, 'w+') as json_file:
                plot = generate_selection(getFilePath(file), kind=type, dir=dir)
                start = time.time()
                item = json_item(plot)
                dump(item, json_file)
                print("To json {}-{}: ".format(dir, type) + str(time.time()-start))
            return dumps(item)
    # All filters use this
    else:
        item = json_item(generate_selection(get_filtered_df(), kind=type, dir=dir, dataframe=True))

        return dumps(item)

@apiDegreeBlueprint.route('/postmethod', methods = ['POST'])
def worker():
    # read json + reply
    left = float(request.form['left'])
    right = float(request.form['right'])
    type = request.form['type']
    dir = request.form['dir']
    file = request.form['file']
    length = filter_data(left, right, type, dir, file)
    return str(length)


def filter_data(left, right, type, dir, file):
    global filtered_df
    if(type == 'degree'):
        df = get_filtered_df()
        filtered_df = generate_degree_selection(df, left, right, dir)
        return len(filtered_df.columns)
    elif(type == 'weight'):
        df = get_df()
        filtered_df = generate_edge_selection(df, left, right, keep_edges = True)
        return len(filtered_df.columns)

def get_filtered_df():
    if 'filtered_df' in globals():
        return filtered_df.copy()
    return get_df()

def getFilePath(file):
    file = file + '.h5'
    return os.path.join(server.config['UPLOAD_FOLDER'], file)


