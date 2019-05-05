"""
Author(s): Steven van den Broek
Created: 2019-05-05
Edited: 2019-05-05
"""
from bokeh.embed import json_item
from flask import Blueprint
from json import dumps
from graphion.graphing.generator import generateMatrix

apiMatrixBlueprint = Blueprint('apiMatrixBlueprint', __name__, template_folder='templates')

@apiMatrixBlueprint.route('/api/matrix/matrix', methods=['GET'], strict_slashes=False)
@apiMatrixBlueprint.route('/api/matrix/matrix/<file>', methods=['GET'], strict_slashes=False)
def matrixAPI(file=None):
    if file is None:
        return abort(400)

    return dumps(json_item(generateMatrix(file)))
