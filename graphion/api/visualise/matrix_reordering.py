"""
Author(s): Sam Baggen, Tom Udding
Created: 2019-06-05
Edited: 2019-06-09
"""
from flask import Blueprint, request
from graphion import server
from graphion.graphing.generator import changeOrdering

apiOrderBlueprint = Blueprint('apiOrderBlueprint', __name__, template_folder='templates')

@apiOrderBlueprint.route('/switch-ordering', methods = ['POST'])
def worker():
    sid = request.cookies.get(server.config['SESSION_COOKIE_NAME'])
    new_ordering = request.form['to']
    changeOrdering(new_ordering, sid)
    return "ordered"