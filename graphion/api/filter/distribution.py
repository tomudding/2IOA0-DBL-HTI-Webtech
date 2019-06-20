"""
Author(s): Steven van den Broek, Tom Udding, Tim van de Klundert
Created: 2019-05-18
Edited: 2019-06-19
"""
from bokeh.embed import json_item
from flask import Flask, render_template, request, redirect, Response, Blueprint, jsonify, session
from graphion import server
from graphion.filtering.distribution_selection import generate_selection
from graphion.filtering.cluster import generate_cluster_graph, get_dataframe_from_dot
from graphion.filtering.filter_dataframe import generate_degree_selection, fetch_edge_count, filter_df_weight
from graphion.session.handler import get_partially_filtered_df, get_almost_filtered_df, get_df, \
     set_almost_filtered_df, set_partially_filtered_df, set_filtered_df, set_left_weight, \
     get_left_weight, set_right_weight, get_right_weight, set_cluster_filtered_df
from json import dumps
from os.path import exists, join
from time import time

apiDegreeBlueprint = Blueprint('apiDegreeBlueprint', __name__, template_folder='templates')

# If anyone feels like moving this to another file, be my guest
@apiDegreeBlueprint.route('/api/filter/clustering/graph/', methods=['GET'], strict_slashes=False)
def clusteringAPI():
    print('clusteringAPI')
    sid = request.cookies.get(server.config['SESSION_COOKIE_NAME'])
    data = get_df(sid)
    plot = generate_cluster_graph(data)
    return dumps(json_item(plot))

@apiDegreeBlueprint.route('/api/filter/clustering/choose/<number>', methods=['POST'], strict_slashes=False)
def chooseClusterNumber(number):
    print('cluster number is ' + number)
    sid = request.cookies.get(server.config['SESSION_COOKIE_NAME'])
    data = get_df(sid)
    set_cluster_filtered_df(get_dataframe_from_dot(data, int(number)), sid)
    return dumps(dict())

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
    #            start = time()
    #             item = json_item(plot)
    #             dump(item, json_file)
    #             print("To json {}-{}: ".format(dir, type) + str(time()-start))
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
            begin = time()
            filtered_df = generate_degree_selection(get_almost_filtered_df(sid), left, right, dir)
            print("Calculating selection took: " + str(time()-begin))
            set_filtered_df(filtered_df, sid)
        if dir == 'in':
            begin = time()
            filtered_df = generate_degree_selection(get_partially_filtered_df(sid), left, right, dir)
            print("Calculating selection took: " + str(time() - begin))
            set_almost_filtered_df(filtered_df, sid)
        return str(len(filtered_df.columns))
    elif(type == 'weight'):
        if left <= 0:
            left = 0.0000000001
        begin = time()
        result = fetch_edge_count(sid, get_df(sid), left, right)
        set_left_weight(left, sid) # APP_CONTEXT did not work here, so I proxied it through gsh.
        set_right_weight(right, sid)
        print("Calculating selection took: " + str(time() - begin))
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

#def getFilePath(file):
#    file = file + '.h5'
#    return join(server.config['UPLOAD_FOLDER'], file)