"""
Author(s): Tom Udding
Created: 2019-04-29
Edited: 2019-05-01
"""
from flask import Blueprint, render_template

indexBlueprint = Blueprint('indexBlueprint', __name__, template_folder='templates')

@indexBlueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')