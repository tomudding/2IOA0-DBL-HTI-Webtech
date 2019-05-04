"""
Author(s): Tom Udding
Created: 2019-05-04
Edited: 2019-05-05
"""
from flask import Blueprint, jsonify
from graphion.graphing.generator import generateNodeLinkGraph

apiNodeLinkRadialBlueprint = Blueprint('apiNodeLinkRadialBlueprint', __name__, template_folder='templates')

@apiNodeLinkRadialBlueprint.route('/api/nodelink/radial/', methods=['GET'], strict_slashes=False)
@apiNodeLinkRadialBlueprint.route('/api/nodelink/radial/<file>', methods=['GET'], strict_slashes=False)
@apiNodeLinkRadialBlueprint.route('/api/nodelink/radial/<directed>/<file>', methods=['GET'], strict_slashes=False)
def radialNodeLinkAPI(file=None, directed=None):
    if file is None:
        return abort(400)
    if directed == None or directed.upper() != "DIRECTED":
        isDirected = False
    else:
        isDirected = True
    return jsonify(generateNodeLinkGraph("RADIAL", file, isDirected))