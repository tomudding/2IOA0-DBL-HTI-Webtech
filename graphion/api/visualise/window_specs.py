"""
Author(s): Tom Udding
Created: 2019-06-19
Edited: 2019-06-19
"""
from flask import Flask, request, Response, Blueprint, session
from graphion import server
from graphion.session.handler import set_window_width

apiWindowSpecsBlueprint = Blueprint('apiWindowSpecsBlueprint', __name__)

@apiWindowSpecsBlueprint.route('/update-window-specs', methods=['POST'])
def worker():
    sid = request.cookies.get(server.config['SESSION_COOKIE_NAME'])
    w = request.form['w']
    set_window_width(int(w), sid) # this code is not safe
    return "updated"