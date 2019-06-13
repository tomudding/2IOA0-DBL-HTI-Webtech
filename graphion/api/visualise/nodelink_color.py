"""
Author(s): Sam Baggen
Created: 2019-06-12
Edited: 2019-06-12
"""
from flask import Blueprint, request
from graphion import server
from graphion.graphing.generator import changeNodeColor

apiNodeColorBlueprint = Blueprint('apiNodeColorBlueprint', __name__, template_folder='templates')

@apiNodeColorBlueprint.route('/switch-color', methods = ['POST'])
def worker():
    sid = request.cookies.get(server.config['SESSION_COOKIE_NAME'])
    new_color = request.form['to']
    changeNodeColor(new_color, sid)
    return "new node color succesfully applied"