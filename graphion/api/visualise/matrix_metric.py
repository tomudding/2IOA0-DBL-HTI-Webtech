"""
Author(s): Sam Baggen
Created: 2019-06-06
Edited: 2019-06-06
"""
from flask import Blueprint, request
from graphion.graphing.generator import changeMetric

apiMetricBlueprint = Blueprint('apiMetricBlueprint', __name__, template_folder='templates')

@apiMetricBlueprint.route('/switch-metric', methods = ['POST'])
def worker():
    new_metric = request.form['to']
    changeMetric(new_metric)
    return "new metric succesfully applied"