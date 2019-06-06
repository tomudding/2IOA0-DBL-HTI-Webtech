"""
Author(s): Steven van den Broek
Created: 2019-06-03
Edited: 2019-06-03
"""
from flask import Blueprint, request
from graphion.graphing.generator import changeScreen1

apiSwitchBlueprint = Blueprint('apiSwitchBlueprint', __name__, template_folder='templates')

@apiSwitchBlueprint.route('/switch-nodelink', methods = ['POST'])
def worker():
    new_type = request.form['to']
    changeScreen1(new_type)
    return "switched"
