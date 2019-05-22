"""
Author(s): Steven van den Broek, Tom Udding
Created: 2019-05-18
Edited: 2019-05-22
"""
from bokeh.embed import json_item
from flask import Blueprint
from json import dump, dumps
from graphion.filtering.degree_selection import generate_selection
from graphion.graphing.generator import getFilePath
import time
from os.path import exists

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