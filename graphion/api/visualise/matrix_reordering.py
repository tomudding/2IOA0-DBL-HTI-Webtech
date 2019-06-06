"""
Author(s): Sam Baggen
Created: 2019-06-05
Edited: 2019-06-05
"""
from flask import Blueprint, request
from graphion.graphing.generator import changeOrdering

apiOrderBlueprint = Blueprint('apiOrderBlueprint', __name__, template_folder='templates')

@apiOrderBlueprint.route('/switch-ordering', methods = ['POST'])
def worker():
    new_ordering = request.form['to']
    changeOrdering(new_ordering)
    return "ordered"