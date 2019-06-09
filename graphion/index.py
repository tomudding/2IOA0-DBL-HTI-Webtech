"""
Author(s): Tom Udding
Created: 2019-04-29
Edited: 2019-06-08
"""
from flask import Blueprint, render_template, session

indexBlueprint = Blueprint('indexBlueprint', __name__, template_folder='templates')

@indexBlueprint.route('/', methods=['GET'])
def index():
    if session.get("active", None) is None:
        session['active'] = True
    return render_template('index.html')