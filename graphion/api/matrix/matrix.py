"""
Author(s): Steven van den Broek
Created: 2019-05-05
Edited: 2019-05-05
"""
from bokeh.embed import json_item
from flask import Blueprint
from json import dumps
from graphion.graphing.generator import generateMatrix

apiNodeLinkRadialBlueprint = Blueprint('apiNodeLinkRadialBlueprint', __name__, template_folder='templates')

@apiNodeLinkRadialBlueprint.route('/api/matrix/', methods=['GET'], strict_slashes=False)
@apiNodeLinkRadialBlueprint.route('/api/matrix/<file>', methods=['GET'], strict_slashes=False)

def radialNodeLinkAPI(file=None, directed=None):
    if file is None:
        return abort(400)

    return dumps(json_item(generateNodeLinkGraph(file)))
