"""
Author(s): Steven van den Broek, Tom Udding
Created: 2019-06-03
Edited: 2019-06-09
"""
from flask import Blueprint, request
from graphion import server
from graphion.graphing.generator import changeScreen1

apiSwitchBlueprint = Blueprint('apiSwitchBlueprint', __name__, template_folder='templates')

@apiSwitchBlueprint.route('/switch-nodelink', methods = ['POST'])
def worker():
    sid = request.cookies.get(server.config['SESSION_COOKIE_NAME'])
    new_type = request.form['to']
    changeScreen1(new_type, sid)
    return "switched"
