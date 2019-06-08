"""
Author(s): Steven van den Broek, Tom Udding
Created: 2019-05-18
Edited: 2019-05-31
"""
from bokeh.embed import json_item
from flask import Flask, render_template, request, redirect, Response, Blueprint, jsonify, session
from json import dump, dumps
from graphion.filtering.distribution_selection import generate_selection
from graphion.filtering.filter_dataframe import generate_degree_selection, fetch_edge_count, filter_df_weight
import time

from graphion.upload import get_partially_filtered_df, get_almost_filtered_df, get_df, set_almost_filtered_df, set_partially_filtered_df, set_filtered_df

from os.path import exists
import os
from graphion import server


apiDegreeBlueprint = Blueprint('apiDegreeBlueprint', __name__, template_folder='templates')

# @apiDegreeBlueprint.route('/api/filter/distribution/<type>/<dir>/<file>', methods=['GET'], strict_slashes=False)
@apiDegreeBlueprint.route('/api/filter/distribution/<type>/<dir>', methods=['GET'], strict_slashes=False)
@apiDegreeBlueprint.route('/api/filter/distribution/<type>/', methods=['GET'], strict_slashes=False)
def degreeAPI(type=None, dir=None):
    # Not used
    # if file is not None:
    #     filePath = 'api/filter/cached_plots/{}-{}-{}.json'.format(file, type, dir)
    #     if (exists(filePath)):
    #         with open(filePath, 'r') as json_file:
    #             return json_file.read()
    #     else:
    #         with open(filePath, 'w+') as json_file:
    #             plot = generate_selection(getFilePath(file), kind=type, dir=dir)
    #            start = time.time()
    #             item = json_item(plot)
    #             dump(item, json_file)
    #             print("To json {}-{}: ".format(dir, type) + str(time.time()-start))
    #         return dumps(item)
    # All filters use this
    if type == 'weight':
        data = get_df()
    if type == 'degree':
        if dir == 'in':
            data = get_partially_filtered_df()
        if dir == 'out':
            data = get_almost_filtered_df()
    plot = generate_selection(data, kind=type, dir=dir, dataframe=True)
    return dumps(json_item(plot))

@apiDegreeBlueprint.route('/postmethod', methods = ['POST'])
def worker():
    # read json + reply
    left = float(request.form['left'])

    right = float(request.form['right'])
    type = request.form['type']
    dir = request.form['dir']
    file = request.form['file']

    if type == 'degree':
        if dir == 'out':
            begin = time.time()
            filtered_df = generate_degree_selection(get_almost_filtered_df(), left, right, dir)
            print("Calculating selection took: " + str(time.time()-begin))
            set_filtered_df(filtered_df)
        if dir == 'in':
            begin = time.time()
            filtered_df = generate_degree_selection(get_partially_filtered_df(), left, right, dir)
            print("Calculating selection took: " + str(time.time() - begin))
            set_almost_filtered_df(filtered_df)
        return len(filtered_df.columns)
    elif(type == 'weight'):
        if left <= 0:
            left = 0.0000000001
        begin = time.time()
        result = fetch_edge_count(get_df(), left, right)
        session['left_weight'] = left
        session['right_weight'] = right
        print("Calculating selection took: " + str(time.time() - begin))
        # set_partially_filtered_df(result)
        # return result.astype(bool).sum(axis=0).sum()
        return str(result)

@apiDegreeBlueprint.route('/filter-edges', methods = ['POST'])
def filter_worker():
    if 'left_weight' in globals():
        result = filter_df_weight(get_df(), left_weight, right_weight)
        set_partially_filtered_df(result)
    return "fitered"

def getFilePath(file):
    file = file + '.h5'
    return os.path.join(server.config['UPLOAD_FOLDER'], file)