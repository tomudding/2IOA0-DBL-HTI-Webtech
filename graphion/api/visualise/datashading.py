"""
Author(s): Tom Udding
Created: 2019-06-12
Edited: 2019-06-12
"""
from flask import Flask, request, Response, Blueprint, session
from graphion import server
from graphion.session.handler import set_datashading

apiDatashadingBlueprint = Blueprint('apiDatashadingBlueprint', __name__)

@apiDatashadingBlueprint.route('/switch-datashading', methods=['POST'])
def worker():
    sid = request.cookies.get(server.config['SESSION_COOKIE_NAME'])
    state = request.form['datashading']
    set_datashading(state, sid)
    return "switched"