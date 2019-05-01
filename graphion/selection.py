"""
Author(s): Tom Udding
Created: 2019-05-01
Edited: 2019-05-01
"""
from flask import Blueprint, render_template

selectionBlueprint = Blueprint('selectionBlueprint', __name__, template_folder='templates')

@selectionBlueprint.route('/selection', methods=['GET'])
def selection():
    return render_template('selection.html')