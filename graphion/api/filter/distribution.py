"""
Author(s): Steven van den Broek
Created: 2019-05-18
Edited: 2019-05-20
"""
from bokeh.embed import json_item
from flask import Blueprint
from json import dumps
from graphion.filtering.degree_selection import generate_selection
from graphion.graphing.generator import getFilePath

apiDegreeBlueprint = Blueprint('apiMatrixBlueprint', __name__, template_folder='templates')

@apiDegreeBlueprint.route('/api/filter/distribution/<type>/<dir>/<file>', methods=['GET'], strict_slashes=False)
@apiDegreeBlueprint.route('/api/filter/distribution/<type>/<dir>', methods=['GET'], strict_slashes=False)
@apiDegreeBlueprint.route('/api/filter/distribution/<type>/<file>', methods=['GET'], strict_slashes=False)
@apiDegreeBlueprint.route('/api/filter/distribution/<type>/', methods=['GET'], strict_slashes=False)
def degreeAPI(file=None, type=None, dir=None):
    return dumps(json_item(generate_selection(getFilePath(file), kind=type, dir=dir)))