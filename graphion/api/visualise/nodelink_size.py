"""
Author(s): Sam Baggen
Created: 2019-06-12
Edited: 2019-06-12
"""
from flask import Blueprint, request
from graphion import server
from graphion.graphing.generator import changeNodeSize

apiNodeSizeBlueprint = Blueprint('apiNodeSizeBlueprint', __name__, template_folder='templates')

@apiNodeSizeBlueprint.route('/switch-size', methods = ['POST'])
def worker():
    sid = request.cookies.get(server.config['SESSION_COOKIE_NAME'])
    new_size = request.form['to']
    changeNodeSize(new_size, sid)
    return "new node size succesfully applied"