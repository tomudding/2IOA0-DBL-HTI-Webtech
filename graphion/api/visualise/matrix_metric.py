"""
Author(s): Sam Baggen, Tom Udding
Created: 2019-06-06
Edited: 2019-06-09
"""
from flask import Blueprint, request
from graphion import server
from graphion.graphing.generator import changeMetric

apiMetricBlueprint = Blueprint('apiMetricBlueprint', __name__, template_folder='templates')

@apiMetricBlueprint.route('/switch-metric', methods = ['POST'])
def worker():
    sid = request.cookies.get(server.config['SESSION_COOKIE_NAME'])
    new_metric = request.form['to']
    changeMetric(new_metric, sid)
    return "new metric succesfully applied"