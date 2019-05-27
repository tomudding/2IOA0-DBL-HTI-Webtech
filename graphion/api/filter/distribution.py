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
from graphion.graphing.generator import getFilePath
import time
import json
from os.path import exists
import os, secrets
from graphion import server

df = 0

apiDegreeBlueprint = Blueprint('apiMatrixBlueprint', __name__, template_folder='templates')

@apiDegreeBlueprint.route('/api/filter/distribution/<type>/<dir>/<file>', methods=['GET'], strict_slashes=False)
@apiDegreeBlueprint.route('/api/filter/distribution/<type>/<dir>', methods=['GET'], strict_slashes=False)
@apiDegreeBlueprint.route('/api/filter/distribution/<type>/<file>', methods=['GET'], strict_slashes=False)
@apiDegreeBlueprint.route('/api/filter/distribution/<type>/', methods=['GET'], strict_slashes=False)
def degreeAPI(file=None, type=None, dir=None):
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

@apiDegreeBlueprint.route('/')

@apiDegreeBlueprint.route('/postmethod', methods = ['POST'])
def worker():
	# read json + reply
	left = float(request.form['left'])
	right = float(request.form['right'])
	type = request.form['type']
	dir = request.form['dir']
	file = request.form['file']
	length,fileUniqueHash = filter_data(left, right, type, dir, file)
    updateHash(fileUniqueHash)
	return str(length)


def filter_data(left, right, type, dir, file):
	filepath = getFilePath(file)
	if(type == 'degree'):
		filtered_df, filtered_names = generate_degree_selection(filepath, left, right, dir)
        global df
        df = filtered_df
		return len(filtered_names), fileUniqueHash
	elif(type == 'weight'):
		filtered_df = generate_edge_selection(filepath, left, right, keep_edges = False)
        global df
        df = filtered_df
		return filtered_df.size, fileUniqueHash



