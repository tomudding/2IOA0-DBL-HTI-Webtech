"""
Author(s): Tom Udding
Created: 2019-05-06
Edited: 2019-05-06
"""
from bokeh.embed import json_item
from flask import Blueprint
from json import dumps
from graphion.graphing.generator import generateNodeLinkGraph

apiNodeLinkForceDirectedBlueprint = Blueprint('apiNodeLinkForceDirectedBlueprint', __name__, template_folder='templates')

@apiNodeLinkForceDirectedBlueprint.route('/api/nodelink/forcedirected/', methods=['GET'], strict_slashes=False)
@apiNodeLinkForceDirectedBlueprint.route('/api/nodelink/forcedirected/<file>', methods=['GET'], strict_slashes=False)
@apiNodeLinkForceDirectedBlueprint.route('/api/nodelink/forcedirected/<directed>/<file>', methods=['GET'], strict_slashes=False)
def forceDirectedNodeLinkAPI(file=None, directed=None):
    if file is None:
        return abort(400)
    if directed == None or directed.upper() != "DIRECTED":
        isDirected = False
    else:
        isDirected = True
    return dumps(json_item(generateNodeLinkGraph("FORCEDIRECTED", file, isDirected)))