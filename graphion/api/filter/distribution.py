"""
Author(s): Steven van den Broek, Tom Udding
Created: 2019-05-18
Edited: 2019-06-09
"""
from bokeh.embed import json_item
from flask import Flask, render_template, request, redirect, Response, Blueprint, jsonify, session
from json import dump, dumps
from graphion.filtering.distribution_selection import generate_selection
from graphion.filtering.filter_dataframe import generate_degree_selection, fetch_edge_count, filter_df_weight
import time

from graphion.session.handler import get_partially_filtered_df, get_almost_filtered_df, get_df, set_almost_filtered_df, set_partially_filtered_df, set_filtered_df, set_left_weight, get_left_weight, set_right_weight, get_right_weight

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
    sid = request.cookies.get(server.config['SESSION_COOKIE_NAME'])
    if type == 'weight':
        data = get_df(sid)
    if type == 'degree':
        if dir == 'in':
            data = get_partially_filtered_df(sid)
        if dir == 'out':
            data = get_almost_filtered_df(sid)
    plot = generate_selection(data, kind=type, dir=dir, dataframe=True)
    return dumps(json_item(plot))

@apiDegreeBlueprint.route('/postmethod', methods=['POST'])
def worker():
    # read json + reply
    sid = request.cookies.get(server.config['SESSION_COOKIE_NAME'])
    left = float(request.form['left'])
    right = float(request.form['right'])
    type = request.form['type']
    dir = request.form['dir']
    file = request.form['file']

    if type == 'degree':
        if dir == 'out':
            begin = time.time()
            filtered_df = generate_degree_selection(get_almost_filtered_df(sid), left, right, dir)
            print("Calculating selection took: " + str(time.time()-begin))
            set_filtered_df(filtered_df, sid)
        if dir == 'in':
            begin = time.time()
            filtered_df = generate_degree_selection(get_partially_filtered_df(sid), left, right, dir)
            print("Calculating selection took: " + str(time.time() - begin))
            set_almost_filtered_df(filtered_df, sid)
        return str(len(filtered_df.columns))
    elif(type == 'weight'):
        if left <= 0:
            left = 0.0000000001
        begin = time.time()
        result = fetch_edge_count(get_df(sid), left, right)
        set_left_weight(left, sid) # APP_CONTEXT did not work here, so I proxied it through gsh.
        set_right_weight(right, sid)
        print("Calculating selection took: " + str(time.time() - begin))
        # set_partially_filtered_df(result)
        # return result.astype(bool).sum(axis=0).sum()
        return str(result)

@apiDegreeBlueprint.route('/filter-edges', methods = ['POST'])
def filter_worker():
    sid = request.cookies.get(server.config['SESSION_COOKIE_NAME'])
    if (get_left_weight(sid) is not None) and (get_right_weight(sid) is not None):
        result = filter_df_weight(get_df(sid), get_left_weight(sid), get_right_weight(sid))
        set_partially_filtered_df(result, sid)
    return "fitered"

def getFilePath(file):
    file = file + '.h5'
    return os.path.join(server.config['UPLOAD_FOLDER'], file)